import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from reportlab.pdfgen import canvas
import io

# ================= MODEL =================
model = joblib.load("fault_model.pkl")

# ================= PAGE CONFIG =================
st.set_page_config(page_title="⚡ Smart Grid SCADA System", layout="wide")

# ================= SESSION STATE =================
if "log" not in st.session_state:
    st.session_state.log = []

# ================= TITLE =================
st.title("⚡ FINAL BOSS SCADA - Smart Grid Monitoring System")
st.markdown("AI + Electrical Engineering Hybrid Fault Diagnosis System")

st.divider()

# ================= INPUT PANEL =================
col1, col2, col3, col4 = st.columns(4)

voltage = col1.number_input("Voltage (V)", value=230.0)
current = col2.number_input("Current (A)", value=10.0)
pf = col3.number_input("Power Factor", value=0.95)
frequency = col4.number_input("Frequency (Hz)", value=50.0)

# ================= PREDICTION =================
data = pd.DataFrame([[voltage, current, pf, frequency]],
                    columns=["Voltage", "Current", "PowerFactor", "Frequency"])

prediction = model.predict(data)[0]
confidence = np.max(model.predict_proba(data)[0]) * 100

# ================= ENGINEERING RULE ENGINE =================
health = 100

if pf < 0.65:
    prediction = "Power Factor Fault"
    severity = "CRITICAL"
    health -= 40

elif frequency < 48:
    prediction = "Grid Instability"
    severity = "CRITICAL"
    health -= 50

elif voltage > 260:
    prediction = "Over Voltage"
    severity = "HIGH"
    health -= 25

elif current > 25:
    prediction = "Over Load"
    severity = "HIGH"
    health -= 25

else:
    severity = "NORMAL"
    health -= 5

health = max(0, health)

# ================= DASHBOARD =================
st.subheader("📡 Control Room Dashboard")

c1, c2, c3 = st.columns(3)
c1.metric("⚡ Fault Type", prediction)
c2.metric("📊 Confidence", f"{confidence:.1f}%")
c3.metric("🏥 Health Index", f"{health}/100")

# ================= HEALTH GAUGE =================
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=health,
    title={'text': "Grid Health Score"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "cyan"},
        'steps': [
            {'range': [0, 40], 'color': "red"},
            {'range': [40, 70], 'color': "orange"},
            {'range': [70, 100], 'color': "green"}
        ]
    }
))

st.plotly_chart(fig, use_container_width=True)

# ================= TREND SNAPSHOT =================
st.subheader("📊 System Snapshot")

fig2 = go.Figure()

fig2.add_trace(go.Bar(name="Voltage", x=["V"], y=[voltage]))
fig2.add_trace(go.Bar(name="Current", x=["A"], y=[current]))

st.plotly_chart(fig2, use_container_width=True)

# ================= ALERT PANEL =================
st.subheader("🚨 System Alert")

if severity == "CRITICAL":
    st.error("🔴 CRITICAL SYSTEM ALERT - IMMEDIATE ACTION REQUIRED")
elif severity == "HIGH":
    st.warning("🟠 HIGH RISK DETECTED")
else:
    st.success("🟢 SYSTEM NORMAL")

# ================= EVENT LOG =================
st.subheader("📜 Event History")

st.session_state.log.append({
    "Time": datetime.now().strftime("%H:%M:%S"),
    "Voltage": voltage,
    "Current": current,
    "PF": pf,
    "Frequency": frequency,
    "Fault": prediction,
    "Health": health
})

df_log = pd.DataFrame(st.session_state.log)
st.dataframe(df_log, use_container_width=True)

# ================= PDF REPORT =================
def generate_pdf(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)

    c.drawString(100, 800, "SMART GRID SCADA REPORT")
    y = 750

    for item in data[-10:]:
        line = f"{item['Time']} | {item['Fault']} | Health:{item['Health']}"
        c.drawString(100, y, line)
        y -= 20

    c.save()
    buffer.seek(0)
    return buffer

if st.session_state.log:
    pdf = generate_pdf(st.session_state.log)

    st.download_button(
        "📄 Download SCADA Report",
        data=pdf,
        file_name="scada_report.pdf",
        mime="application/pdf"
    )

# ================= FOOTER =================
st.markdown("---")
st.caption("⚡ FINAL BOSS SCADA SYSTEM | AI + Electrical Engineering Hybrid")
