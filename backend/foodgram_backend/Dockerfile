FROM python:3.9-slim
WORKDIR /app
RUN pip install gunicorn==20.1.0
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:2000", "foodgram_backend.wsgi"]
