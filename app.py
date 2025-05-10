import streamlit as st
from openai import OpenAI
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import os
import re

# ✅ 日本語フォント設定（自動検出）
font_candidates = [
    "/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf",
    "/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴ ProN W3.ttc",  # macOS
    "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
]
for font_path in font_candidates:
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        plt.rcParams["font.family"] = fm.FontProperties(fname=font_path).get_name()
        break
else:
    plt.rcParams["font.family"] = "sans-serif"

# JSON形式らしさの確認
def is_json_like(text):
    return bool(re.match(r'^[\s]*[\[{]', text.strip()))

# ChatGPT API呼び出し
def extract_tasks_from_text(text, api_key):
    client = OpenAI(api_key=api_key)
    prompt = f"""
以下のテキストからプロジェクトのタスクと期間（開始日・終了日）を抽出し、以下のJSON形式で返してください：

[
  {{"task": "ネットワーク設計", "start": "2025-06-01", "end": "2025-06-15"}}
]

説明やテンプレート形式は不要です。

テキスト:
{text}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたはプロジェクトマネージャーのアシスタントです。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# JSON → DataFrame
def json_to_df(json_text):
    if not json_text.strip() or not is_json_like(json_text):
        st.error("❌ ChatGPTが有効なJSONを返しませんでした。以下をご確認ください：")
        st.code(json_text)
        return pd.DataFrame()
    try:
        task_list = json.loads(json_text)
        df = pd.DataFrame(task_list)
        df['start'] = pd.to_datetime(df['start'], format="%Y-%m-%d")
        df['end'] = pd.to_datetime(df['end'], format="%Y-%m-%d")
        return df
    except Exception as e:
        st.error("❌ JSONまたは日付変換に失敗しました。以下の出力を確認してください：")
        st.code(json_text)
        raise e

# ガントチャート表示
def plot_gantt(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    for i, row in df.iterrows():
        ax.barh(row['task'], (row['end'] - row['start']).days, left=row['start'], height=0.5)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    plt.title("自然文から生成されたガントチャート")
    plt.tight_layout()
    st.pyplot(fig)

# Streamlit UI
st.title("📤 .txtアップロード → ガントチャート生成")

api_key = st.text_input("🔑 OpenAI APIキーを入力してください", type="password")
uploaded_file = st.file_uploader("📁 .txtファイルをアップロードしてください", type="txt")

if uploaded_file and api_key:
    try:
        text = uploaded_file.read().decode("utf-8")
        st.success("✅ ファイル読み込み成功")
        st.subheader("📄 アップロード内容")
        st.text(text[:1000] + ("..." if len(text) > 1000 else ""))

        if st.button("🚀 ChatGPTで解析してガントチャート生成"):
            with st.spinner("ChatGPTで解析中..."):
                json_text = extract_tasks_from_text(text, api_key)
                df = json_to_df(json_text)

            if not df.empty:
                st.success("✅ ガントチャート生成完了！")
                st.subheader("📋 抽出されたタスク一覧")
                st.dataframe(df)

                st.subheader("📈 ガントチャート")
                plot_gantt(df)

    except Exception as e:
        st.error(f"❌ エラーが発生しました: {e}")
