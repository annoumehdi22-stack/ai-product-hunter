from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import requests
import os
import sqlite3
import json
import re
import markdownify

app = FastAPI(title="AI Smart Product Hunter")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

# 1. إعداد قاعدة البيانات SQLite وفري الجدول إيلا ماكانش
def init_db():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price TEXT,
            link TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db() # كنعيطو ليها أول مايخدم السيرفور

class CategoryRequest(BaseModel):
    category_url: str

def scrape_page_text(url: str):
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(8)
        
        # كنجبدو الـ HTML كامل
        raw_html = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
        
        # كنحولو HTML لـ Markdown، وكنحيدو التصاور والسكريبتات اللي كياكلو لينا الـ Tokens على والو
        clean_md = markdownify.markdownify(raw_html, strip=['img', 'svg', 'script', 'style', 'iframe'])
        
        return clean_md
    except Exception as e:
        print(f"Error scraping: {e}")
        return None
    finally:
        driver.quit()

def extract_with_groq(page_text: str):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    You are an e-commerce data extraction assistant. 
    Analyze the following text from an e-commerce site and extract a list of products.
    Limit your extraction to a MAXIMUM of 10 products.
    
    For each product, find:
    - title (string)
    - price (string)
    - link (string if available, else null). CRITICAL: Clean the URL. Remove ALL tracking parameters. The link MUST stop at ".html" (e.g., https://www.aliexpress.com/item/123456.html). Do NOT include "?algo_pvid=" or anything after it.
    
    Return ONLY a valid JSON array of objects with keys: "title", "price", "link". No extra text, no markdown formatting.
    
    Webpage text:
    {page_text[:18000]} 
    """
    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 4000
    }
    response = requests.post(url, json=payload, headers=headers)
    
    # Hna zidna print bach n-chofo l'error b dbt f terminal
    if response.status_code == 200:
        res_data = response.json()
        return res_data["choices"][0]["message"]["content"]
    else:
        print(f"❌ Groq Error Status: {response.status_code}")
        print(f"❌ Groq Error Response: {response.text}")
        return None

@app.post("/api/v1/ai-hunt")
def ai_hunt_products(data: CategoryRequest):
    print(f"🔄 Kan-scrapiw page: {data.category_url}")
    raw_text = scrape_page_text(data.category_url)
    
    if not raw_text:
        raise HTTPException(status_code=500, detail="Mochkil f scraping dyal page")
        
    print("🤖 Kan-sifto d-data l Groq AI bach y-extradiha...")
    ai_result_str = extract_with_groq(raw_text)
    
    if not ai_result_str:
        raise HTTPException(status_code=500, detail="Mochkil m3a Groq API Key wla l'model")
        
    try:
        # كننظفو الجواب من أي علامات ديال Markdown بحال ```json
        cleaned_str = ai_result_str.replace("```json", "").replace("```", "").strip()
        
        # دابا عاد نحولوه لـ JSON حقيقي
        products_list = json.loads(cleaned_str)
        
        # تخزين المنتجات في SQLite
        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()
        for prod in products_list:
            cursor.execute("""
                INSERT INTO products (title, price, link)
                VALUES (?, ?, ?)
            """, (prod.get("title"), prod.get("price"), prod.get("link")))
        conn.commit()
        conn.close()
        
        
    except Exception as e:
        print(f"⚠️ Mochkil f tkhzin f database: {e}")
        products_list = ai_result_str # إيلا وقع شي غلط فرجح النص كما هو

    return {
        "status": "success",
        "saved_to_sqlite": True,
        "extracted_products": products_list
    }
@app.get("/api/v1/products")
def get_saved_products():
    try:
        # كنتكونيكطاو لـ قاعدة البيانات
        conn = sqlite3.connect("products.db")
        
        # هاد السطر كيخلي SQLite ترجع لينا الداتا بالسميات ديال الأعمدة (title, price...) ماشي غير أرقام
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        # كنجبدو كلشي من الجدول، ورتبناهم باش الجديد يبان هو الأول
        cursor.execute("SELECT * FROM products ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        
        # كنحولو النتيجة لـ ليستة ديال JSON
        saved_products = [dict(row) for row in rows]
        
        return {
            "status": "success",
            "total_in_db": len(saved_products),
            "products": saved_products
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Mochkil f database: {e}"}