import re

TEAM_MEMBERS = [
    "Mehran",
    "Ansh Raj Verma",
    "Anshuman Tiwari",
    "Piyush Parmar",
]


def is_hindi_or_hinglish(text: str) -> bool:
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
            "**Offline Smart SOS — UPI / Bank Fraud Action Plan:**\n"
            "**1. Freeze Immediately:** Open your banking app, UPI app, or call your bank helpline to block/freeze your card, UPI, or account right away.\n"
            "**2. Call 1930:** In India, call National Cyber Crime Helpline **1930** immediately or report at **cybercrime.gov.in**.\n"
            "**3. Save Evidence:** Keep transaction IDs, UTR numbers, fraudster UPI/phone details, and screenshots safe.\n"
            "**4. Bank Complaint:** Visit your bank branch with a written complaint and take a stamped receiving copy.\n"
            "**Tip:** Never share OTP, PIN, or CVV to reverse a payment."
        )

    if any(k in s for k in ["insta", "instagram", "facebook", "gmail", "google", "hack", "account", "password"]):
        return (
            "**Offline Smart SOS — Account Hacked Action Plan:**\n"
            "**1. Reset Password:** Use your official recovery email or registered phone number to reset your password immediately.\n"
            "**2. Log Out All Sessions:** Go to security/login activity settings and sign out from all unknown devices.\n"
            "**3. Enable 2FA:** Turn on Two-Factor Authentication using an authenticator app.\n"
            "**4. Warn Contacts:** Tell friends and followers not to click links or send money if they get messages from your account.\n"
            "**Tip:** Also secure your linked email account first so attackers cannot reset your password again."
        )

    if any(k in s for k in ["blackmail", "sextortion", "video call", "threat", "leak"]):
        return (
            "**Offline Smart SOS — Blackmail / Threat Action Plan:**\n"
            "**1. Do Not Pay:** Do not send money—paying scammers usually leads to higher demands.\n"
            "**2. Preserve Proof:** Save screenshots, profile links, chat history, and phone numbers without deleting evidence.\n"
            "**3. Report Immediately:** File a complaint at **cybercrime.gov.in**, call **1930** if financial extortion is involved, or contact local cyber police.\n"
            "**4. Tighten Privacy:** Lock down social media profiles, restrict who can message/call you, and inform a trusted adult/family member.\n"
            "**Tip:** Avoid engaging in video calls with unknown accounts."
        )

    if any(k in s for k in ["job", "task", "telegram", "part time", "part-time", "investment", "trading"]):
        return (
            "**Offline Smart SOS — Fake Job / Task Scam Action Plan:**\n"
            "**1. Stop Paying:** Do not deposit any more money for tasks, registration, taxes, or withdrawals.\n"
            "**2. Block & Save Proof:** Keep payment receipts, UTRs, chat logs, and group/username details.\n"
            "**3. Report:** Call **1930** or file a report at **cybercrime.gov.in**, and alert your bank if money was transferred.\n"
            "**Tip:** Real jobs do not ask you to pay money to earn."
        )

    if any(k in s for k in ["phone", "mobile", "stolen", "lost", "sim"]):
        return (
            "**Offline Smart SOS — Lost / Stolen Phone Action Plan:**\n"
            "**1. Block SIM:** Contact your mobile operator immediately to block your SIM card.\n"
            "**2. Block IMEI:** Submit a request on **ceir.gov.in** to block the lost/stolen device.\n"
            "**3. Lock / Erase Data:** Use Google Find My Device or Apple iCloud to lock the phone or protect personal data.\n"
            "**4. Protect Bank & UPI:** Alert your bank and disable/block UPI/cards linked to that number.\n"
            "**Tip:** Keep your IMEI number and purchase bill safely recorded."
        )

    return (
        "**Offline Smart SOS — General Cyber Incident Plan:**\n"
        "**1. Disconnect:** Turn off Wi-Fi and mobile data on the affected device immediately.\n"
        "**2. Secure Accounts:** Change passwords for email, banking, and social accounts from a clean device.\n"
        "**3. Clean Device:** Uninstall suspicious apps/files and run a trusted security scan.\n"
        "**4. Report:** In India, call **1930** or report at **cybercrime.gov.in**.\n"
        "**Tip:** Keep backups and turn on 2FA across important accounts."
    )


