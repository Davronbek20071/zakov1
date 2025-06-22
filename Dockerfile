FROM python:3.10-slim

# Ishchi papka yaratamiz
WORKDIR /app

# Talablar faylini nusxalaymiz
COPY requirements.txt .

# Kutubxonalarni o‘rnatamiz
RUN pip install --upgrade pip && pip install -r requirements.txt

# Loyihani ko‘chiramiz
COPY . .

# Botni ishga tushiramiz
CMD ["python", "main.py"]
