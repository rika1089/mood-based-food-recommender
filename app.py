# ============================================================
# 🍽️ MoodMeal — Emotion-Aware Food & Wellness Chatbot (v2)
# ============================================================

import streamlit as st
import requests, os, csv, datetime, random, time
from io import BytesIO
from PIL import Image
from transformers import pipeline

# --------------------- Configuration ------------------------
st.set_page_config(page_title="MoodMeal 🍽️", page_icon="🍽️", layout="centered")

# --- Disable common HuggingFace warnings ---
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# --- Streamlit header ---
st.markdown("""
<h1 style='text-align: center; 
           background: linear-gradient(90deg, #FF4B2B, #FF416C);
           -webkit-background-clip: text; 
           color: transparent;
           font-size: 42px;'>
🍽️ MoodMeal — Feel. Eat. Heal.
</h1>
""", unsafe_allow_html=True)

st.caption("A hybrid AI chatbot that recommends comforting foods & mindfulness tips based on your emotions 💭")
NEGATION_WORDS = ["not", "n't", "didn't", "don't", "never", "no", "can't", "couldn't", "worse", "bad"]
POSITIVE_CUES = ["happy", "joy", "excited", "good", "great", "love", "amazing"]
NEGATIVE_EMOTION = "sadness"

def preprocess_and_adjust_emotion(text):
    text_lower = text.lower()
    if any(neg in text_lower for neg in NEGATION_WORDS) and any(pos in text_lower for pos in POSITIVE_CUES):
        return NEGATIVE_EMOTION
    return None


# --------------------- Load Models --------------------------
@st.cache_resource
def load_models():
    return pipeline(
        "text-classification",
        model="bhadresh-savani/distilbert-base-uncased-emotion",
        top_k=None
    )

emotion_classifier = load_models()

# --------------------- Emotion → Food -----------------------
emotion_food_map = {
    "joy": ["smoothie", "ice cream", "fruit salad"],
    "sadness": ["dark chocolate", "soup", "mac & cheese"],
    "anger": ["herbal tea", "yogurt", "salad"],
    "fear": ["cookies", "pasta"],
    "love": ["pizza", "strawberries"],
    "surprise": ["cupcake", "popcorn"],
    "neutral": ["coffee", "sandwich"],
    "hungry": ["pizza", "burger", "sandwich"]
}

# --------------------- Emotion → Wellness -------------------
emotion_wellness_map = {
    "joy": [
        "Celebrate with a 30-second gratitude note — write one thing you’re thankful for.",
        "Share your joy: message a friend a quick thank-you or compliment."
    ],
    "sadness": [
        "Try a 60-second box breathing: inhale 4s — hold 4s — exhale 4s — hold 4s.",
        "Do a 2-minute walk or stretch to change the body state."
    ],
    "anger": [
        "Try progressive muscle relaxation for 60s: clench then release your muscles.",
        "Count slowly to 10 while taking deep breaths."
    ],
    "fear": [
        "Grounding exercise: name 5 things you see, 4 you can touch, 3 you can hear.",
        "Sip a warm drink mindfully for 1–2 minutes."
    ],
    "love": [
        "Share how you feel — send a short positive message to someone you care about.",
        "Take a mindful bite: savour your food slowly."
    ],
    "surprise": [
        "Pause and take 3 slow breaths to process the feeling.",
        "Write down one small takeaway from what surprised you."
    ],
    "neutral": [
        "Take a short moment to check-in: rate your energy level (1–5).",
        "Try a 2-minute stretch to re-energize your body."
    ],
    "hungry": [
        "Eat a small balanced snack (protein + carbs).",
        "Hydrate first — thirst can feel like hunger."
    ]
}

# --------------------- Image Retrieval -----------------------
PIXABAY_API_KEY = "53013203-c13f1313b56468c8334790092"

SAFE_FOOD_IMAGES = {
    "pizza": "https://images.unsplash.com/photo-1594007654729-407eedc4be65",
    "burger": "https://images.unsplash.com/photo-1550547660-d9450f859349",
    "ice cream": "https://images.unsplash.com/photo-1505253216365-40b43a2cc6d2",
    "chocolate": "https://images.unsplash.com/photo-1615485737457-1a274c178f3c",
    "salad": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1",
    "soup": "https://images.unsplash.com/photo-1579694155554-d19efb6c579b"
}

@st.cache_resource
def get_food_image(food_name):
    try:
        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={food_name}&image_type=photo&orientation=square&per_page=3"
        response = requests.get(url, timeout=10)
        
        # check response validity
        if response.status_code != 200:
            st.warning(f"⚠️ Pixabay API error: {response.status_code}")
            return None
        
        data = response.json()
        if not data.get("hits"):
            st.info("No image found for this food. Using fallback.")
            return None

        image_url = data["hits"][0]["webformatURL"]
        img_resp = requests.get(image_url, timeout=10)

        # check if the URL really returns an image
        if "image" not in img_resp.headers.get("Content-Type", ""):
            st.warning("⚠️ Invalid image content received.")
            return None

        return Image.open(BytesIO(img_resp.content))

    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# --------------------- Utility Functions ---------------------
def detect_emotion(user_input):
    # First, apply negation-aware rule
    adjusted = preprocess_and_adjust_emotion(user_input)
    if adjusted:
        return adjusted  # directly output sadness if rule triggered
    
    # Otherwise, use model
    result = emotion_classifier(user_input)
    if isinstance(result[0], list):
        top = max(result[0], key=lambda x: x['score'])
        emotion = top['label'].lower()
    else:
        emotion = result[0]['label'].lower()
    return emotion


def recommend_food(emotion):
    foods = emotion_food_map.get(emotion, ["coffee"])
    return random.choice(foods)

def recommend_wellness(emotion):
    tips = emotion_wellness_map.get(emotion, ["Take a slow breath and relax."])
    return random.choice(tips)

def log_interaction(user_input, emotion, food, tip, feedback=None):
    log_file = "moodmeal_feedback.csv"
    header = ["timestamp", "user_input", "emotion", "food", "tip", "feedback"]
    exists = os.path.exists(log_file)
    with open(log_file, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(header)
        writer.writerow([datetime.datetime.now().isoformat(), user_input, emotion, food, tip, feedback or ""])

# --------------------- Main App ------------------------------
st.subheader("💬 Tell me how you’re feeling:")
user_input = st.text_input("Type your current mood or emotion (e.g., 'I feel sad')")

if user_input:
    with st.spinner("Analyzing your mood... 🍽️"):
        emotion = detect_emotion(user_input)
        food = recommend_food(emotion)
        tip = recommend_wellness(emotion)

    st.success(f"🧠 I sense you’re feeling **{emotion.capitalize()}**.")
    st.markdown(f"### 🍲 How about some **{food.title()}**?")
    image = get_food_image(food)
    if image:
        st.image(image, caption=f"{food.title()}", use_container_width=True)

    st.info(f"💡 Wellness Tip: {tip}")

    st.caption("⚠️ This is not a medical advice app. If you feel persistently low, consider talking to a professional.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Helpful 👍"):
            log_interaction(user_input, emotion, food, tip, "helpful")
            st.toast("Glad it helped! 🌸")
    with col2:
        if st.button("Not helpful 👎"):
            log_interaction(user_input, emotion, food, tip, "not helpful")
            st.toast("Thanks! I’ll improve my suggestions.")

# --------------------- Footer ------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Made with ❤️ by Sreekar — Powered by Transformers, Streamlit, and Pixabay API.")
