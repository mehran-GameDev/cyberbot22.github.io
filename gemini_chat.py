import os
from pathlib import Path
import re
from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

LLAMA_MODEL = "llama-3.3-70b-versatile"

TEAM_MEMBERS = [
    "Mehran",
    "Ansh Raj Verma",
    "Anshuman Tiwari",
    "Piyush Parmar",
]

SYSTEM_INSTRUCTION = (
    "You are CyberShield AI, a friendly, reassuring, and smart cybersecurity peer "
    "created by Mehran, Ansh Raj Verma, Anshuman Tiwari, and Piyush Parmar. "
    "Always speak in natural, friendly English by default. Only switch to Hindi or Hinglish "
    "if the user explicitly asks to speak in Hindi or speaks in Hindi/Hinglish first. "
    "When a user reports any incident, attack, fraud, or hack, give a complete, clear, "
    "numbered step-by-step emergency action plan without cutting off mid-sentence, "
    "including official Indian helplines such as 1930, cybercrime.gov.in, and ceir.gov.in where relevant."
)


def get_groq_api_key() -> str | None:
    key = os.getenv("GROQ_API_KEY")
    if key and key.strip() and key.strip() != "your_groq_api_key_here":
        return key.strip()
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            val = str(st.secrets["GROQ_API_KEY"]).strip()
            if val and val != "your_groq_api_key_here":
                return val
    except Exception:
        pass
    return None


def get_client() -> Groq:
    api_key = get_groq_api_key()
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Add it to .env or Streamlit Secrets.")
    return Groq(api_key=api_key)


def wants_hindi(user_text: str) -> bool:
    if re.search(r"[\u0900-\u097F]", user_text):
        return True
    low = user_text.lower()
    if any(p in low for p in ["speak in hindi", "talk in hindi", "hindi me baat", "hindi mein baat", "hindi karo"]):
        return True
    hinglish_words = {
        "kya", "kaise", "hai", "hain", "mera", "meri", "mere", "karo", "karna",
        "batao", "bataiye", "chahiye", "nahi", "nhi", "aur", "kuch", "sab", "yeh", "woh"
    }
    tokens = set(re.findall(r"[a-z]+", low))
    return len(tokens & hinglish_words) >= 2


def detect_intent(user_text: str) -> str:
    text = user_text.strip().lower()

    if any(k in text for k in ["team", "member", "members", "who made", "created by", "bnaya", "banaya", "kaun hai"]):
        return "team"

    if any(k in text for k in ["how you can help", "how can you help", "what can you do", "features", "your purpose"]):
        return "chat"

    sos_triggers = [
        "hacked", "hack", "scam", "fraud", "blackmail", "sextortion", "threat", "leak",
        "sim swap", "stolen phone", "lost phone", "identity theft", "aadhaar", "ransomware",
        "paise kat", "unauthorized transaction", "compromised", "virus", "malware", "sos"
    ]
    if any(k in text for k in sos_triggers):
        return "sos"

    if "http://" in text or "https://" in text or "www." in text or "scan url" in text or "link safe" in text:
        return "url"

    if "password" in text and any(k in text for k in ["check", "strength", "strong", "weak", "score", "test"]):
        return "password"

    if any(k in text for k in ["sms", "message", "whatsapp", "kyc", "lottery", "suspicious msg"]):
        return "message"

    return "chat"


def generate_incident_steps(incident_text: str, hindi: bool = False) -> str:
    client = get_client()
    lang_prompt = (
        "Respond in clear, natural Hinglish or simple Hindi so it is easy to read and complete."
        if hindi
        else "Respond in clear, friendly English."
    )

    prompt = f"""
    A user reported this cybersecurity incident or emergency: "{incident_text}".
    {lang_prompt}

    Provide a complete, clear response:
    1. One calm, reassuring opening line.
    2. Numbered immediate action steps (1, 2, 3...) tailored to this exact situation.
    3. Official support / reporting channels (including 1930, cybercrime.gov.in, and ceir.gov.in in India when applicable).
    4. One short tip to prevent this in the future.
    """

    chat_completion = client.chat.completions.create(
        model=LLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2048,
        temperature=0.35,
    )
    return (chat_completion.choices[0].message.content or "Could not generate guidance.").strip()


def ask_gemini(history: list[dict], new_message: str) -> str:
    client = get_client()
    messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]

    for msg in history:
        role = "user" if msg.get("role") == "user" else "assistant"
        content = msg.get("content", "")
        if content:
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": new_message})

    chat_completion = client.chat.completions.create(
        model=LLAMA_MODEL,
        messages=messages,
        max_tokens=2048,
        temperature=0.55,
    )
    return (chat_completion.choices[0].message.content or "Could not generate a response.").strip()
