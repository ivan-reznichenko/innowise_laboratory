# 1. Base Image
FROM python:3.9-slim

# 2. Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Working Directory
WORKDIR /app

# 4. Dependency Management
COPY requirements.txt .

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Application Code
COPY . .

# 6. Port Exposure 
EXPOSE 8000

# 7. Start Command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]