def offline_chat_reply(user_text: str) -> str:
    low = user_text.strip().lower()
    hindi = is_hindi_or_hinglish(user_text)

    if any(k in low for k in ["team", "member", "members", "who made", "created by", "bnaya", "banaya"]):
        members = "\n".join(f"**{i}. {m}**" for i, m in enumerate(TEAM_MEMBERS, 1))
        return f"**CyberShield AI Team:**\n{members}"

    if any(k in low for k in ["how you can help", "how can you help", "what can you do", "features", "help"]):
        if hindi:
            return (
                "**Main CyberShield AI hoon (Offline Smart Mode Active):**\n"
                "**1. URL Scan:** Suspicious links check karein.\n"
                "**2. Password Check:** Password strength aur tips dekhein.\n"
                "**3. Message Check:** Scam/urgent messages pehchanein.\n"
                "**4. SOS Guide:** Hack, fraud, blackmail, ya lost phone ke steps paayein."
            )
        return (
            "**I am CyberShield AI (Offline Smart Mode Active):**\n"
            "**1. URL Scanner:** Check suspicious links for phishing signs.\n"
            "**2. Password Check:** Rate password strength and get upgrade tips.\n"
            "**3. Message Check:** Spot scam language, urgent traps, and risky links.\n"
            "**4. SOS Guide:** Get step-by-step action plans for hacks, scams, or fraud."
        )

    if "phishing" in low:
        if hindi:
            return (
                "**Phishing Kya Hai:**\n"
                "**-** Fake website, urgent message, ya nakli link ke zariye password, OTP, ya bank details churane ka attack.\n"
                "**-** Hamesha domain spelling check karein aur unknown links par login na karein."
            )
        return (
            "**What is Phishing:**\n"
            "**-** A cyber attack that uses fake login pages, urgent messages, or lookalike links to steal passwords, OTPs, or banking info.\n"
            "**-** Always verify the official website address and avoid logging in from unexpected links."
        )

    if any(k in low for k in ["2fa", "two factor", "otp", "password", "strong password"]):
        return (
            "**Password & Account Safety:**\n"
            "**-** Use a unique **12+ character** password for each account.\n"
            "**-** Turn on **Two-Factor Authentication (2FA)** (an authenticator app is stronger than SMS).\n"
            "**-** Never share **OTP, PIN, CVV, or passwords** with anyone."
        )

    if any(k in low for k in ["hi", "hello", "hey", "namaste"]):
        if hindi:
            return "**Namaste! API quota abhi limit par hai, isliye main Offline Smart Mode mein hoon. Aap URL, password, message, ya SOS guide aaram se use kar sakte hain.**"
        return "**Hey! Live AI API quota is currently unavailable, so I am running in Offline Smart Mode. You can still scan URLs, test passwords, check messages, and view SOS guides!**"

    if hindi:
        return (
            "**Offline Smart Mode Active:** Abhi Gemini API quota limit par hai ya connect nahi ho pa raha, isliye main built-in cybersecurity guides se madad kar raha hoon.\n"
            "**-** Link check karne ke liye **URL Scanner** ya URL bhejein.\n"
            "**-** Password check karne ke liye **Password Check** mode use karein.\n"
            "**-** Fraud/hack ke liye **SOS Incident Guide** dekhein ya **1930** / **cybercrime.gov.in** par sampark karein."
        )

    return (
        "**Offline Smart Mode Active:** Live AI API quota is currently exhausted or unreachable, so I am responding using built-in cybersecurity rules and guides.\n"
        "**-** Paste a link or open **URL Scanner** to inspect URLs.\n"
        "**-** Open **Password Check** to test password strength.\n"
        "**-** Open **SOS Incident Guide** for step-by-step emergency actions, or call **1930** / visit **cybercrime.gov.in** in India."
    )
