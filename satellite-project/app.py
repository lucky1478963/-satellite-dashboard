import streamlit as st
import requests
import json
import random
from streamlit_autorefresh import st_autorefresh

API = "https://49tvo7zd99.execute-api.ap-south-1.amazonaws.com"

st.set_page_config(layout="wide")

st.title("🛰️ Satellite Organization Monitoring System")

# AUTO REFRESH
st_autorefresh(interval=3000)

# -------- ADMIN PANEL --------
st.sidebar.title("⚙️ Admin Panel")

admin = st.sidebar.checkbox("Enable Admin")

if admin:
    st.sidebar.subheader("Add Rule")

    k = st.sidebar.text_input("Keyword")
    p = st.sidebar.selectbox("Priority", ["HIGH", "MEDIUM", "LOW"])
    t = st.sidebar.number_input("Auto Resolve Time", 1, 60)

    if st.sidebar.button("Add Rule"):
        requests.post(API + "/send-message", json={
            "type": "rule",
            "keyword": k,
            "priority": p,
            "time": t
        })
        st.sidebar.success("Rule Added")

# -------- SIMULATION --------
if st.button("Simulate Alert"):
    msgs = [
        "Satellite communication failed",
        "Battery level low",
        "Temperature warning",
        "Orbit deviation detected"
    ]
    msg = random.choice(msgs)

    requests.post(API + "/send-message", json={"message": msg})
    st.success("Alert Generated")
    st.rerun()

# -------- FETCH --------
res = requests.get(API + "/get-message")

if res.status_code == 200:
    data = res.json()

    if isinstance(data, dict) and "body" in data:
        messages = json.loads(data["body"])
    else:
        messages = data

    for m in messages:
        color = "red" if m["priority"]=="HIGH" else "orange" if m["priority"]=="MEDIUM" else "green"

        st.markdown(f"""
        <div style='background:{color};padding:10px;margin:5px;border-radius:8px;color:white;'>
        <b>[{m['department']}]</b> {m['message']}<br>
        Priority: {m['priority']} | Status: {m['status']}<br>
        ⏰ {m['time']}
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("API Error")
