from fastapi import FastAPI
from pydantic import BaseModel
import requests
from typing import List, Dict, Any
import time
import os

app = FastAPI(title="Agent 3 - Analyzer")

# Ma-nsach t-bedel API Key dyalek hna!
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 

class Agent3Input(BaseModel):
    products: List[Dict[str, Any]]

@app.post("/api/v1/analyze")
def analyze_data(data: Agent3Input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    You are an expert e-commerce analyst. Analyze this JSON list of products:
    {data.products}
    
    Please provide a very short, professional summary containing:
    1. Total number of products found.
    2. The cheapest product (Name and Price).
    3. A brief 1-sentence insight about the prices.
    
    Respond clearly without markdown code blocks.
    """
    
    payload = {
        "model": "allam-2-7b", # Nfs l-model li khdem lik f Agent 1 w 2
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 300
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            summary = response.json()["choices"][0]["message"]["content"].strip()
            return {"status": "success", "summary": summary}
        else:
            # Hna ghadi n-tb3o l-error l-7a9i9i f terminal ila Groq rfed t-talab
            print(f"⚠️ Groq Error: {response.text}") 
            return {"status": "error", "message": f"Groq API Error: {response.status_code}"}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}