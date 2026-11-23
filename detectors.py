import re


def scan_url(url: str) -> dict:
    clean_url = url.strip()
    lower_url = clean_url.lower()
    flags = []

    if not re.match(r"^https?://", lower_url):
        lower_url = "http://" + lower_url

    if lower_url.startswith("http://"):
        flags.append("Uses unencrypted HTTP instead of HTTPS")
    if re.search(r"https?://\d{1,3}(?:\.\d{1,3}){3}", lower_url):
        flags.append("Uses a raw IP address instead of a proper domain name")
    if re.search(r"\.(xyz|top|click|tk|ml|ga|cf|live|gq|work)(/|$|\?)", lower_url):
        flags.append("Uses a high-risk or free TLD often seen in scams")
    if re.search(r"\.(pdf|doc|docx|zip|rar|exe|apk|msi)($|\?)", lower_url):
        flags.append("Points directly to a downloadable or executable file")
    if re.search(r"(login|verify|update|bank|kyc|reward|free|claim|secure).*\.(com|in|org|net)", lower_url):
        flags.append("Contains common phishing or reward-lure keywords")
    if clean_url.count("-") >= 3:
        flags.append("Contains multiple hyphens (often used in lookalike domains)")
    if len(clean_url) > 85:
        flags.append("Unusually long URL")

    risk = "High" if len(flags) >= 2 else "Moderate" if len(flags) == 1 else "Low"
    return {"url": clean_url, "risk": risk, "flags": flags}


def check_password(password: str) -> dict:
    score = 0
    tips = []
    common_weak = {
        "123456", "12345678", "123456789", "password", "password123",
        "admin", "qwerty", "letmein", "abc123", "iloveyou", "india123"
    }

    if not password:
        return {"score": 0, "level": "Weak", "tips": ["Please enter a password to check."]}

    if password.lower() in common_weak:
        return {
            "score": 5,
            "level": "Very Weak",
            "tips": [
                "This is a very common password and can be guessed easily.",
                "Use a unique password or passphrase with at least 12 characters.",
            ],
        }

    if len(password) >= 12:
        score += 35
    elif len(password) >= 8:
        score += 20
    else:
        tips.append("Make it at least 12 characters long.")

    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 25
    else:
        tips.append("Mix both uppercase (A-Z) and lowercase (a-z) letters.")

    if re.search(r"\d", password):
        score += 20
    else:
        tips.append("Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/~`]", password):
        score += 20
    else:
        tips.append("Include special symbols like @, #, $, or %.")

    if re.search(r"(.)\1{2,}", password):
        score = max(0, score - 15)
        tips.append("Avoid repeating the same character three or more times in a row.")

    score = min(100, max(0, score))
    level = "Strong" if score >= 80 else "Moderate" if score >= 50 else "Weak"
    return {"score": score, "level": level, "tips": tips}


def check_message(text: str) -> dict:
    clean_text = text.strip()
    lower_msg = clean_text.lower()
    signals = []

    urgency_terms = [
        "urgent", "immediately", "suspended", "blocked", "account blocked",
        "kyc", "expire", "expired", "winner", "won", "lottery", "cashback",
        "refund", "customs", "parcel", "fine", "last warning", "verify now"
    ]
    matched_terms = [term for term in urgency_terms if term in lower_msg]
    if matched_terms:
        signals.append(f"Urgency or scam keywords found: {', '.join(matched_terms[:4])}")

    links = re.findall(r"https?://\S+|www\.\S+", clean_text)
    if links:
        signals.append(f"Contains {len(links)} link(s) — verify independently before clicking")

    if re.search(r"\b(otp|pin|cvv|upi|password)\b", lower_msg):
        signals.append("Mentions sensitive details (OTP, PIN, CVV, UPI, or password)")

    risk = "High" if len(signals) >= 2 else "Moderate" if len(signals) == 1 else "Low"
    return {"risk": risk, "signals": signals, "links": links}
