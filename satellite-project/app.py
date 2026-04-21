import streamlit as st
import requests
import pandas as pd
import random
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt

# -------- CONFIG (MUST BE FIRST STREAMLIT COMMAND) --------
st.set_page_config(page_title="Satellite Organization System", layout="wide")

# -------- API --------
API_SEND = "https://49tvo7zd99.execute-api.ap-south-1.amazonaws.com/send-message"
API_GET  = "https://49tvo7zd99.execute-api.ap-south-1.amazonaws.com/get-message"

# -------- AUTO REFRESH --------
st_autorefresh(interval=10000, key="refresh")

# -------- FETCH DATA FIRST --------
high = medium = low = 0
messages = []

try:
    response = requests.get(API_GET)

    if response.status_code == 200:
        messages = response.json()

        for msg in messages:
            if msg["priority"] == "HIGH":
                high += 1
            elif msg["priority"] == "MEDIUM":
                medium += 1
            else:
                low += 1
    else:
        st.error("❌ API Error")

except Exception as e:
    st.error(f"❌ Connection Error: {e}")

# -------- UI STYLE --------
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #0a0f2c, #000000);
    color: white;
}
.stApp {
    background-image: url("https://images.unsplash.com/photo-1446776811953-b23d57bd21aa");
    background-size: cover;
}
</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
st.markdown("""
<h1 style='text-align:center; color:white;'>
🛰️ SATELLITE ORGANIZATION MONITORING SYSTEM
</h1>
<p style='text-align:center; color:lightgray;'>
Real-Time Automated Fault Detection
</p>
<hr>
""", unsafe_allow_html=True)

# -------- ALERT CARDS --------
c1, c2, c3 = st.columns(3)

c1.markdown(f"""
<div style='background:#ff4b4b;padding:15px;border-radius:10px;color:white;text-align:center;'>
🚨 <b>{high} Critical Alerts</b>
</div>
""", unsafe_allow_html=True)

c2.markdown(f"""
<div style='background:#ffa500;padding:15px;border-radius:10px;color:white;text-align:center;'>
⚠️ <b>{medium} Warnings</b>
</div>
""", unsafe_allow_html=True)

c3.markdown(f"""
<div style='background:#28a745;padding:15px;border-radius:10px;color:white;text-align:center;'>
ℹ️ <b>{low} Normal</b>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -------- MAIN LAYOUT --------
left, right = st.columns([1, 2])

# -------- LEFT PANEL --------
with left:
    st.subheader("🛰️ Control Panel")

    if st.button("🚀 Run System Simulation"):
        auto_messages = [
            "Satellite communication failed",
            "Battery level low",
            "Orbit deviation detected",
            "Signal lost from satellite",
            "Temperature warning",
            "System running normally"
        ]

        msg = random.choice(auto_messages)

        requests.post(API_SEND, json={"message": msg})
        st.success("✅ Auto alert generated")

# -------- RIGHT PANEL --------
with right:
    st.subheader("📡 Live Organization Alerts")

    dept_filter = st.selectbox(
        "Department Filter",
        ["All", "Communication", "Power", "Navigation", "Monitoring"]
    )

    for msg in messages:
        if dept_filter == "All" or msg["department"] == dept_filter:

            color = "#ff4b4b" if msg["priority"]=="HIGH" else "#ffa500" if msg["priority"]=="MEDIUM" else "#28a745"

            st.markdown(f"""
            <div style='background:{color};padding:12px;border-radius:8px;margin-bottom:10px;color:white;'>
            <b>[{msg['department']}]</b> {msg['message']} <br>
            ⏰ {msg['time']}
            </div>
            """, unsafe_allow_html=True)

# -------- CHART --------
st.markdown("---")
st.subheader("📊 System Analytics")

fig, ax = plt.subplots()
ax.pie(
    [high, medium, low],
    labels=["HIGH", "MEDIUM", "LOW"],
    autopct='%1.1f%%'
)
st.pyplot(fig)
