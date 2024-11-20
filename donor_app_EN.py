import streamlit as st
import numpy as np

# Title and summary
st.title("Predicted Cr values 1 year after donor kidney donation")
st.write("""
This app is a tool to calculate creatinine values 1 year after donation by entering weight, creatinine value, non-extracted kidney volume, and gender.
""")

# Description of each item first
st.markdown("""
- **Body Weight (Bw)**: Donor weight in kg.
- **Creatinine (Cre)**: Preoperative blood creatinine level (mg/dL)
- **Non-Excised Kidney Volume**: Volume of non-excised kidney measured by CT (in mL)
- **Male (1 for Male, 0 for Female)**: Gender (Male: 1, Female: 0)
""")

# Input
st.write("Please enter the following parameters:")
Bw = st.number_input("Body Weight (Bw)", min_value=0.0, step=0.1)
Cre = st.number_input("Creatinine (Cre)", min_value=0.0, step=0.01)
NonExcisedKidney = st.number_input("Non-Excised Kidney Volume", min_value=0.0, step=0.1)
Male = st.selectbox("Male (1 for Male, 0 for Female)", options=[1, 0])

# Simplify_model calculation function
def calculate_simplify_model(Bw, Cre, NonExcisedKidney, Male, Age=50):
    # Fixed values
    CVD_replaced = 0
    HbA1C_replaced = 5.7
    BUN_replaced = 13.8

    # Model calculations
    model_1 = -0.09903755662234529 + 0.006502924180113298 * Bw + 1.3625035862329375 * np.sqrt(Cre) + 0.1139767991517405 * Male - 0.0027455075816872963 * NonExcisedKidney
    model_2 = -0.3901364879414445 + 0.04471756216946074 * BUN_replaced + 0.006715659519617908 * Bw + 1.0352518798689898 * Cre - 0.000009604315179117748 * BUN_replaced**2 * NonExcisedKidney
    model_3 = -0.38478682583687274 + 0.002081547696286225 * Age + 0.04399956263153849 * BUN_replaced + 0.005628920758504391 * Bw + 0.9320131800396743 * Cre + 0.06722065750493375 * Male - 0.000009867424180159245 * BUN_replaced**2 * NonExcisedKidney
    model_4 = 0.049617816124754036 + 0.9225151798784034 * Cre + 0.18320900637720863 * CVD_replaced + 0.10349178758374927 * HbA1C_replaced + 0.13985579153513217 * Male - 0.0019323076033121343 * NonExcisedKidney
    model_5 = -0.18899026587394271 + 0.024398835894397737 * BUN_replaced + 0.0032842131730298754 * Bw + 1.142965718977502e-9 * BUN_replaced**4 * NonExcisedKidney
    model_6 = -0.006961262066861628 + 0.8126766126098913 * Cre + 0.11057326356803435 * Male + 1.4573284728625062 / (0.7326765340341233 + NonExcisedKidney / Bw)
    model_7 = 0.005082859737290714 + 0.03531000856642338 * BUN_replaced + 0.00699894215253158 * Bw + 0.7899600124990199 * Cre + 0.10910119812549417 * Male - 0.0002167791209982864 * BUN_replaced * NonExcisedKidney
    model_8 = 1.2549512514779957 + 0.005164327440285673 * Bw + 0.8188362941962077 * Cre - 4.127069601506772 / (CVD_replaced + HbA1C_replaced + Male) - 0.0026704663767301066 * NonExcisedKidney
    model_9 = -0.15903717053578167 + 0.00025977004836070643 * Age * BUN_replaced + 0.005291867117086743 * Bw + 1.0913423662894317 * Cre - 6.322735119054266e-12 * BUN_replaced**3 * NonExcisedKidney**3

    # Calculate median of all models
    simplify_model = np.median([model_1, model_2, model_3, model_4, model_5, model_6, model_7, model_8, model_9], axis=0)
    return simplify_model

# Input fields
Bw = st.number_input("Body Weight (Bw)", min_value=0.0, step=0.1)
Cre = st.number_input("Creatinine (Cre)", min_value=0.0, step=0.01)
NonExcisedKidney = st.number_input("Non-Excised Kidney Volume", min_value=0.0, step=0.1)
Male = st.selectbox("Male (1 for Male, 0 for Female)", options=[1, 0])

# Calculate button
if st.button("Calculate"):
    try:
        result = calculate_simplify_model(Bw, Cre, NonExcisedKidney, Male)
        st.success(f"Your predicted creatinine value after 1 year of kidney donation is as follows (in mg/dL): {result;.2f}")
    except Exception as e:
        st.error(f"An error occurred: \{e\}")

# Notes
        st.write("""
        **This result is calculated based on data from patients who actually donated a kidney at the Department of Urology, Tokyo Women's Medical University.
        Please note that the actual measured values may differ. **
        """)

        
}
