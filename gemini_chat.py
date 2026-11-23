import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Sabse stable aur fast Groq free model
PRIMARY_MODEL = "llama-3.1-8b-instant"

TEAM_MEMBERS = [
    "Mehran",
    "Ansh Raj Verma",
    "Anshuman Tiwari",
    "Piyush Parmar",
]

SYSTEM_INSTRUCTION = (
    "You are CyberShield AI, a sharp, friendly, and practical cybersecurity peer "
    "created by Mehran, Ansh Raj Verma, Anshuman Tiwari, and Piyush Parmar. "
    "Respond naturally in casual Hinglish (natural mix of Hindi and English written in Latin/English script) "
    "or friendly Indian English. Keep it direct, crisp, and no gyaan. "
    "When a user asks for incident help or SOS, always give direct numbered action steps (1, 2, 3...) "
    "and include relevant Indian authorities like 1930, cybercrime.gov.in, or ceir.gov.in."
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
            "Please check karein."
        )

    try:
        client = Groq(api_key=api_key)
        safe_messages = _clean_messages(messages)
        
        response = client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=safe_messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return (response.choices[0].message.content or "").strip()
    except Exception as e:
        # Fallback to 70b if 8b has issues
        try:
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=_clean_messages(messages),
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return (response.choices[0].message.content or "").strip()
        except Exception as e2:
            return f"⚠️ **Groq Error:** {str(e2)}"


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
    Hinglish mein natural, calm aur crisp reply do:
    1. Ek line ka reassuring context.
    2. Exact action steps numbered list (1, 2, 3...) mein.
    3. India specific reporting portal & helpline (1930 / cybercrime.gov.in / ceir.gov.in).
    4. One prevention rule for future.
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
