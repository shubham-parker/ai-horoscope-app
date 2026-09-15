import os
from datetime import date
from typing import Optional

import streamlit as st
from google import genai

# ---------- Page setup ----------
st.set_page_config(
    page_title="AI Horoscope Predictor",
    page_icon="🔮",
    layout="centered",
)

# You can swap this for another Gemini model name if you like.
# "gemini-2.5-flash" is fast, cheap, and has a generous free tier.
MODEL_NAME = "gemini-3.5-flash"

ZODIAC_SIGNS = [
    ("Capricorn", (12, 22), (1, 19)),
    ("Aquarius", (1, 20), (2, 18)),
    ("Pisces", (2, 19), (3, 20)),
    ("Aries", (3, 21), (4, 19)),
    ("Taurus", (4, 20), (5, 20)),
    ("Gemini", (5, 21), (6, 20)),
    ("Cancer", (6, 21), (7, 22)),
    ("Leo", (7, 23), (8, 22)),
    ("Virgo", (8, 23), (9, 22)),
    ("Libra", (9, 23), (10, 22)),
    ("Scorpio", (10, 23), (11, 21)),
    ("Sagittarius", (11, 22), (12, 21)),
]


def get_zodiac_sign(day: int, month: int) -> str:
    """Work out the zodiac sign from a birth day and month."""
    for sign, start, end in ZODIAC_SIGNS:
        start_month, start_day = start
        end_month, end_day = end
        if start_month == month and day >= start_day:
            return sign
        if end_month == month and day <= end_day:
            return sign
    return "Capricorn"


def get_api_key() -> Optional[str]:
    """Look for the Gemini API key in Streamlit secrets, then env vars,
    then whatever the user typed into the sidebar."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key

    return st.session_state.get("manual_api_key")


def build_prompt(name, dob, tob, pob, zodiac, focus_areas) -> str:
    focus_text = ", ".join(focus_areas) if focus_areas else "general life"
    return f"""
You are an experienced, warm, and insightful astrologer.
Write a personalized horoscope for the person described below.

Name: {name}
Date of birth: {dob.strftime('%d %B %Y')}
Time of birth: {tob}
Place of birth: {pob if pob else "Not provided"}
Zodiac sign: {zodiac}
Areas of focus: {focus_text}

Write the horoscope with these sections, using short bold headers:
1. Overall Vibe (2-3 sentences)
2. Love & Relationships
3. Career & Finance
4. Health & Wellbeing
5. Lucky Color, Lucky Number, and Lucky Time of Day
6. One Piece of Advice for Today

Keep the tone positive, warm, and easy to read. Make it feel personal rather
than generic — weave in a couple of natural {zodiac} traits. Keep the whole
response under 300 words.
""".strip()


def generate_horoscope(client: genai.Client, prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text


# ---------- Sidebar ----------
st.sidebar.title("🔮 Settings")
st.sidebar.markdown("This app uses the **Google Gemini API** to write your horoscope.")

if not get_api_key():
    st.session_state["manual_api_key"] = st.sidebar.text_input(
        "Enter your Gemini API key",
        type="password",
        help="Get a free key at https://aistudio.google.com/app/apikey",
    )

st.sidebar.markdown("---")
st.sidebar.caption("Built with Python, Streamlit & Google Gemini API")

# ---------- Main UI ----------
st.title("🔮 AI Horoscope Predictor")
st.write("Enter your birth details below and get a personalized, AI-generated horoscope.")

with st.form("birth_details_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name", placeholder="e.g. Ninja")
        dob = st.date_input(
            "Date of Birth",
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            value=date(2000, 1, 1),
        )
    with col2:
        tob = st.time_input("Time of Birth (optional)")
        pob = st.text_input("Place of Birth", placeholder="e.g. Gurugram, India")

    focus_areas = st.multiselect(
        "What should your horoscope focus on?",
        ["Love", "Career", "Health", "Finance", "Family", "Travel"],
        default=["Love", "Career"],
    )

    submitted = st.form_submit_button("✨ Generate My Horoscope")

if submitted:
    api_key = get_api_key()
    if not name:
        st.warning("Please enter your name.")
    elif not api_key:
        st.error("Please add a Gemini API key in the sidebar to continue.")
    else:
        zodiac = get_zodiac_sign(dob.day, dob.month)
        st.success(f"Your zodiac sign is **{zodiac}** ✨")

        with st.spinner("Consulting the stars..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = build_prompt(name, dob, tob, pob, zodiac, focus_areas)
                horoscope_text = generate_horoscope(client, prompt)
                st.markdown("### Your Personalized Horoscope")
                st.write(horoscope_text)
            except Exception as e:
                st.error(f"Something went wrong while generating your horoscope: {e}")
