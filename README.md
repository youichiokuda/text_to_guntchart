# 📅 Streamlit + ChatGPT 自然文 → ガントチャート アプリ

このアプリは、自然文（例：「5月1日から15日はキックオフ」など）を書いた `.txt` ファイルを読み込み、OpenAI GPT-4o-mini によって解析し、タスクの期間を抽出してガントチャートを描画します。

---

## ✅ フォルダ構成（Streamlit Cloud 対応）

```
guntchartmake3/
├── app.py                 # Streamlit アプリ本体
├── requirements.txt       # ライブラリ定義
├── taskfiles/             # ✅ .txtファイルをここに入れる
│   └── sample_task.txt
```

---

## 🚀 デプロイ方法（Streamlit Cloud）

1. GitHub にこのプロジェクトを push
2. https://streamlit.io/cloud にログイン
3. 「New App」→ リポジトリを選択
4. アプリファイル: `app.py`
5. ブランチ名: `main`（例）
6. 「Deploy」

---

## 📂 📥 フォルダパスの入力方法（重要）

アプリの実行画面で「📁 フォルダパスを入力してください」という欄には、次のように入力します：

```
taskfiles
```

または

```
./taskfiles
```

どちらでもOKです（カレントディレクトリからの相対パス）。**絶対パス（/Users/〜）は使用できません。**

---

## 🔐 OpenAI APIキーについて

Streamlitアプリ実行時に入力欄に貼り付ける形式になっています。  
環境変数や secrets.toml を使いたい場合は別途設定が必要です。

---

## ✏️ sample_task.txt の例

```
5月1日から15日まではキックオフ準備を行う。
6月にネットワーク要件を固める。
10月に院内ネットワークの発注、
11月にクラウドと電子カルテの発注を予定。
12月〜1月に工事、5月に完全移行。
```

---

## 🖼️ 出力

- 📋 タスク一覧表（DataFrame形式）
- 📈 ガントチャート（Matplotlib）

---

## 💡 ローカルで動かす場合

```bash
pip install -r requirements.txt
streamlit run app.py
```

その際、読み込みフォルダに以下のような絶対パスも使用可能：

```
/Users/yourname/Downloads/guntchartmake3/taskfiles
```

---

## 🙌 お問い合わせ

フィードバック歓迎です！