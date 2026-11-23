import re


def scan_url(url: str) -> dict:
    clean_url = (url or "").strip()
    if not clean_url:
        return {"url": "", "risk": "Low", "flags": ["No URL provided"]}

    lower_url = clean_url.lower()
    if not re.match(r"^https?://", lower_url):
        lower_url = "http://" + lower_url

    flags = []

    if lower_url.startswith("http://"):
        flags.append("Uses unencrypted HTTP instead of HTTPS")
    if re.search(r"https?://\d{1,3}(?:\.\d{1,3}){3}", lower_url):
        flags.append("Uses a raw IP address instead of a proper domain name")
    if re.search(r"\.(xyz|top|click|tk|ml|ga|cf|live|gq|work)(/|$|\?)", lower_url):
        flags.append("Uses a high-risk or free TLD often seen in scams")
    if re.search(r"\.(pdf|doc|docx|zip|rar|exe|apk|msi)($|\?)", lower_url):
        flags.append("Points directly to a downloadable or executable file")
    if re.search(
        r"https?://[^/\s]*(login|verify|update|bank|kyc|reward|free|claim|secure)[^/\s]*\.(com|in|org|net)",
        lower_url,
    ):
        flags.append("Domain contains common phishing or reward-lure keywords")
    if clean_url.count("-") >= 3:
        flags.append("Contains multiple hyphens (often used in lookalike domains)")
    if len(clean_url) > 100:
        flags.append("Unusually long URL")

    risk = "High" if len(flags) >= 2 else "Moderate" if len(flags) == 1 else "Low"
    return {"url": clean_url, "risk": risk, "flags": flags}


def check_password(password: str) -> dict:
    pwd = password or ""
    tips = []
    common_weak = {
        "123456", "12345678", "123456789", "password", "password123",
        "admin", "qwerty", "letmein", "abc123", "iloveyou", "india123",
    }

    if not pwd:
        return {"score": 0, "level": "Weak", "tips": ["Please enter a password to check."]}

    if pwd.lower() in common_weak:
        return {
            "score": 5,
            "level": "Very Weak",
            "tips": [
                "This is a very common password and can be guessed easily.",
                "Use a unique password or passphrase with at least 12 characters.",
            ],
        }

    score = 0
    has_lower = bool(re.search(r"[a-z]", pwd))
    has_upper = bool(re.search(r"[A-Z]", pwd))
    has_digit = bool(re.search(r"\d", pwd))
    has_symbol = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/~`]", pwd))
    variety_count = sum([has_lower, has_upper, has_digit, has_symbol])

    if len(pwd) >= 12:
        score += 35
    elif len(pwd) >= 8:
        score += 20
    else:
        tips.append("Make it at least 12 characters long.")

    if has_lower and has_upper:
        score += 25
    else:
        tips.append("Mix both uppercase (A-Z) and lowercase (a-z) letters.")

    if has_digit:
        score += 20
    else:
        tips.append("Add at least one number (0-9).")

    if has_symbol:
        score += 20
    else:
        tips.append("Include special symbols like @, #, $, or %.")

    # Penalize low character variety (e.g., all digits or all letters)
    if variety_count <= 1:
        score = min(score, 25)
        tips.append("Avoid using only one type of character (such as only numbers or only letters).")

    if re.search(r"(.)\1{2,}", pwd):
        score = max(0, score - 15)
        tips.append("Avoid repeating the same character three or more times in a row.")

    score = min(100, max(0, score))
    level = "Strong" if score >= 80 else "Moderate" if score >= 50 else "Weak"
    return {"score": score, "level": level, "tips": tips}


def check_message(text: str) -> dict:
    clean_text = (text or "").strip()
    if not clean_text:
        return {"risk": "Low", "signals": [], "links": []}

    lower_msg = clean_text.lower()
    signals = []

    urgency_phrases = [
        "urgent", "immediately", "suspended", "blocked", "account blocked",
        "kyc", "expire", "expired", "winner", "won", "lottery", "cashback",
        "refund", "customs", "parcel", "fine", "last warning", "verify now",
    ]
    matched_terms = []
    for phrase in urgency_phrases:
        pattern = r"\b" + r"\s+".join(re.escape(w) for w in phrase.split()) + r"\b"
        if re.search(pattern, lower_msg):
            matched_terms.append(phrase)

    if matched_terms:
        signals.append(f"Urgency or scam keywords found: {', '.join(matched_terms[:4])}")

    links = re.findall(r"https?://\S+|www\.\S+", clean_text)
    if links:
        signals.append(f"Contains {len(links)} link(s) — verify independently before clicking")

    if re.search(r"\b(otp|pin|cvv|upi|password)\b", lower_msg):
        signals.append("Mentions sensitive details (OTP, PIN, CVV, UPI, or password)")

    risk = "High" if len(signals) >= 2 else "Moderate" if len(signals) == 1 else "Low"
    return {"risk": risk, "signals": signals, "links": links}
