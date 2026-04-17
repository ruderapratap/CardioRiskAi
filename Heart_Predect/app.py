import streamlit as st
import pandas as pd
import joblib
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CardioRisk AI",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Palette ────────────────────────────────────────────────────────────────────
# B6F5AB  – mint green  (light accent / badges)
# 48753E  – forest green (primary / buttons / headings)
# DCEBB7  – pale sage   (card surfaces / borders)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Outfit:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background-color: #f5faf0;
    color: #1a2e14;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 5vw, 3.2rem);
    color: #48753E;
    margin: 0;
    line-height: 1.1;
}
.hero-title span { color: #1a2e14; }
.hero-sub {
    color: #5a7a52;
    font-size: 0.92rem;
    margin-top: 0.5rem;
    font-weight: 300;
    letter-spacing: 0.05em;
}
.hero-badge {
    display: inline-block;
    margin-top: 0.9rem;
    padding: 0.28rem 1rem;
    border-radius: 999px;
    background: #B6F5AB;
    color: #1a3d14;
    font-size: 0.7rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    font-weight: 600;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1.5px solid #DCEBB7 !important;
    margin: 1.2rem 0 !important;
}

/* ── Section labels ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #48753E;
    margin: 1.4rem 0 0.7rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1.5px;
    background: linear-gradient(to right, #B6F5AB, transparent);
}

/* ── Widget labels ── */
label[data-testid="stWidgetLabel"] p {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #2d4a26 !important;
}

/* ── Select / Input ── */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-color: #DCEBB7 !important;
    border-radius: 8px !important;
    color: #1a2e14 !important;
}
div[data-baseweb="input"] > div > input {
    background-color: #ffffff !important;
    border-color: #DCEBB7 !important;
    border-radius: 8px !important;
    color: #1a2e14 !important;
}

