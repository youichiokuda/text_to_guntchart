import streamlit as st
from openai import OpenAI
import os
import glob
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import re

# ✅ 日本語フォントを直接指定（Noto Sans CJK JPなどがCloud環境にある場合）
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "IPAexGothic", "TakaoGothic", "Hiragino Maru Gothic Pro", "Arial Unicode MS", "sans-serif"]

def is_json_like(text):
    return bool(re.match(r'^\s*[\[{]', text.strip()))

def extract_tasks_from_text(text, api_key):
    client = OpenAI(api_key=api_key)
    prompt = f"""
以下のテキストからプロジェクトのタスクとその期間（開始日・終了日）を抽出してください。
出力は以下のような JSON 形式で返してください（説明不要）：

[
  {{"task": "ネットワーク設計", "start": "2025-06-01", "end": "2025-06-15"}},
  ...
]

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

def read_texts(folder_path):
    files = glob.glob(os.path.join(folder_path, "*.txt"))
    texts = []
    st.subheader("📂 読み込んだファイル一覧と内容")
    for f in files:
        st.markdown(f"✅ **{os.path.basename(f)}**")
        with open(f, "r", encoding="utf-8") as file:
            content = file.read()
            st.code(content, language="text")
            texts.append(content)
    return "\n".join(texts)

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
st.title("📅 自然文ファイル → ガントチャート生成アプリ")

folder_path = st.text_input("📁 フォルダパスを入力してください", value="./taskfiles")
api_key = st.text_input("🔑 OpenAI APIキー", type="password")

if folder_path and api_key:
    try:
        with st.spinner("ファイル読み込み中..."):
            text = read_texts(folder_path)
        st.success("✅ ファイル読み込み完了")

        if not text.strip():
            st.warning("⚠️ 読み込まれたテキストが空です。内容をご確認ください。")
        else:
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
