import streamlit as st
import requests
import pandas as pd
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Organization System", layout="wide")

API_SEND = "https://49tvo7zd99.execute-api.ap-south-1.amazonaws.com/send-message"
API_GET  = "https://49tvo7zd99.execute-api.ap-south-1.amazonaws.com/get-message"

st_autorefresh(interval=5000, key="refresh")

# -------- LOGIN --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Organization Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()

# -------- UI --------
st.title("🛰️ Satellite Organization Monitoring System")

# -------- SIMULATION --------
if st.button("Simulate Alert"):
    msgs = [
        "Satellite communication failed",
        "Battery level low",
        "Orbit deviation detected",
        "Signal lost from satellite",
        "Temperature warning",
        "System running normally"
    ]

    msg = random.choice(msgs)
    requests.post(API_SEND, json={"message": msg})
    st.success("Alert Generated")
    st.rerun()

# -------- FETCH --------
res = requests.get(API_GET)

st.write("STATUS CODE:", res.status_code)
st.write("RAW RESPONSE:", res.text)

if res.status_code == 200:
    messages = res.json()

    high = medium = low = 0

    for m in messages:
        if m["priority"] == "HIGH":
            high += 1
        elif m["priority"] == "MEDIUM":
            medium += 1
        else:
            low += 1

    # -------- STATS --------
    c1, c2, c3 = st.columns(3)
    c1.metric("🚨 High", high)
    c2.metric("⚠️ Medium", medium)
    c3.metric("ℹ️ Low", low)

    st.markdown("---")

    # -------- DISPLAY --------
    for m in messages:
        color = "red" if m["priority"]=="HIGH" else "orange" if m["priority"]=="MEDIUM" else "green"

        st.markdown(f"""
        <div style='background:#222;padding:10px;border-radius:8px;margin-bottom:10px;color:white;'>
        <b>[{m['department']}]</b> {m['message']}<br>
        Priority: {m['priority']} |
        Status: <span style='color:{color}'>{m['status']}</span><br>
        ⏰ {m['time']}
        </div>
        """, unsafe_allow_html=True)

    # -------- CHART --------
    df = pd.DataFrame({
        "Priority": ["HIGH","MEDIUM","LOW"],
        "Count": [high, medium, low]
    })

    st.bar_chart(df.set_index("Priority"))

else:
    st.error("API error")
