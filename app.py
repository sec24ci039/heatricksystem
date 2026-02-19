import streamlit as st
import pandas as pd
import numpy as np

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="AI Heatwave Intelligence",
    page_icon="🔥",
    layout="wide"
)

# -------------------------
# PREMIUM DARK THEME STYLE
# -------------------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 8px 32px 0 rgba(0, 0, 0, 0.3);
}

.big-number {
    font-size: 40px;
    font-weight: bold;
}

.risk-low { color: #00ff99; }
.risk-moderate { color: #ffcc00; }
.risk-high { color: #ff4d4d; }

</style>
""", unsafe_allow_html=True)

# -------------------------
# SAMPLE MODEL OUTPUTS
# (Replace with your real values)
# -------------------------
today_temp = 28.14
tomorrow_temp = 29.14
day_after_temp = 28.98

prob_tomorrow = 0.08
prob_day_after = 0.15

# -------------------------
# RISK LOGIC
# -------------------------
def risk_level(prob):
    if prob < 0.2:
        return "LOW", "risk-low"
    elif prob < 0.5:
        return "MODERATE", "risk-moderate"
    else:
        return "HIGH", "risk-high"

# -------------------------
# HEADER
# -------------------------
# -------------------------
# PREMIUM LUXURY HEADER
# -------------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">

<style>

.title {
    font-family: 'Orbitron', sans-serif;
    font-size: 50px;
    text-align: center;
    letter-spacing: 2px;
    margin-bottom: 8px;
    color: #F5F5DC;   /* Beige */
}

.subtitle {
    font-family: 'Playfair Display', serif;
    text-align: center;
    font-size: 20px;
    letter-spacing: 1px;
    color: #E6D5B8;   /* Soft champagne beige */
    opacity: 0.9;
}

</style>

<h1 class="title">AI Heatwave Intelligence Dashboard</h1>
<p class="subtitle">Smart Climate Risk Monitoring System</p>

""", unsafe_allow_html=True)

# -------------------------
# TEMPERATURE CARDS
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🌡 Today")
    st.markdown(f"<div class='big-number'>{today_temp:.2f}°C</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🌤 Tomorrow")
    st.markdown(f"<div class='big-number'>{tomorrow_temp:.2f}°C</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ☀ Day After")
    st.markdown(f"<div class='big-number'>{day_after_temp:.2f}°C</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.write("")

# -------------------------
# HEATWAVE RISK SECTION
# -------------------------
col4, col5 = st.columns(2)

# Tomorrow Risk
with col4:
    level, css_class = risk_level(prob_tomorrow)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🔥 Tomorrow Heatwave Risk")
    st.progress(prob_tomorrow)
    st.markdown(f"<h2 class='{css_class}'>{level}</h2>", unsafe_allow_html=True)
    st.markdown(f"Probability: {prob_tomorrow:.2%}")
    st.markdown("</div>", unsafe_allow_html=True)

# Day After Risk
with col5:
    level2, css_class2 = risk_level(prob_day_after)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🔥 Day After Heatwave Risk")
    st.progress(prob_day_after)
    st.markdown(f"<h2 class='{css_class2}'>{level2}</h2>", unsafe_allow_html=True)
    st.markdown(f"Probability: {prob_day_after:.2%}")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.write("")

# -------------------------
# TREND CHART
# -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 📈 30-Day Temperature Trend")

dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
temps = np.random.normal(30, 2, 30)

chart_data = pd.DataFrame({
    "Date": dates,
    "Temperature": temps
}).set_index("Date")

st.line_chart(chart_data)

st.markdown("</div>", unsafe_allow_html=True)
