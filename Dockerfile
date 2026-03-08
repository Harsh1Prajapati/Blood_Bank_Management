# 1. Base image Python ki lenge
FROM python:3.9-slim

# 2. Container ke andar ek working directory banayenge
WORKDIR /app

# 3. Requirements file copy karenge aur install karenge
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Baaki ka poora code copy karenge
COPY . .

# 5. Port 5000 open karenge
EXPOSE 5000

# 6. Project ko run karne ka command
CMD ["python", "main.py"]
