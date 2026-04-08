import streamlit as st
import pandas as pd
import pickle

# ==============================
# LOAD MODEL FILES
# ==============================
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# ==============================
# TITLE
# ==============================
st.title("🎓 Burnout Prediction System")
st.write("Enter student details and click Predict")

# ==============================
# USER INPUT
# ==============================

st.subheader("📋 Student Details")

age = st.number_input("Age", min_value=15, max_value=30)

gender = st.selectbox("Gender", ["Select", "Male", "Female"])

course = st.selectbox("Course", ["Select", "Science", "Commerce", "Arts"])

year = st.number_input("Year", min_value=1, max_value=5)

# Academic
st.subheader("📊 Academic Details")

daily_study_hours = st.number_input("Daily Study Hours")

cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0)

attendance_percentage = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0)

# Mental Health
st.subheader("🧠 Mental Health")

stress_level = st.selectbox("Stress Level", ["Select", "Low", "Medium", "High"])

anxiety_score = st.number_input("Anxiety Score")

depression_score = st.number_input("Depression Score")

academic_pressure_score = st.number_input("Academic Pressure")

financial_stress_score = st.number_input("Financial Stress")

social_support_score = st.number_input("Social Support")

# Lifestyle
st.subheader("🏃 Lifestyle")

daily_sleep_hours = st.number_input("Daily Sleep Hours")

screen_time_hours = st.number_input("Screen Time Hours")

physical_activity_hours = st.number_input("Physical Activity Hours")

sleep_quality = st.selectbox("Sleep Quality", ["Select", "Poor", "Average", "Good"])

internet_quality = st.selectbox("Internet Quality", ["Select", "Poor", "Average", "Good"])

# ==============================
# PREDICT BUTTON
# ==============================
if st.button("🔍 Predict Burnout"):

    # ==============================
    # VALIDATION
    # ==============================
    if (
        gender == "Select" or course == "Select" or
        stress_level == "Select" or sleep_quality == "Select" or
        internet_quality == "Select"
    ):
        st.warning("⚠️ Please select all dropdown values")

    elif age == 0 or cgpa == 0 or attendance_percentage == 0:
        st.warning("⚠️ Please enter valid numeric values")

    else:
        # ==============================
        # CREATE INPUT DICTIONARY
        # ==============================
        user_input = {
            "age": age,
            "gender": 1 if gender == "Male" else 0,
            "course": {"Science": 0, "Commerce": 1, "Arts": 2}[course],
            "year": year,
            "daily_study_hours": daily_study_hours,
            "daily_sleep_hours": daily_sleep_hours,
            "screen_time_hours": screen_time_hours,
            "stress_level": {"Low": 0, "Medium": 1, "High": 2}[stress_level],
            "anxiety_score": anxiety_score,
            "depression_score": depression_score,
            "academic_pressure_score": academic_pressure_score,
            "financial_stress_score": financial_stress_score,
            "social_support_score": social_support_score,
            "physical_activity_hours": physical_activity_hours,
            "sleep_quality": {"Poor": 0, "Average": 1, "Good": 2}[sleep_quality],
            "attendance_percentage": attendance_percentage,
            "cgpa": cgpa,
            "internet_quality": {"Poor": 0, "Average": 1, "Good": 2}[internet_quality]
        }

        # ==============================
        # FEATURE ENGINEERING
        # ==============================
        user_input["lifestyle_score"] = (
            daily_sleep_hours + physical_activity_hours - screen_time_hours
        )

        st.info(f"Lifestyle Score: {user_input['lifestyle_score']}")

        # ==============================
        # CREATE DATAFRAME
        # ==============================
        input_df = pd.DataFrame([user_input])
        input_df = input_df[columns]

        # ==============================
        # SCALE & PREDICT
        # ==============================
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]

        # ==============================
        # OUTPUT
        # ==============================
        st.subheader("📊 Prediction Result")

        if prediction == 0:
            st.success("Low Burnout 😊")
        elif prediction == 1:
            st.warning("Medium Burnout ⚠️")
        else:
            st.error("High Burnout 🚨")