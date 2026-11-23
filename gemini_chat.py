import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

TEAM_MEMBERS = [
    "Mehran",
    "Ansh Raj Verma",
    "Anshuman Tiwari",
    "Piyush Parmar",
]

SYSTEM_INSTRUCTION = (
    "You are CyberShield AI, a sharp, friendly, and practical cybersecurity peer "
    "created by Mehran, Ansh Raj Verma, Anshuman Tiwari, and Piyush Parmar. "
    "Always reply naturally in Hinglish (natural mix of Hindi and English written in Roman/Latin script) "
    "or friendly Indian English. Keep answers clear, direct, and helpful. "
    "When a user reports any incident, hack, or fraud, always provide numbered action steps (1, 2, 3...) "
    "and include Indian helplines/portals like 1930, cybercrime.gov.in, or ceir.gov.in when relevant."
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


def _pick_model(client: Groq) -> str:
    preferred = [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "gemma2-9b-it",
        "qwen/qwen3-32b",
    ]
    try:
        models = client.models.list().data or []
        ids = [m.id for m in models if getattr(m, "id", None)]
        for p in preferred:
            if p in ids:
                return p
        for m_id in ids:
            low = m_id.lower()
            if not any(skip in low for skip in ["whisper", "guard", "tts", "embed", "audio", "vision", "safeguard"]):
                return m_id
    except Exception:
        pass
    return "llama-3.1-8b-instant"


def _clean_messages(messages: list[dict]) -> list[dict]:
    cleaned = []
    for m in messages:
        role = m.get("role")
        content = (m.get("content") or "").strip()
        if role in {"system", "user", "assistant"} and content:
            cleaned.append({"role": role, "content": content})
    return cleaned


def _call_groq(messages: list[dict], max_tokens: int = 1500, temperature: float = 0.5) -> str:
    api_key = get_groq_api_key()
    if not api_key:
        return (
            "⚠️ **API Key Missing:** Streamlit Cloud Secrets ya `.env` mein `GROQ_API_KEY` nahi mila. "
            "Please `GROQ_API_KEY = \"gsk_...\"` add karein."
        )

    safe_messages = _clean_messages(messages)
    try:
        client = Groq(api_key=api_key)
        model_name = _pick_model(client)
        response = client.chat.completions.create(
            model=model_name,
            messages=safe_messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return (response.choices[0].message.content or "").strip()
    except Exception as e:
        return f"⚠️ **Groq Error:** {str(e)}"


def detect_intent(user_text: str) -> str:
    text = (user_text or "").strip().lower()

    if any(k in text for k in ["team", "member", "members", "who made", "created by", "who amde", "bnaya", "banaya", "developer"]):
        return "team"

    if any(k in text for k in ["how you can help", "what can you do", "features", "madad", "help karo"]):
        return "help"

    sos_triggers = [
        "hacked", "hack", "scam", "fraud", "blackmail", "sextortion", "threat", "leak",
        "sim swap", "stolen phone", "lost phone", "identity theft", "aadhaar", "ransomware",
        "paise kat", "unauthorized transaction", "compromised", "virus", "malware", "sos"
    ]
    if any(k in text for k in sos_triggers):
        return "sos"

    if "http://" in text or "https://" in text or "www." in text or "scan url" in text:
        return "url"

    if "password" in text and any(k in text for k in ["check", "strength", "strong", "weak", "score", "test"]):
        return "password"

    if any(k in text for k in ["sms", "message", "whatsapp msg", "kyc msg", "lottery", "suspicious msg"]):
        return "message"

    return "chat"


def generate_incident_steps(incident_text: str) -> str:
    prompt = f"""
    User ne yeh cyber incident ya attack report kiya hai: "{incident_text}".
    Hinglish mein natural, calm aur clear reply do:
    1. Ek line ka reassuring context.
    2. Numbered immediate action steps (1, 2, 3...).
    3. India reporting helpline & portal (1930 / cybercrime.gov.in / ceir.gov.in) agar applicable ho.
    4. Ek short prevention tip future ke liye.
    """
    return _call_groq(
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
        temperature=0.3,
    )


def ask_gemini(history: list[dict], new_message: str) -> str:
    messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for msg in history:
        role = "user" if msg.get("role") == "user" else "assistant"
        content = (msg.get("content") or "").strip()
        if content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": new_message})

    return _call_groq(messages=messages, max_tokens=1500, temperature=0.6)
