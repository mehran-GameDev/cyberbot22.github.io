import re
from gemini_chat import TEAM_MEMBERS


def _is_hindi_or_hinglish(text: str) -> bool:
    if re.search(r"[\u0900-\u097F]", text):
        return True
    low = text.lower()
    if any(p in low for p in ["hindi me", "hindi mein", "speak in hindi", "talk in hindi"]):
        return True
    hinglish_words = {
        "kya", "kaise", "hai", "hain", "mera", "meri", "mere", "karo", "karna",
        "batao", "bataiye", "chahiye", "nahi", "nhi", "aur", "kuch", "sab", "yeh", "woh"
    }
    return len(set(re.findall(r"[a-z]+", low)) & hinglish_words) >= 2


def offline_sos_guide(scenario: str) -> str:
    s = scenario.lower()
    if any(k in s for k in ["upi", "bank", "money", "fraud", "paise", "transaction", "payment"]):
        return (
            "**Offline SOS Mode — UPI / Bank Fraud Action Plan:**\n"
            "**1. Freeze Immediately:** Banking app, UPI app, ya bank helpline se card/account/UPI turant block ya freeze karein.\n"
            "**2. Call 1930:** India mein National Cyber Crime Helpline **1930** par immediately call karein ya **cybercrime.gov.in** par complaint darj karein.\n"
            "**3. Save Proof:** Transaction ID, UTR number, fraudster UPI/phone number, aur screenshots safe rakhein.\n"
            "**4. Bank Visit:** Bank branch mein written application dein aur receiving copy lein."
        )
    if any(k in s for k in ["insta", "instagram", "facebook", "gmail", "google", "hack", "account", "password"]):
        return (
            "**Offline SOS Mode — Account Hacked Action Plan:**\n"
            "**1. Password Reset:** Official recovery email ya registered phone number se password turant badlein.\n"
            "**2. Kick Out Sessions:** Security settings mein jaakar **Log out of all devices / active sessions** karein.\n"
            "**3. Turn On 2FA:** Authenticator app ya strong Two-Factor Authentication on karein.\n"
            "**4. Alert Contacts:** Friends ko bata dein ke aapke account se aane wale kisi suspicious link ya money request par bharosa na karein."
        )
    if any(k in s for k in ["blackmail", "sextortion", "video call", "threat", "leak"]):
        return (
            "**Offline SOS Mode — Blackmail / Threat Action Plan:**\n"
            "**1. Do Not Pay:** Scammers ko paise bilkul na bhejein—paise dene se demand aur badhti hai.\n"
            "**2. Block & Preserve Evidence:** Chat/call logs, profile links, aur numbers ke screenshots/recordings safe rakhein.\n"
            "**3. Report Immediately:** **cybercrime.gov.in** par report karein aur zaroorat pade to **1930** / local cyber cell se sampark karein.\n"
            "**4. Lock Privacy:** Social media aur WhatsApp privacy settings tight karein."
        )
    if any(k in s for k in ["phone", "mobile", "stolen", "lost", "sim"]):
        return (
            "**Offline SOS Mode — Lost / Stolen Phone Action Plan:**\n"
            "**1. Block SIM:** Telecom operator ko call karke SIM turant block karwayein.\n"
            "**2. CEIR Portal:** **ceir.gov.in** par IMEI block karne ki request daalein.\n"
            "**3. Remote Lock / Wipe:** Google Find My Device / Apple iCloud se device lock ya data secure karein.\n"
            "**4. Bank & UPI Alert:** Linked bank accounts aur UPI apps ko secure/block karein."
        )

    return (
        "**Offline SOS Mode — General Cyber Incident Plan:**\n"
        "**1. Disconnect:** Suspicious device ka internet (Wi-Fi / mobile data) turant band karein.\n"
        "**2. Secure Accounts:** Email, banking, aur social passwords kisi safe device se change karein.\n"
        "**3. Remove Threats:** Unknown apps/files hatayein aur trusted security scan run karein.\n"
        "**4. Report:** India mein **1930** par call karein ya **cybercrime.gov.in** par report file karein."
    )


def offline_chat_reply(user_text: str) -> str:
    low = user_text.strip().lower()
    hindi = _is_hindi_or_hinglish(user_text)

    if any(k in low for k in ["team", "member", "members", "who made", "created by", "bnaya", "banaya"]):
        members = "\n".join(f"**{i}. {m}**" for i, m in enumerate(TEAM_MEMBERS, 1))
        return f"**CyberShield AI Team (Offline Mode):**\n{members}"

    if "phishing" in low:
        if hindi:
            return (
                "**Phishing Kya Hai (Offline Guide):**\n"
                "**-** Fake link, urgent dar, ya nakli login page ke zariye aapka password, OTP, ya bank details churane ka tarika.\n"
                "**-** Hamesha URL spelling check karein aur unknown links par login na karein."
            )
        return (
            "**What is Phishing (Offline Guide):**\n"
            "**-** An attack that uses fake websites, urgent messages, or lookalike links to steal passwords, OTPs, or banking info.\n"
            "**-** Always verify the exact domain name and never enter credentials from unexpected links."
        )

    if any(k in low for k in ["2fa", "two factor", "otp", "password tips", "strong password"]):
        return (
            "**Account & Password Safety (Offline Guide):**\n"
            "**-** Use **12+ character** unique passwords for every account.\n"
            "**-** Enable **2FA** (authenticator app preferred over SMS).\n"
            "**-** Never share **OTP, PIN, CVV, or password** with anyone."
        )

    if any(k in low for k in ["hi", "hello", "hey", "namaste"]):
        if hindi:
            return "**Namaste! API quota abhi limit par hai, isliye main Offline Smart Mode mein hoon. Aap URL, password, message, ya SOS guide aaram se use kar sakte hain.**"
        return "**Hey! API quota is currently limited, so I am running in Offline Smart Mode. You can still use the URL scanner, password checker, message analyzer, and SOS guides!**"

    if hindi:
        return (
            "**Offline Smart Mode Active:** Abhi AI API quota khatam ya unavailable hai, isliye main pre-built cybersecurity rules aur guides se madad kar raha hoon.\n"
            "**-** Link check karne ke liye **URL Scanner** ya link paste karein.\n"
            "**-** Password check karne ke liye **Password Check** mode use karein.\n"
            "**-** Fraud/hack ke liye **SOS Incident Guide** ya `1930` / `cybercrime.gov.in` dekhein."
        )

    return (
        "**Offline Smart Mode Active:** The live AI API quota is currently exhausted or unreachable, so I am answering using built-in cybersecurity rules and guides.\n"
        "**-** Paste a URL or use **URL Scanner** to check links.\n"
        "**-** Use **Password Check** to test password strength.\n"
        "**-** Use **SOS Incident Guide** for emergency steps, or contact **1930** / **cybercrime.gov.in** in India."
    )
