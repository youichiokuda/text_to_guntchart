# 📅 自然文 → ガントチャート 生成アプリ

このアプリは、自然言語で書かれた `.txt` ファイルを ChatGPT (gpt-4o-mini) を使って解析し、タスクと期間を抽出してガントチャートを自動生成します。

## 📁 フォルダ構成（推奨）

```
guntchartmake3/
├── app.py                 # Streamlit アプリ本体
├── Dockerfile             # Docker 実行用
├── requirements.txt       # 必要なライブラリ一覧
├── README.md              # このファイル
└── taskfiles/             # ✅ .txtファイルをここに入れてください
    └── sample_task.txt
```

## 🚀 起動方法

### 1. Dockerイメージのビルド

```bash
cd guntchartmake3
docker build -t gantt-chart-app .
```

### 2. アプリの起動

```bash
docker run -p 8501:8501 gantt-chart-app
```

その後、以下にアクセス：

```
http://localhost:8501
```

## ✏️ `.txt` ファイルの書き方

```
5月1日から15日まではキックオフ準備を行う。
6月中にネットワーク要件を固めたい。
10月に院内ネットワークの発注、
11月にクラウド環境と電子カルテの発注を予定している。
```

## 🔐 OpenAI APIキーの準備

- [OpenAI Platform](https://platform.openai.com/account/api-keys) にてAPIキーを発行してください。
- アプリ起動後、画面で入力する必要があります。
