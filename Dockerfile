FROM python:3.10-slim

# フォントキャッシュなどに必要なツールのみ（フォントはローカルに含む）
RUN apt-get update && apt-get install -y fontconfig && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
