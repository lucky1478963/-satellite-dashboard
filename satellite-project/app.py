import streamlit as st
import requests
import json
import random
from streamlit_autorefresh import st_autorefresh

API = "https://49tvo7zd99.execute-api.ap-south-1.amazonaws.com"

st.set_page_config(page_title="Satellite System", layout="wide")

# ------------------ 🌌 BACKGROUND STYLE ------------------
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Glass effect cards */
.card {
    background: rgba(0, 0, 0, 0.6);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: white;
}

/* Title */
.title {
    text-align: center;
    color: cyan;
    font-size: 36px;
    font-weight: bold;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: rgba(0,0,0,0.8);
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("<div class='title'>🛰️ Satellite Organization Monitoring System</div>", unsafe_allow_html=True)
st.markdown("---")

# ------------------ AUTO REFRESH ------------------
st_autorefresh(interval=3000)

# ------------------ SIDEBAR ADMIN ------------------
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

# ------------------ SIMULATION ------------------
if st.button("🚀 Simulate Alert"):
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

# ------------------ FETCH DATA ------------------
res = requests.get(API + "/get-message")

if res.status_code == 200:
    data = res.json()

    if isinstance(data, dict) and "body" in data:
        messages = json.loads(data["body"])
    else:
        messages = data

    st.subheader("📡 Live Alerts")

    for m in messages:
        color = "#ff4b4b" if m["priority"]=="HIGH" else "#ffa500" if m["priority"]=="MEDIUM" else "#28a745"

        st.markdown(f"""
        <div class="card" style="border-left: 6px solid {color};">
            <b>[{m['department']}]</b> {m['message']}<br>
            Priority: {m['priority']} | Status: {m['status']}<br>
            ⏰ {m['time']}
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("❌ API Error")
