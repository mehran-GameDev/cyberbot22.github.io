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
    "You are CyberShield AI, a clear, friendly, and practical cybersecurity assistant "
    "created by Mehran, Ansh Raj Verma, Anshuman Tiwari, and Piyush Parmar. "
    "Always reply in natural, clear English. "
    "When a user reports any incident, hack, or fraud, always provide numbered immediate action steps (1, 2, 3...) "
    "and include relevant Indian helplines and portals such as 1930, cybercrime.gov.in, and ceir.gov.in."
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
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "qwen/qwen3-32b",
        "gemma2-9b-it",
    ]
    blocked_keywords = [
        "whisper", "guard", "tts", "embed", "audio",
        "vision", "safeguard", "orpheus", "playai"
    ]
    allowed_families = ["llama", "qwen", "gemma", "deepseek", "mistral"]

    try:
        models = client.models.list().data or []
        ids = [m.id for m in models if getattr(m, "id", None)]
        for p in preferred:
            if p in ids:
                return p
        for m_id in ids:
            low = m_id.lower()
            if any(bad in low for bad in blocked_keywords):
                continue
            if any(fam in low for fam in allowed_families):
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
            "⚠️ **API Key Missing:** `GROQ_API_KEY` was not found in `.env` or Streamlit Cloud Secrets. "
            'Add `GROQ_API_KEY = "gsk_..."` and restart the app.'
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

    if any(
        k in text
        for k in [
            "team",
            "member",
            "members",
            "who made",
            "created by",
            "who amde",
            "developer",
        ]
    ):
        return "team"

    if any(k in text for k in ["how you can help", "what can you do", "features", "help"]):
        return "help"

    sos_triggers = [
        "hacked",
        "hack",
        "scam",
        "fraud",
        "blackmail",
        "sextortion",
        "threat",
        "leak",
        "sim swap",
        "stolen phone",
        "lost phone",
        "identity theft",
        "aadhaar",
        "ransomware",
        "unauthorized transaction",
        "compromised",
        "virus",
        "malware",
        "sos",
    ]
    if any(k in text for k in sos_triggers):
        return "sos"

    if "http://" in text or "https://" in text or "www." in text or "scan url" in text:
        return "url"

    if "password" in text and any(
        k in text for k in ["check", "strength", "strong", "weak", "score", "test"]
    ):
        return "password"

    if any(k in text for k in ["sms", "message", "whatsapp", "kyc", "lottery", "suspicious msg"]):
        return "message"

    return "chat"


def generate_incident_steps(incident_text: str) -> str:
    prompt = f"""
    A user reported this cybersecurity incident or emergency: "{incident_text}".
    Respond in clear, calm, and practical English:
    1. One reassuring opening line.
    2. Numbered immediate action steps (1, 2, 3...).
    3. Official Indian reporting channels and helplines (1930, cybercrime.gov.in, ceir.gov.in) when applicable.
    4. One short prevention tip for the future.
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

    return _call_groq(messages=messages, max_tokens=1500, temperature=0.55)
