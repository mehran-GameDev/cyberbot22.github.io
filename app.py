import streamlit as st
from detectors import check_message, check_password, scan_url
from gemini_chat import (
    TEAM_MEMBERS,
    ask_gemini,
    detect_intent,
    generate_incident_steps,
    wants_hindi,
)

st.set_page_config(
    page_title="CyberShield AI | Cybersecurity Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    .stApp {
        background: radial-gradient(circle at top right, #10192d 0%, #080d19 45%, #040711 100%);
        color: #f1f5f9;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1120px;
    }

    .cyber-hero {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.9) 0%, rgba(15, 23, 42, 0.75) 100%);
        border: 1px solid rgba(0, 210, 255, 0.28);
        border-radius: 18px;
        padding: 22px 28px;
        margin-bottom: 24px;
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
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.4px;
        color: #ffffff;
        margin: 0 0 6px 0;
    }
    .hero-sub {
        font-size: 16px;
        font-weight: 700;
        color: #7dd3fc;
        margin: 0;
    }

    .cyber-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #38bdf8;
        border-radius: 14px;
        padding: 20px 24px;
        margin: 14px 0;
        font-size: 17px;
        font-weight: 600;
        line-height: 1.7;
        color: #f8fafc;
    }

    .thinking-box {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        background: rgba(14, 165, 233, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 14px;
        padding: 12px 18px;
        margin: 8px 0 14px 0;
        color: #e0f2fe;
        font-weight: 800;
        font-size: 15.5px;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.15);
    }
    .thinking-dots {
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .thinking-dots span {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #38bdf8;
        box-shadow: 0 0 8px #38bdf8;
        animation: cyberPulse 1.2s infinite ease-in-out;
    }
    .thinking-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }
    .thinking-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }
    @keyframes cyberPulse {
        0%, 80%, 100% {
            transform: scale(0.65);
            opacity: 0.45;
        }
        40% {
            transform: scale(1.2);
            opacity: 1;
        }
    }

    .risk-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 15px;
        letter-spacing: 0.4px;
        text-transform: uppercase;
    }
    .risk-high {
        background: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.45);
    }
    .risk-mod {
        background: rgba(234, 179, 8, 0.2);
        color: #facc15;
        border: 1px solid rgba(234, 179, 8, 0.45);
    }
    .risk-low {
        background: rgba(34, 197, 94, 0.2);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.45);
    }

    [data-testid="stSidebar"] {
        background-color: #070c18 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        font-weight: 700 !important;
    }

    .sidebar-helpline-card {
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(244, 63, 94, 0.35);
        border-radius: 12px;
        padding: 14px 16px;
        margin-top: 14px;
        font-weight: 700;
    }
    .sidebar-helpline-card h4 {
        margin: 0 0 8px 0;
        color: #fb7185;
        font-size: 14px;
        font-weight: 800;
        text-transform: uppercase;
    }

    [data-testid="stChatMessage"] {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] li {
        font-size: 17px !important;
        font-weight: 700 !important;
        line-height: 1.7 !important;
        color: #f8fafc !important;
    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #0d1527 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        padding: 12px 14px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 10px !important;
        padding: 8px 22px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_thinking(placeholder, label: str = "CyberShield AI is thinking"):
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


def format_team_reply(hindi: bool = False) -> str:
    lines = "\n".join(f"**{i}. {name}**" for i, name in enumerate(TEAM_MEMBERS, 1))
    if hindi:
        return f"**CyberShield AI Team Members:**\n{lines}"
    return f"**Meet the CyberShield AI Team:**\n{lines}"


def format_capabilities_reply(hindi: bool = False) -> str:
    if hindi:
        return (
            "**Main CyberShield AI hoon — aapka friendly cyber buddy! Yahan main kya-kya kar sakta hoon:**\n"
            "**1. Friendly Smart Chat:** Cyber safety, tech, aur security sawalon par aaram se baat karein.\n"
            "**2. Fake / Phishing URL Scanner:** Suspicious links scan karke risk level dekhein.\n"
            "**3. Password Strength Checker:** Password score aur strong banane ke tips paayein.\n"
            "**4. Suspicious Message Detector:** Urgent/scam messages aur risky links pakdein.\n"
            "**5. AI + Offline SOS Response:** Hack, fraud, ya blackmail ke waqt step-by-step action plan."
        )
    return (
        "**Hey! I am CyberShield AI — your friendly cybersecurity buddy. Here is how I can help:**\n"
        "**1. Friendly Smart Chat:** Ask any cybersecurity, privacy, or tech questions.\n"
        "**2. Fake URL Scanner:** Check links for phishing patterns, risky TLDs, or raw IPs.\n"
        "**3. Password Strength Checker:** Test password strength and get instant upgrade tips.\n"
        "**4. Suspicious Message Detector:** Spot urgency traps, scam wording, and risky links.\n"
        "**5. Smart SOS Response:** Get clear step-by-step action plans for hacks or scams."
    )


if "mode" not in st.session_state:
    st.session_state.mode = "Auto Chat"
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "**Hey there! I am CyberShield AI — your cybersecurity buddy.** "
                "**Ask me anything, check a URL, password, or suspicious message, or tell me if something went wrong for step-by-step SOS help.**"
            ),
        }
    ]

