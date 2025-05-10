# 📅 自然文 → ガントチャート生成アプリ（Streamlit + OpenAI）

このアプリは、自然文で記述された `.txt` ファイルをアップロードし、OpenAI (gpt-4o-mini) を使ってプロジェクトのタスクと期間を抽出し、ガントチャートを自動生成します。

---

## ✅ 特徴

- `.txt` ファイルをアップロードするだけでOK（フォルダパス不要）
- 日本語の自然文をChatGPTで解析し、JSON形式で期間付きタスクに変換
- `matplotlib` で日本語対応のガントチャートを描画
- **日本語フォントはシステムにあるOSSフォントを自動使用**
- Dockerでローカル環境構築も可能

---

## 📂 フォルダ構成

```
guntchartmake_app/
├── app.py               # Streamlit アプリ本体
├── requirements.txt     # Pythonライブラリ
├── Dockerfile           # 日本語フォントありDocker構成（Takao + IPA + Noto）
└── sample_task.txt      # （任意）アップロード用テキストサンプル
```

---

## 🚀 実行方法

### 1. OpenAI APIキーの取得

- https://platform.openai.com/account/api-keys から新規作成
- `sk-...` で始まるキーをアプリ画面の入力欄に貼り付け

### 2. Dockerでローカル実行（推奨）

```bash
docker build -t gantt-chart-app .
docker run -p 8501:8501 gantt-chart-app
```

起動後、`http://localhost:8501` にアクセス。

---

## 📤 入力方法

- アプリ画面で `.txt` ファイルをアップロード
- 例：

```
5月1日から15日まではキックオフ準備を行う。
6月にネットワーク要件を固める。
10月に院内ネットワークの発注、
11月にクラウドと電子カルテの発注を予定している。
```

---

## 📈 出力

- 📋 タスク一覧（表形式）
- 📅 ガントチャート（日本語対応、時系列上→下、X軸上部）

---

## 🔤 日本語フォントについて（Docker）

このアプリはDocker内で以下のフォントをインストールして使用します：

- `fonts-takao`
- `fonts-ipafont-gothic`
- `fonts-noto-cjk`

また、`app.py` ではこれらのフォントの存在を確認し、自動的に `matplotlib` に適用しています。

---

## 💬 注意事項

- モデルは `gpt-4o-mini` を使用します（無料アカウントでは利用不可）
- APIキーは **絶対にGitHub等に公開しないよう注意してください**

---

## 🙌 お問い合わせ

ご質問・改善提案などありましたら、お気軽にどうぞ。
