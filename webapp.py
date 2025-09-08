import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pickle

st.set_page_config(page_title="Health Assistant", layout="wide")

# Show navbar
selected = option_menu(
    menu_title=None,
    options=["Home", "Disease Predictor", "About"],
    icons=["house", "activity", "info"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

if selected == "Home":
    st.title("🏥 Welcome to Health Assistant")

    st.markdown("""
        This web app helps you predict the likelihood of:
        <b>Diabetes</b>, <b>Heart Disease</b>, and <b>Chronic Kidney Disease</b>
        using Machine Learning models.
        </p>
        <p font-size:16px;'>
        🔹 Choose a disease from the Disease Predictor<br>
        🔹 Enter medical details<br>
        🔹 Instantly get predictions
        </p>
        <hr>
    """, unsafe_allow_html=True)

elif selected == "Disease Predictor":

    st.title("🧪 Disease Predictor")

    Diabetes_model = pickle.load(open('Saved Models/Diabetes_model.sav', 'rb'))
    Heart_model = pickle.load(open('Saved Models/Heart_model.sav', 'rb'))
    Ckd_model = pickle.load(open('Saved Models/CKD_model.sav', 'rb'))
    scalar = pickle.load(open('Saved Models/Ckd_scalar.sav', 'rb'))
    
    disease = st.selectbox("Select Disease to Predict", ["Diabetes", "Heart Disease", "Kidney Disease"])
    
    if disease == "Diabetes":
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
    if disease == "Heart Disease":
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
    if disease == "Kidney Disease":
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

elif selected == "About":

    st.title("ℹ️ About & 📬 Contact")
    
    tab1, tab2 = st.tabs(["About Project", "Contact Developer"])
    
    with tab1:
        st.subheader("About Health Assistant")
        st.write("""
        **Health Assistant** is a multi-disease prediction web app built using:
        - Python 🐍
        - Streamlit 🌐
        - Machine Learning (with Scikit-learn)
        - SQLite Database for user login
    
        It helps users predict the likelihood of having diseases like:
        - 🩺 Diabetes
        - ❤️ Heart Disease
        - 🧬 Kidney Disease
    
        This project aims to demonstrate the power of AI in simplifying medical diagnostics.
        """)
    
    with tab2:
        st.subheader("Developer Info")
        st.markdown("""
        **👨‍💻 Developer:** Shah Faisal Khan  
        📧 **Email:** [shahfaisal3102@gmail.com](mailto:shahfaisal3102@gmail.com)  
        📞 **Phone:** +91 8744020553  
        🌐 **GitHub:** [github.com/shahfaisal3102](https://github.com/)  
        """)



    # Footer
def footer():
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #f0f0f0;
            text-align: center;
            padding: 10px;
            color: gray;
        }
        </style>
        <div class="footer">
            © 2025 Shah Faisal Khan | Health Assistant | All Rights Reserved
        </div>
    """, unsafe_allow_html=True)

footer()