with st.sidebar:
    st.markdown("## **🛡️ CyberShield AI**")
    st.markdown("**AI + Offline Fallback Assistant**")
    st.session_state.mode = st.radio(
        "**Select Mode**",
        ["Auto Chat", "URL Scanner", "Password Check", "Message Check", "SOS Incident Guide", "Team Info"],
    )
    st.markdown(
        """
        <div class="sidebar-helpline-card">
            <h4><b>🚨 Emergency Helplines (India)</b></h4>
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
        <div class="hero-title"><b>🛡️ CyberShield AI Assistant</b></div>
        <p class="hero-sub"><b>Smart SOS Guidance • URL Scanner • Password Audit • Message Check • Hybrid AI/Offline Chat</b></p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.mode == "URL Scanner":
    url_in = st.text_input("**Enter URL to scan**", placeholder="https://example.com")
    if st.button("**Scan URL**") and url_in:
        res = scan_url(url_in)
        pill = get_risk_pill(res["risk"])
        details = "<br>".join(f"<b>• {f}</b>" for f in res["flags"]) or "<b>• No obvious suspicious patterns found.</b>"
        st.markdown(
            f"<div class='cyber-card'><b>Risk Level:</b> {pill}<br><br>{details}</div>",
            unsafe_allow_html=True,
        )

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

elif st.session_state.mode == "SOS Incident Guide":
    st.markdown("### **🚨 Incident Response & Emergency Action Plan**")
    st.markdown("**Select a cyber crime category or describe what happened to generate step-by-step actions.**")

    incident_options = [
        "Instagram / Social Media Account Hacked",
        "UPI / Bank Fraud (Money Deducted)",
        "WhatsApp Video Call Blackmail / Sextortion",
        "Fake Job / Part-Time Telegram Task Scam",
        "Lost or Stolen Mobile Phone (Risk of SIM Abuse)",
        "Identity Theft / PAN or Aadhaar Misuse",
        "Ransomware / Device Locked by Virus",
        "Fake Courier / Customs Parcel Fraud",
        "Other Custom Emergency...",
    ]

    selected_incident = st.selectbox("**What happened?**", incident_options)
    custom_desc = ""
    if selected_incident == "Other Custom Emergency...":
        custom_desc = st.text_input("**Describe your situation briefly:**")

    target_incident = custom_desc if selected_incident == "Other Custom Emergency..." else selected_incident

    if st.button("**Generate Step-by-Step Action Plan**", type="primary"):
        if target_incident.strip():
            anim_box = st.empty()
            show_thinking(anim_box, "Preparing emergency action steps")
            guide = generate_incident_steps(target_incident, hindi=False)
            anim_box.empty()
            st.markdown(
                f"<div class='cyber-card'><b>{guide.replace(chr(10), '<br>')}</b></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<div class='cyber-card'><b>Please describe your situation first.</b></div>", unsafe_allow_html=True)

elif st.session_state.mode == "Team Info":
    st.markdown(
        f"<div class='cyber-card'><b>{format_team_reply(False).replace(chr(10), '<br>')}</b></div>",
        unsafe_allow_html=True,
    )

if st.session_state.mode == "Auto Chat":
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(f"**{m['content']}**")

    prompt = st.chat_input("Chat freely, paste a link, or describe an incident...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f"**{prompt}**")

        hindi_mode = wants_hindi(prompt)
        intent = detect_intent(prompt)
        lower_p = prompt.strip().lower()

        with st.chat_message("assistant"):
            anim_box = st.empty()
            if intent == "team":
                reply = format_team_reply(hindi=hindi_mode)
            elif lower_p in {"how you can help me", "how can you help me", "what can you do", "help"}:
                reply = format_capabilities_reply(hindi=hindi_mode)
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
                parts = prompt.strip().split()
                candidate = parts[-1] if len(parts) > 1 else ""
                r = check_password(candidate)
                reply = (
                    f"**Password Strength: {r['level']} ({r['score']}/100)**\n"
                    + (
                        "\n".join(f"**- {t}**" for t in r["tips"])
                        if r["tips"]
                        else "**- Strong password! You can also test passwords in the Password Check mode.**"
                    )
                )
            elif intent == "sos":
                show_thinking(anim_box, "Analyzing threat & preparing SOS steps")
                reply = generate_incident_steps(prompt, hindi=hindi_mode)
            else:
                show_thinking(anim_box, "CyberShield AI is thinking")
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
