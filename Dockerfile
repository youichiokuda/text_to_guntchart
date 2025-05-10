FROM python:3.10-slim

# 日本語フォントをインストール（Takao + IPA）
RUN apt-get update && apt-get install -y \
    fonts-takao \
    fonts-ipafont-gothic \
    fonts-noto-cjk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
