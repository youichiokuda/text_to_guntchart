FROM python:3.10-slim

# ✅ 日本語フォント（Takao + IPA）をインストール
RUN apt-get update && apt-get install -y \
    fonts-takao \
    fonts-ipafont-gothic \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /app

# プロジェクトファイルをコピー
COPY . /app

# Pythonライブラリのインストール
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit が使用するポートを公開
EXPOSE 8501

# アプリを起動
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
