# 🔮 AI Horoscope Predictor

An AI-powered horoscope generator built with **Python**, **Streamlit**, and the **Google Gemini API**.
Enter your birth details and get a personalized, AI-generated horoscope covering love,
career, health, and more.

## Tech stack
- Python 3.10+
- [Streamlit](https://streamlit.io/) — web app framework
- [Google Gemini API](https://ai.google.dev/) — AI text generation (`google-genai` SDK)

## Run it locally
1. Clone this repo and open the folder in a terminal.
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and paste in your
   own Gemini API key (get one free at https://aistudio.google.com/app/apikey).
5. Run the app:
   ```
   streamlit run app.py
   ```

## Deploy for free
Push this repo to GitHub, then deploy it on
[Streamlit Community Cloud](https://streamlit.io/cloud) — add your `GEMINI_API_KEY`
under app Settings → Secrets instead of committing the real secrets file.

## Disclaimer
This app generates horoscopes for entertainment purposes only.
