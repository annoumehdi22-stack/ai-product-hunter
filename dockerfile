# كانجيبو نسخة خفيفة ديال بايثون
FROM python:3.10-slim

# كنحددو الدوسي فين غنخدمو لداخل
WORKDIR /app

# كانكوبيو ملف المكتبات ونانسطاليوهم
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# كانكوبيو الكود ديالنا كامل
COPY . .