/* ── Slider track ── */
div[data-testid="stSlider"] .stSlider > div > div > div {
    background: #48753E !important;
}

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: #ffffff;
    border: 1.5px solid #DCEBB7;
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
}
div[data-testid="metric-container"] label {
    color: #5a7a52 !important;
    font-size: 0.72rem !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #1a2e14 !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}

/* ── Primary button ── */
div.stButton > button {
    width: 100%;
    padding: 0.85rem 2rem;
    border-radius: 10px;
    background: #48753E;
    color: #ffffff;
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    border: none;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s, box-shadow 0.2s;
    box-shadow: 0 4px 14px rgba(72,117,62,0.28);
    margin-top: 0.6rem;
}
div.stButton > button:hover {
    background: #3a5f32;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(72,117,62,0.38);
}
div.stButton > button:active { transform: translateY(0); }

/* ── Result boxes ── */
.result-high {
    background: #fff5f5;
    border: 1.5px solid #e05252;
    border-radius: 14px;
    padding: 2rem 1.5rem;
    text-align: center;
    margin-top: 1rem;
}
.result-low {
    background: linear-gradient(135deg, #edfbe9, #f3fdf0);
    border: 1.5px solid #48753E;
    border-radius: 14px;
    padding: 2rem 1.5rem;
    text-align: center;
    margin-top: 1rem;
}
.result-icon  { font-size: 2.6rem; margin-bottom: 0.5rem; }
.result-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.55rem;
    margin: 0.3rem 0 0.6rem;
}
.result-title.high { color: #c0392b; }
.result-title.low  { color: #48753E; }
.result-desc {
    font-size: 0.87rem;
    color: #5a7a52;
    max-width: 380px;
    margin: 0 auto;
    line-height: 1.7;
}
.conf-pill {
    display: inline-block;
    margin-top: 0.8rem;
    padding: 0.3rem 1rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
}
.conf-pill.high { background: #fde8e8; color: #c0392b; }
.conf-pill.low  { background: #B6F5AB; color: #1a3d14; }

/* ── Footer ── */
.footer {
    text-align: center;
    color: #8aaa82;
    font-size: 0.7rem;
    padding: 2.5rem 0 1rem;
    letter-spacing: 0.04em;
}

div[data-testid="stSpinner"] p { color: #48753E !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_artifacts():
    model         = joblib.load("knn_heart.pkl")
    scaler        = joblib.load("scaler.pkl")
    expected_cols = joblib.load("columns.pkl")
    return model, scaler, expected_cols


def build_input(age, sex, chest_pain, resting_bp, cholesterol,
                fasting_bs, resting_ecg, max_hr, exercise_angina,
                oldpeak, st_slope, expected_cols):
    raw = {
        'Age':         age,
        'RestingBP':   resting_bp,
        'Cholesterol': cholesterol,
        'FastingBS':   fasting_bs,
        'MaxHR':       max_hr,
        'Oldpeak':     oldpeak,
        f'Sex_{sex}':                        1,
        f'ChestPainType_{chest_pain}':       1,
        f'RestingECG_{resting_ecg}':         1,
        f'ExerciseAngina_{exercise_angina}': 1,
        f'ST_Slope_{st_slope}':              1,
    }
    return pd.DataFrame([raw]).reindex(columns=expected_cols, fill_value=0)


# ── Load model ─────────────────────────────────────────────────────────────────
try:
    model, scaler, expected_cols = load_artifacts()
    model_loaded = True
except Exception as e:
    model_loaded = False
    load_error = str(e)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">Cardio<span>Risk</span> AI</div>
    <div class="hero-sub">KNN-powered heart disease risk prediction</div>
    <span class="hero-badge">🫀 Clinical Decision Support Tool</span>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.error(
        f"⚠️ Could not load model files: `{load_error}`\n\n"
        "Make sure `knn_heart.pkl`, `scaler.pkl`, and `columns.pkl` "
        "are in the same directory as this script."
    )
    st.stop()

st.markdown("---")

# ── Two-column form ────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-label">👤 Patient Demographics</div>', unsafe_allow_html=True)
    age = st.slider("Age", 18, 100, 45, help="Patient's age in years")
    sex = st.selectbox("Biological Sex", ["M", "F"],
                       format_func=lambda x: "Male" if x == "M" else "Female")
    chest_pain = st.selectbox(
        "Chest Pain Type", ["ATA", "NAP", "TA", "ASY"],
        format_func=lambda x: {
            "ATA": "ATA — Atypical Angina",
            "NAP": "NAP — Non-Anginal Pain",
            "TA":  "TA  — Typical Angina",
            "ASY": "ASY — Asymptomatic",
        }[x],
    )
    exercise_angina = st.selectbox(
        "Exercise-Induced Angina", ["Y", "N"],
        format_func=lambda x: "Yes" if x == "Y" else "No",
    )

    st.markdown('<div class="section-label">📊 Vitals & Lab Results</div>', unsafe_allow_html=True)
    resting_bp  = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 120)
    cholesterol = st.number_input("Serum Cholesterol (mg/dL)", 100, 603, 200)
    fasting_bs  = st.selectbox(
        "Fasting Blood Sugar > 120 mg/dL", [0, 1],
        format_func=lambda x: "Yes (> 120 mg/dL)" if x == 1 else "No (≤ 120 mg/dL)",
    )

with col_right:
    st.markdown('<div class="section-label">❤️ Cardiac Measurements</div>', unsafe_allow_html=True)
    max_hr  = st.slider("Maximum Heart Rate Achieved", 60, 220, 150,
                        help="Peak HR during stress test")
    oldpeak = st.slider("Oldpeak — ST Depression", 0.0, 6.0, 1.0, step=0.1,
                        help="ST depression induced by exercise relative to rest")
    resting_ecg = st.selectbox(
        "Resting ECG Result", ["Normal", "ST", "LVH"],
        format_func=lambda x: {
            "Normal": "Normal",
            "ST":     "ST — T-wave abnormality",
            "LVH":    "LVH — Left Ventricular Hypertrophy",
        }[x],
    )
    st_slope = st.selectbox(
        "ST Segment Slope (Peak Exercise)", ["Up", "Flat", "Down"],
        format_func=lambda x: f"{x}sloping",
    )

    st.markdown('<div class="section-label">📋 Input Summary</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    m1.metric("Age",         f"{age} yrs")
    m2.metric("Sex",         "Male" if sex == "M" else "Female")
    m3, m4 = st.columns(2)
    m3.metric("BP",          f"{resting_bp} mmHg")
    m4.metric("Cholesterol", f"{cholesterol} mg/dL")
    m5, m6 = st.columns(2)
    m5.metric("Max HR",      f"{max_hr} bpm")
    m6.metric("Oldpeak",     f"{oldpeak}")

# ── Predict button ─────────────────────────────────────────────────────────────
st.markdown("---")
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    predict_clicked = st.button("🔍  Run Cardiac Risk Assessment",
                                use_container_width=True)

if predict_clicked:
    with st.spinner("Analysing cardiovascular indicators…"):
        time.sleep(0.7)

    input_df   = build_input(age, sex, chest_pain, resting_bp, cholesterol,
                             fasting_bs, resting_ecg, max_hr, exercise_angina,
                             oldpeak, st_slope, expected_cols)
    scaled     = scaler.transform(input_df)
    prediction = model.predict(scaled)[0]
    proba      = model.predict_proba(scaled)[0] if hasattr(model, "predict_proba") else None

    _, res_col, _ = st.columns([1, 3, 1])
    with res_col:
        if prediction == 1:
            prob_str = f"{proba[1]*100:.0f}% model confidence" if proba is not None else ""
            st.markdown(f"""
            <div class="result-high">
                <div class="result-icon">⚠️</div>
                <div class="result-title high">High Cardiac Risk Detected</div>
                {'<span class="conf-pill high">' + prob_str + '</span>' if prob_str else ''}
                <p class="result-desc">
                    The model indicates an <strong>elevated risk of heart disease</strong>
                    based on the provided values.<br><br>
                    This is a screening tool — please consult a cardiologist
                    for a full clinical evaluation.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            prob_str = f"{proba[0]*100:.0f}% model confidence" if proba is not None else ""
            st.markdown(f"""
            <div class="result-low">
                <div class="result-icon">✅</div>
                <div class="result-title low">Low Cardiac Risk</div>
                {'<span class="conf-pill low">' + prob_str + '</span>' if prob_str else ''}
                <p class="result-desc">
                    The model suggests a <strong>low risk of heart disease</strong>
                    based on the provided values.<br><br>
                    Maintain a healthy lifestyle and schedule regular check-ups
                    with your physician.
                </p>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    CardioRisk AI · Built with Streamlit & scikit-learn ·
    For educational purposes only — not a substitute for medical advice.<br>
    Model: K-Nearest Neighbours · Dataset: UCI Heart Disease
</div>
""", unsafe_allow_html=True)