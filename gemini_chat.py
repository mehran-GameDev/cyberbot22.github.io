import os
from pathlib import Path
import re
from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

PREFERRED_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "llama3-8b-8192",
    "llama3-70b-8192",
]

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


def get_client() -> Groq | None:
    api_key = get_groq_api_key()
    if not api_key:
        return None
    return Groq(api_key=api_key)


def _clean_messages(messages: list[dict]) -> list[dict]:
    cleaned = []
    for m in messages:
        role = m.get("role")
        content = (m.get("content") or "").strip()
        if role in {"system", "user", "assistant"} and content:
            cleaned.append({"role": role, "content": content})
    return cleaned


def _run_llm(messages: list[dict], max_tokens: int = 1500, temperature: float = 0.5) -> str | None:
    client = get_client()
    if client is None:
        return None

    safe_messages = _clean_messages(messages)
    for model_name in PREFERRED_MODELS:
        try:
            res = client.chat.completions.create(
                model=model_name,
                messages=safe_messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            text = (res.choices[0].message.content or "").strip()
            if text:
                return text
        except Exception:
            continue
    return None


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

    if any(k in text for k in ["team", "member", "members", "who made", "created by", "who amde", "bnaya", "banaya", "kaun hai"]):
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

    llm_reply = _run_llm(
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
        temperature=0.35,
    )
    if llm_reply:
        return llm_reply

    return (
        "**Emergency Action Steps:**\n"
        "**1. Secure Accounts:** Change passwords immediately and enable 2FA.\n"
        "**2. Block / Freeze:** If money or phone is involved, block cards/UPI/SIM right away.\n"
        "**3. Report in India:** Call **1930** or visit **cybercrime.gov.in** (and **ceir.gov.in** for lost/stolen phones)."
    )


def ask_gemini(history: list[dict], new_message: str) -> str:
    messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for msg in history:
        role = "user" if msg.get("role") == "user" else "assistant"
        content = (msg.get("content") or "").strip()
        if content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": new_message})

    llm_reply = _run_llm(messages=messages, max_tokens=1500, temperature=0.55)
    if llm_reply:
        return llm_reply

    return (
        "**CyberShield AI:** Live AI response is temporarily unavailable right now. "
        "You can still use **URL Scanner**, **Password Check**, **Message Check**, or call **1930** / visit **cybercrime.gov.in** for cyber help in India."
    )
