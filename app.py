import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import os
import numpy as np
import pandas as pd
from database import create_user_table, create_prediction_table, add_user, login_user, save_prediction

# Initialize database tables
create_user_table()
create_prediction_table()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login page
def login_page():
    st.title("🔐 Login to Health Assistant")
    choice = st.selectbox("Login / Sign Up", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            if login_user(username, password):
                st.success("Login successful ✅")
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials ❌")
    else:
        if st.button("Sign Up"):
            try:
                add_user(username, password)
                st.success("Account created. Please login.")
            except:
                st.error("User already exists or error occurred.")

# 🔐 Show login first
if not st.session_state.logged_in:
    login_page()
    st.stop()

# Load models
Diabetes_model = pickle.load(open('D:/Disease prediction/Saved Models/Diabetes_model.sav', 'rb'))
Heart_model = pickle.load(open('D:/Disease prediction/Saved Models/Heart_model.sav', 'rb'))
Ckd_model = pickle.load(open('D:/Disease prediction/Saved Models/CKD_model.sav', 'rb'))
scalar = pickle.load(open('D:/Disease prediction/Saved Models/Ckd_scalar.sav', 'rb'))

# Page config
st.set_page_config(page_title="Health Assistant", page_icon="🩺", layout="centered")
st.image("logo.png", width=100)

st.markdown("""
    <h1 style='text-align: center; color: white;'>Health Assistant</h1><hr>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System Menu',
                           ['Home','Diabetes', 'Heart Disease', 'Kidney Disease'],
                           menu_icon='hospital-fill',
                           icons=['house','activity', 'heart', 'person'],
                           default_index=st.session_state.get('__menu__', 0),
                           orientation="horizontal"
                           
)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- HOME PAGE ----------------
if selected == "Home":
    st.markdown("""
        <h2 style='text-align: center;'>🏠 Welcome to Health Assistant</h2>
        <p style='text-align: center; font-size:18px;'>
        This web app helps you predict the likelihood of:
        <b>Diabetes</b>, <b>Heart Disease</b>, and <b>Chronic Kidney Disease</b>
        using Machine Learning models.
        </p>
        <p style='text-align: center; font-size:16px;'>
        🔹 Choose a disease from the sidebar<br>
        🔹 Enter medical details<br>
        🔹 Instantly get predictions
        </p>
        <hr>
    """, unsafe_allow_html=True)

      # Add button to go to the first prediction page
    if st.button("👉 Go to Prediction Menu"):
        st.session_state['__menu__'] = 1  # Set sidebar index to 'Diabetes'
        st.rerun()

# ---------------- DIABETES ----------------
if selected == "Diabetes":
    st.subheader("🧪 Diabetes Prediction")
    col1, col2, col3 = st.columns(3)
    with col1: preg = st.number_input("Pregnancies", 0, 20)
    with col2: glucose = st.number_input("Glucose Level", 0, 200)
    with col3: bp = st.number_input("Blood Pressure", 0, 140)
    with col1: skin = st.number_input("Skin Thickness", 0, 100)
    with col2: insulin = st.number_input("Insulin", 0, 900)
    with col3: bmi = st.number_input("BMI", 0.0, 70.0)
    with col1: dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0)
    with col2: age = st.number_input("Age", 10, 100)

    if st.button("Predict", key="predict_diabetes"):
        input_data = np.array([[preg, glucose, bp, skin, insulin, bmi, dpf, age]])
        prediction = Diabetes_model.predict(input_data)
        st.success("🧪 Prediction: Diabetic" if prediction[0] == 1 else "✅ Prediction: Not Diabetic")

# ---------------- HEART DISEASE ----------------
if selected == "Heart Disease":
    st.subheader("❤️ Heart Disease Prediction")
    col1, col2, col3 = st.columns(3)
    with col1: age = st.number_input("Age", 1, 120)
    with col2: sex = st.selectbox("Sex", ["M", "F"])
    with col3:
        cp_map = {"TA: Typical Angina": "TA", "ATA: Atypical Angina": "ATA", "NAP: Non-Anginal Pain": "NAP", "ASY: Asymptomatic": "ASY"}
        ChestPainType = cp_map[st.selectbox("Chest Pain Type", list(cp_map.keys()))]
    with col1: RestingBP = st.number_input("Resting Blood Pressure", 0, 300)
    with col2: Cholesterol = st.number_input("Cholesterol", 0, 1000)
    with col3: FastingBS = int(st.selectbox("Fasting Blood Sugar", ["1: if > 120 mg/dl", "0: otherwise"]).split(":")[0])
    with col1: RestingECG = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
    with col2: MaxHR = st.number_input("Max Heart Rate", 60, 220)
    with col3: ExerciseAngina = st.selectbox("Exercise Induced Angina", ["Y", "N"])
    with col1: Oldpeak = st.number_input("Oldpeak", 0.0, 10.0, step=0.1)
    with col2: ST_Slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

    if st.button("Predict", key="predict_heart"):
        input_data = [
            float(age), 1 if sex == "M" else 0,
            ["TA", "ATA", "NAP", "ASY"].index(ChestPainType),
            float(RestingBP), float(Cholesterol), FastingBS,
            ["Normal", "ST", "LVH"].index(RestingECG), float(MaxHR),
            1 if ExerciseAngina == "Y" else 0, float(Oldpeak),
            ["Up", "Flat", "Down"].index(ST_Slope)
        ]
        prediction = Heart_model.predict([input_data])
        st.success("❤️ Prediction: Heart Disease Detected" if prediction[0] == 1 else "✅ Prediction: No Heart Disease")

# ---------------- KIDNEY DISEASE ----------------
if selected == "Kidney Disease":
    st.subheader("🧪 Chronic Kidney Disease Prediction")
    col1, col2, col3 = st.columns(3)
    with col1: serum_creatinine = st.number_input("Serum Creatinine", 0.0, 5.0)
    with col2: gfr = st.number_input("GFR", 0.0, 150.0)
    with col3: bun = st.number_input("Blood Urea Nitrogen (BUN)", 0.0, 150.0)
    with col1: serum_calcium = st.number_input("Serum Calcium", 0.0, 20.0)
    with col2: ana = st.selectbox("ANA (Antinuclear Antibody)", [0, 1])
    with col3: c3_c4 = st.number_input("C3 C4", 0.0, 200.0)
    with col1: hematuria = st.selectbox("Hematuria", [0, 1])
    with col2: oxalate_levels = st.number_input("Oxalate Levels", 0.0, 5.0)
    with col3: urine_ph = st.number_input("Urine pH", 0.0, 8.0)
    with col1: blood_pressure = st.number_input("Blood Pressure", 0.0, 180.0)
    with col2: physical_activity = st.selectbox("Physical Activity", ['daily', 'weekly', 'rarely'])
    with col3: diet = st.selectbox("Diet", ['high protein', 'low salt', 'balanced'])
    with col1: water_intake = st.number_input("Water Intake (L/day)", 0.0, 4.0)
    with col2: smoking = st.selectbox("Smoking", ['yes', 'no'])
    with col3: alcohol = st.selectbox("Alcohol", ['daily', 'occasionally', 'never'])
    with col1: painkiller_usage = st.selectbox("Painkiller Usage", ['yes', 'no'])
    with col2: family_history = st.selectbox("Family History of CKD", ['yes', 'no'])
    with col3: weight_changes = st.selectbox("Weight Changes", ['stable', 'gain', 'loss'])
    with col1: stress_level = st.selectbox("Stress Level", ['low', 'medium', 'high'])

    if st.button("Predict", key="predict_kidney"):
        input_data = [
            serum_creatinine, gfr, bun, serum_calcium, ana, c3_c4, hematuria, oxalate_levels,
            urine_ph, blood_pressure, ['daily', 'weekly', 'rarely'].index(physical_activity),
            ['high protein', 'low salt', 'balanced'].index(diet), water_intake,
            ['yes', 'no'].index(smoking), ['daily', 'occasionally', 'never'].index(alcohol),
            ['yes', 'no'].index(painkiller_usage), ['yes', 'no'].index(family_history),
            ['stable', 'gain', 'loss'].index(weight_changes), ['low', 'medium', 'high'].index(stress_level)
        ]
        scaled_input = scalar.transform(np.array(input_data).reshape(1, -1))
        prediction = Ckd_model.predict(scaled_input)
        st.success("🧪 CKD Prediction: YES" if prediction[0][0] == 0 else "✅ CKD Prediction: NO")
        st.info(f"Predicted Stage: {prediction[0][1]}")
