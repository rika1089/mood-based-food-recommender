import streamlit as st
from app import detect_emotion, recommend_food, safe_response, get_food_image

st.set_page_config(page_title="MoodMeal 🍽️", page_icon="🥗", layout="centered")
st.markdown("### 🧠 *Feel. Eat. Heal.* — Your AI companion for emotional wellness through food 🌿")
st.divider()

user = st.text_input("How are you feeling today?")

if user:
    emotion, scores = detect_emotion(user)
    food = recommend_food(emotion)
    reply = safe_response(emotion, food)

    if scores:
        st.subheader("📊 Model Confidence Overview")
        top_conf = max(scores.values())
        st.markdown(f"**Detected Emotion:** `{emotion.upper()}`")
        st.markdown(f"**Confidence:** `{top_conf * 100:.2f}%`")
        st.markdown("### 🔍 Emotion Probability Breakdown")
        st.bar_chart(scores)
        st.progress(top_conf)

    st.markdown(f"**MoodMeal:** {reply}")
    img = get_food_image(food)
    if img:
        st.image(img, caption=f"🍽️ {food}")