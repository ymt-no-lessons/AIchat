import streamlit as st
import requests

st.set_page_config(page_title="ちいかわAIチャット", layout="centered")

# -----------------------
# 🤖 AI応答関数（Hugging Face Inference API）
# -----------------------
def get_ai_response(user_input, character):
    if character == "ちいかわ":
        system_prompt = "あなたは臆病でかわいらしいキャラ「ちいかわ」として、短く反応してください。"
    elif character == "ハチワレ":
        system_prompt = "あなたは素直で丁寧なキャラ「ハチワレ」として、明るくポジティブに返事してください。"
    elif character == "うさぎ":
        system_prompt = "あなたは自由奔放でテンション高めな「うさぎ」です。元気いっぱいに返してください。"

    prompt = f"{system_prompt}\nユーザー: {user_input}\nちいかわたち:"

    API_URL = "https://api-inference.huggingface.co/models/rinna/japanese-gpt-neox-3.6b-instruction-ppo"
    headers = {}  # Hugging Face Spaces上では空でOK（ローカルではAPIキーが必要）

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 60},
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            reply = result[0]["generated_text"].split("ちいかわたち:")[-1].strip()
            return reply
        else:
            return "（AIの返事がうまくできなかったみたい…）"
    except Exception as e:
        return f"（通信エラー：{e}）"

# -----------------------
# 🖼️ UIとチャット処理
# -----------------------

# セッション状態にメッセージ保存
if "messages" not in st.session_state:
    st.session_state.messages = []

# タイトルとキャラ選択
st.title("🧸 ちいかわAIチャット")
character = st.selectbox("キャラを選んでね", ["ちいかわ", "ハチワレ", "うさぎ"])
user_icon = "🧍"
char_icon = {"ちいかわ": "🌟", "ハチワレ": "😺", "うさぎ": "🐰"}[character]

# チャット表示部分
st.markdown("---")
for msg in st.session_state.messages:
    icon, speaker, text = msg
    if speaker == "user":
        st.markdown(f"<div style='text-align:right;'>{user_icon}：{text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:left;'>{icon}：{text}</div>", unsafe_allow_html=True)

# 入力欄
user_input = st.text_input("メッセージを送ってみよう", key="input")

if user_input:
    # ユーザーの発言を保存
    st.session_state.messages.append((user_icon, "user", user_input))

    # AIから返答を取得
    reply = get_ai_response(user_input, character)

    # 返事を追加して更新
    st.session_state.messages.append((char_icon, "bot", reply))
    st.experimental_rerun()
