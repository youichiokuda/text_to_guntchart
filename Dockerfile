FROM python:3.10-slim

# 日本語フォントは不要（ローカルに同梱するため）
# 必要なツールのインストール（念のため fontconfig）
RUN apt-get update && apt-get install -y \
    fontconfig \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# プロジェクトファイル一式をコピー（フォントも含む）
COPY . /app

# Pythonライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit のポートを開放
EXPOSE 8501

# アプリ起動コマンド
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
