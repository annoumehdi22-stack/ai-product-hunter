import requests

# حط الـ API Key ديالك هنا بلاصة النجمات
GROQ_API_KEY = "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" 

url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}"
}

print("⏳ Kan-9elbo 3la les models li khdamin...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("\n✅ Hahoma les models li 3ndk l7e9 tkhdem bihom (Khtar wahed fihom):")
    print("-" * 50)
    for model in data.get("data", []):
        print(f"👉 {model['id']}")
    print("-" * 50)
else:
    print(f"❌ Mochkil f l'API: {response.status_code}")
    print(response.text)