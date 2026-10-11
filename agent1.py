from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI(title="Agent 1 - URL Generator")

# حط الـ API Key ديالك هنا
GROQ_API_KEY = "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" 

class Agent1Input(BaseModel):
    product_name: str
    category: str

@app.post("/api/v1/generate-url")
def generate_url(data: Agent1Input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    You are an AI Search Agent. Generate a valid AliExpress search URL based on the product and category.
    Product: {data.product_name}
    Category: {data.category}
    
    Return ONLY the raw URL starting with https://www.aliexpress.com/wholesale?SearchText=
    Replace spaces with '+' in the search text. Do not add any explanation or markdown formatting.
    """
    
    payload = {
        "model": "openai/gpt-oss-120b",  # درنا نفس الموديل اللي خدم ليك فـ agent2
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 100
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # إيلا الجواب كان صحيح
        if response.status_code == 200:
            generated_url = response.json()["choices"][0]["message"]["content"].strip()
            return {"status": "success", "generated_url": generated_url}
        
        # إيلا Groq رفض الطلب، غيبين لينا علاش بالضبط
        else:
            error_details = response.text
            print(f"⚠️ خطأ من Groq: {error_details}")
            return {"status": "error", "message": f"Groq Error: {response.status_code} - {error_details}"}
            
    except Exception as e:
        return {"status": "error", "message": f"Code Error: {str(e)}"}