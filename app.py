import streamlit as st
from detectors import check_message, check_password, scan_url
from gemini_chat import (
    TEAM_MEMBERS,
    ask_gemini,
    detect_intent,
    generate_incident_steps,
)

st.set_page_config(
    page_title="CyberShield AI | Cybersecurity Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        overflow-x: hidden;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
        white-space: pre-wrap;
        word-break: break-word;
    }

    .stApp {
        background: radial-gradient(circle at top right, #10192d 0%, #080d19 45%, #040711 100%);
        color: #f1f5f9;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3.5rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
        max-width: 1120px;
    }

    .cyber-hero {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.92) 0%, rgba(15, 23, 42, 0.78) 100%);
        border: 1px solid rgba(0, 210, 255, 0.28);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 18px;
        box-shadow: 0 10px 30px -10px rgba(0, 210, 255, 0.18);
        position: relative;
        overflow: hidden;
    }
    .cyber-hero::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 5px; height: 100%;
        background: linear-gradient(180deg, #00d2ff 0%, #3a7bd5 100%);
        box-shadow: 0 0 12px #00d2ff;
    }
    .hero-title {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 4px 0;
        line-height: 1.2;
    }
    .hero-sub {
        font-size: 14.5px;
        font-weight: 600;
        color: #7dd3fc;
        margin: 0;
    }

    .cyber-card {
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #38bdf8;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 12px 0;
        font-size: 16px;
        font-weight: 600;
        line-height: 1.6;
        color: #f8fafc;
        overflow-wrap: anywhere;
    }

    .thinking-box {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: rgba(14, 165, 233, 0.14);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 12px;
        padding: 10px 15px;
        margin: 8px 0 14px 0;
        color: #e0f2fe;
        font-weight: 700;
        font-size: 14.5px;
    }
    .thinking-dots {
        display: inline-flex;
        gap: 4px;
    }
    .thinking-dots span {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #38bdf8;
        box-shadow: 0 0 8px #38bdf8;
        animation: cyberPulse 1.2s infinite ease-in-out;
    }
    .thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes cyberPulse {
        0%, 80%, 100% { transform: scale(0.65); opacity: 0.45; }
        40% { transform: scale(1.2); opacity: 1; }
    }

    .risk-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 13.5px;
        text-transform: uppercase;
    }
    .risk-high { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .risk-mod { background: rgba(234, 179, 8, 0.2); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.4); }
    .risk-low { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.4); }

    [data-testid="stSidebar"] {
        background-color: #070c18 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    .sidebar-helpline-card {
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(244, 63, 94, 0.35);
        border-radius: 10px;
        padding: 12px 14px;
        margin-top: 14px;
    }
    .sidebar-helpline-card h4 {
        margin: 0 0 6px 0;
        color: #fb7185;
        font-size: 13px;
        font-weight: 800;
        text-transform: uppercase;
    }

    [data-testid="stChatMessage"] {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] li {
        font-size: 15.5px !important;
        font-weight: 600 !important;
        line-height: 1.6 !important;
        color: #f8fafc !important;
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #0d1527 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 8px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        min-height: 44px;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem;
            padding-bottom: 5.5rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        }
        .hero-title { font-size: 20px; }
        .hero-sub { font-size: 13px; }
        .stButton>button { width: 100% !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_thinking(placeholder, label: str = "CyberShield AI analyzing"):
    placeholder.markdown(
        f"""
        <div class="thinking-box">
            <span>🛡️ <b>{label}</b></span>
            <div class="thinking-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_risk_pill(level: str) -> str:
    lvl = level.lower()
    if "high" in lvl or "very weak" in lvl:
        return f"<span class='risk-pill risk-high'><b>{level}</b></span>"
    if "mod" in lvl:
        return f"<span class='risk-pill risk-mod'><b>{level}</b></span>"
    return f"<span class='risk-pill risk-low'><b>{level}</b></span>"


def format_team_reply() -> str:
    lines = "\n".join(f"**{i}. {name}**" for i, name in enumerate(TEAM_MEMBERS, 1))
    return f"**CyberShield AI Team Members:**\n{lines}"


def format_help_reply() -> str:
    return (
        "**CyberShield AI Features:**\n"
        "**1. Smart Hinglish Chat:** Cyber safety, online privacy aur tech queries solve karta hai.\n"
        "**2. AI SOS Engine:** Kisi bhi online fraud ya hack par direct step-by-step action plan.\n"
        "**3. URL Scanner:** Phishing aur suspicious links detect karta hai.\n"
        "**4. Password Strength:** Password resiliency check aur upgrade recommendations.\n"
        "**5. Message Analyzer:** Fraud WhatsApp / SMS urgency messages check karta hai."
    )


if "mode" not in st.session_state:
    st.session_state.mode = "Auto Chat"
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "**Hey! Main CyberShield AI hoon — aapka cybersecurity peer.** "
                "Mujhse koi bhi doubt pucho, link check karvao, password test karo ya kisi hack/fraud par instant SOS help lo!"
            ),
        }
    ]

with st.sidebar:
    st.markdown("## **🛡️ CyberShield AI**")
    st.markdown("**Real-Time Threat Assistant**")
    st.session_state.mode = st.radio(
        "**Mode Select Karein**",
        ["Auto Chat", "SOS Incident Guide", "URL Scanner", "Password Check", "Message Check", "Team Info"],
    )
    st.markdown(
        """
        <div class="sidebar-helpline-card">
            <h4>🚨 Emergency Helplines (India)</h4>
            <div><b>Cyber Helpline: 1930</b></div>
            <div><b>Portal: cybercrime.gov.in</b></div>
            <div><b>Lost Phone: ceir.gov.in</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="cyber-hero">
        <div class="hero-title">🛡️ CyberShield AI Assistant</div>
        <p class="hero-sub">Live AI Incident Recovery • URL Inspector • Password Audit • Message Analysis</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Mobile quick switch
mode_options = ["Auto Chat", "SOS Incident Guide", "URL Scanner", "Password Check", "Message Check", "Team Info"]
quick_mode = st.selectbox(
    "Quick Switch",
    mode_options,
    index=mode_options.index(st.session_state.mode),
    label_visibility="collapsed",
)
if quick_mode != st.session_state.mode:
    st.session_state.mode = quick_mode
    st.rerun()

# ----------------- SOS INCIDENT GUIDE -----------------
if st.session_state.mode == "SOS Incident Guide":
    st.markdown("### **🚨 AI Emergency Incident Guide**")
    st.markdown("Incident select karein ya apna case likhein, CyberShield AI instant recovery steps batayega.")

    incident_library = [
        "UPI / Bank Fraud (Money Debited via Unauthorized Transaction)",
        "Instagram Account Hacked & Password / Email Changed",
        "WhatsApp Account Hijacked / Fake OTP Verification Scam",
        "WhatsApp Video Call Blackmail / Sextortion Extortion",
        "Fake Job / Part-Time Telegram Task & Investment Fraud",
        "Lost or Stolen Mobile Phone (Risk of SIM & UPI Misuse)",
        "Identity Theft / Aadhaar or PAN Card Exploitation",
        "Suspicious APK / Spyware / Unknown App Installed",
        "Ransomware Attack / PC Files Locked & Encrypted",
        "Clicked a Phishing Link & Entered Account Credentials",
        "Debit / Credit Card Cloning or Unauthorized ATM Withdrawal",
        "Fake Courier / Customs / FedEx Parcel Call Scam",
        "Fake Instant Loan App Harassment & Contact Blackmail",
        "Fake Tech Support / AnyDesk / TeamViewer Screen Share Scam",
        "Cyberbullying / Online Harassment / Defamation on Social Media",
        "Online Shopping / Fake Store Order & QR Code Scam",
        "Home Wi-Fi Router Compromised / Rogue Connected Devices",
        "Personal Email Leaked in Dark Web Data Breach",
        "Other Custom Emergency / Attack Scenario...",
    ]

    selected_incident = st.selectbox("**Select incident type:**", incident_library)

    if selected_incident == "Other Custom Emergency / Attack Scenario...":
        custom_input = st.text_area(
            "**Apna incident detail mein likhein:**",
            placeholder="Mere sath yeh hua, call aayi thi...",
        )
        target_incident = custom_input.strip()
    else:
        target_incident = selected_incident

    if st.button("**Generate AI Emergency Action Plan**", type="primary"):
        if target_incident:
            anim_box = st.empty()
            show_thinking(anim_box, "Emergency steps prepare ho rahe hain")
            ai_response = generate_incident_steps(target_incident)
            anim_box.empty()
            st.markdown(
                f"<div class='cyber-card'>{ai_response.replace(chr(10), '<br>')}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.warning("Pehle details provide karein.")

# ----------------- URL SCANNER -----------------
elif st.session_state.mode == "URL Scanner":
    url_in = st.text_input("**Enter URL to scan**", placeholder="https://example.com")
    if st.button("**Scan URL**") and url_in:
        res = scan_url(url_in)
        pill = get_risk_pill(res["risk"])
        details = "<br>".join(f"<b>• {f}</b>" for f in res["flags"]) or "<b>• No suspicious patterns found.</b>"
        st.markdown(
            f"<div class='cyber-card'><b>Risk Level:</b> {pill}<br><br>{details}</div>",
            unsafe_allow_html=True,
        )

# ----------------- PASSWORD CHECK -----------------
elif st.session_state.mode == "Password Check":
    pwd_in = st.text_input("**Enter password to test**", type="password")
    if st.button("**Check Strength**") and pwd_in:
        res = check_password(pwd_in)
        pill = get_risk_pill(res["level"])
        st.progress(res["score"] / 100)
        st.markdown(
            f"<div class='cyber-card'><b>Strength:</b> {pill} <b>({res['score']}/100)</b></div>",
            unsafe_allow_html=True,
        )
        for tip in res["tips"]:
            st.markdown(f"**- {tip}**")

# ----------------- MESSAGE CHECK -----------------
elif st.session_state.mode == "Message Check":
    msg_in = st.text_area("**Paste suspicious SMS / WhatsApp message**")
    if st.button("**Analyze Message**") and msg_in:
        res = check_message(msg_in)
        pill = get_risk_pill(res["risk"])
        details = "<br>".join(f"<b>• {s}</b>" for s in res["signals"]) or "<b>• No major scam signals detected.</b>"
        st.markdown(
            f"<div class='cyber-card'><b>Risk Level:</b> {pill}<br><br>{details}</div>",
            unsafe_allow_html=True,
        )

# ----------------- TEAM INFO -----------------
elif st.session_state.mode == "Team Info":
    st.markdown(
        f"<div class='cyber-card'><b>{format_team_reply().replace(chr(10), '<br>')}</b></div>",
        unsafe_allow_html=True,
    )

# ----------------- AUTO CHAT -----------------
elif st.session_state.mode == "Auto Chat":
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(f"**{m['content']}**")

    prompt = st.chat_input("Chat karein, link paste karein ya incident batayein...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f"**{prompt}**")

        intent = detect_intent(prompt)

        with st.chat_message("assistant"):
            anim_box = st.empty()
            if intent == "team":
                reply = format_team_reply()
            elif intent == "help":
                reply = format_help_reply()
            elif intent == "url":
                r = scan_url(prompt)
                reply = f"**URL Risk: {r['risk']}**\n" + (
                    "\n".join(f"**- {f}**" for f in r["flags"]) if r["flags"] else "**- No obvious red flags found.**"
                )
            elif intent == "message":
                r = check_message(prompt)
                reply = f"**Message Risk: {r['risk']}**\n" + (
                    "\n".join(f"**- {s}**" for s in r["signals"]) if r["signals"] else "**- No major scam keywords found.**"
                )
            elif intent == "password":
                candidate = prompt.strip().split()[-1]
                r = check_password(candidate)
                reply = f"**Password Strength: {r['level']} ({r['score']}/100)**\n" + (
                    "\n".join(f"**- {t}**" for t in r["tips"]) if r["tips"] else "**- Strong password!**"
                )
            elif intent == "sos":
                show_thinking(anim_box, "Emergency steps prepare ho rahe hain")
                reply = generate_incident_steps(prompt)
            else:
                show_thinking(anim_box, "CyberShield AI thinking")
                reply = ask_gemini(st.session_state.messages[:-1], prompt)

            anim_box.empty()
            st.markdown(f"**{reply}**")

        st.session_state.messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    import os
    import sys
    from streamlit.web import cli as stcli

    if os.environ.get("STREAMLIT_RUNNING") != "1":
        os.environ["STREAMLIT_RUNNING"] = "1"
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())
