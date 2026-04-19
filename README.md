# Mood-Based Food Recommender (MoodMeal)

This project is a mood-aware food recommender that suggests meals based on a user's current mood and preferences. It combines a simple chatbot interface with a recommendation engine and collects feedback to improve suggestions over time.

## Project Structure

- `APP_streamlit.py` – Streamlit app entrypoint for the MoodMeal UI.
- `app.py` – Core backend logic / model code used by the app.
- `Mood_Meal_chatbot.ipynb` – Jupyter notebook for experimentation and prototyping.
- `moodmeal_feedback.csv` – Collected user feedback data (ratings/comments).
- `Requirements/` – Notes or design/requirements documents.
- `MoodMeal_Project_Enhancement_Plan.pdf` – High-level enhancement and design plan.

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/rika1089/mood-based-food-recommender.git
   cd mood-based-food-recommender
   ```

2. **Create and activate a virtual environment (optional but recommended)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**

   ```bash
   streamlit run APP_streamlit.py
   ```

   Then open the local URL printed in the terminal (usually `http://localhost:8501`).

## Requirements

Dependencies are listed in `requirements.txt` (to be cleaned from `requirments.txt.txt`). At a minimum, the project uses:

- `streamlit` for the web UI
- `pandas` for handling feedback data
- `scikit-learn` or similar libraries if you are using ML-based recommendations

## Future Enhancements

- Improve mood detection and recommendation quality.
- Add user authentication and history tracking.
- Visualize feedback data and recommendation performance.
- Deploy the app to a cloud platform (e.g., Streamlit Cloud, Render, or Heroku).
