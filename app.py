import streamlit as st
import lightgbm as lgb
import numpy as np

# Load the AKD and CKD models
aki_model = lgb.Booster(model_file='aki_model.txt')
akd_model = lgb.Booster(model_file='akd_model.txt')

# Mapping for Urine_protein and AKIGrade values
AKI_first_grade_mapping = {"Stage 0": 0, "Stage 1": 1, "Stage 2": 2, "Stage 3": 3}
Diuretics_mapping = {"NO": 0, "Yes": 1}
Dopamine_and_epinephrine_drugs_mapping = {"NO": 0, "Yes": 1}
HBp_mapping = {"NO": 0, "Yes": 1}
anti_gout_medication_mapping = {"NO": 0, "Yes": 1}
NSAIDs_mapping = {"NO": 0, "Yes": 1}
Glucocorticoid_mapping = {"NO": 0, "Yes": 1}
History_of_surgery_mapping = {"NO": 0, "Yes": 1}
Antineoplastic_agents_mapping = {"NO": 0, "Yes": 1}
PPI_mapping = {"NO": 0, "Yes": 1}
Upro_mapping = {"Negative": 0, "+": 1,"++": 2,"+++": 3}

def predict_aki_probability(features):
    aki_prob = aki_model.predict(features)
    return aki_prob[0]

def predict_akd_probability(features):
    akd_prob = akd_model.predict(features)
    return akd_prob[0]

def main():
    st.title('Predicting the Probability of AKI or AKD Occurrence in Gout Patients')

# User selects which content to display
    selected_content = st.radio("", ("Model Introduction", "AKI or AKD Prediction"))

    if selected_content == "Model Introduction":
        st.subheader("Model Introduction")
        st.write("The online application aims to predict the probability of acute kidney injury (AKI) and acute kidney disease (AKD) in gout patients by leveraging their clinical data through the LightGBM algorithm.")
        # Disclaimer
        st.subheader("Disclaimer")
        st.write("The predictions generated by this model are based on historical data and statistical patterns, and they may not be entirely accurate or applicable to every individual.")
        st.write("**For Patients:**")
        st.write("- The predictions presented by this platform are intended for informational purposes only and should not be regarded as a substitute for professional medical advice, diagnosis, or treatment.")
        st.write("- Consult with your healthcare provider for personalized medical guidance and decisions concerning your health.")
        st.write("**For Healthcare Professionals:**")
        st.write("- This platform should be considered as a supplementary tool to aid clinical decision-making and should not be the sole determinant of patient care.")
        st.write("- Clinical judgment and expertise should always take precedence in medical practice.")
        st.write("**For Researchers:**")
        st.write("- While this platform can serve as a valuable resource for research purposes, it is crucial to validate its predictions within your specific clinical context and patient population.")
        st.write("- Ensure that your research adheres to all ethical and regulatory standards.")
        st.write("The creators of this online platform and model disclaim any responsibility for decisions or actions taken based on the predictions provided herein. Please use this tool responsibly and always consider individual patient characteristics and clinical context when making medical decisions.")
        st.write("By utilizing this online platform, you agree to the terms and conditions outlined in this disclaimer.")

    elif selected_content == "AKI or AKD Prediction":
        st.subheader("AKI or AKD Prediction in Gout patients")

    # User selects prediction type (AKD or AKI)
        prediction_type = st.radio("Select Prediction Type", ("AKI Prediction", "AKD Prediction"))

    # Feature input
        features = []

        if prediction_type == "AKI Prediction":
            st.subheader("Predictive Features for AKI in Gout Patients")

            Diuretics = st.selectbox("Diuretics", ["NO", "Yes"], key="Diuretics_AKI")
            Na = st.number_input("Serum sodium (mmol/L)", value=0.0, format="%.2f", key="Na_AKI") 
            anti_gout_medication = st.selectbox("Urate-Lowering Therapy", ["NO", "Yes"], key="anti_gout_medication_AKI")
            HBp = st.selectbox("Hypertension", ["NO", "Yes"], key="HBp_AKI")
            Upro = st.selectbox("Urine protein", ["Negative", "+","++","+++"], key="Upro_AKI")
            ALP = st.number_input("ALP (U/L)", value=0.0, format="%.2f", key="ALP_AKI") 
            UA = st.number_input("Uric acid (umol/L)", value=0.0, format="%.2f", key="UA_AKI")
            Glu= st.number_input("Blood glucose (mmol/L)", value=0.0, format="%.2f", key="Glu_AKI")            
            PPI = st.selectbox("PPI", ["NO", "Yes"], key="PPI_AKI")
            TP = st.number_input("Total protein (g/L)", value=0.0, format="%.2f", key="TP_AKI")


            PPI_encoded = PPI_mapping[PPI]
            Diuretics_encoded = Diuretics_mapping[Diuretics]
            HBp_encoded = HBp_mapping[HBp]
            anti_gout_medication_encoded = anti_gout_medication_mapping[anti_gout_medication]
            Upro_encoded = Upro_mapping[Upro]
            
            features.extend([Diuretics_encoded, HBp_encoded,Na,anti_gout_medication_encoded,ALP, UA, PPI_encoded,Glu, PPI_encoded,TP])
            if st.button("Predict AKI Probability"):
                aki_prob = predict_aki_probability(np.array(features).reshape(1, -1))
                st.write(f"AKI Probability: {aki_prob:.2f}")

        elif prediction_type == "AKD Prediction":
            st.subheader("Predictive Features for AKD in Gout Patients")
 
            Age = st.number_input("Age (years)", value=0, format="%d", key="Age_AKD")
            Diuretics = st.selectbox("Diuretics", ["NO", "Yes"], key="Diuretics_AKD")
            AKI_first_grade = st.selectbox("AKI Grade", ["Stage 0", "Stage 1", "Stage 2", "Stage 3"], key="AKI_first_grade_AKD")
            RBC = st.number_input("RBC (10^12/L)", value=0.0, format="%.2f", key="RBC_AKD") 
            Ca = st.number_input("Serum calcium (mmol/L)", value=0.0, format="%.2f", key="Ca_AKD")
            Specific_gravity_Urinalysis = st.number_input("Urine specific gravity", value=0.0, format="%.2f", key="Specific_gravity_Urinalysis_AKD")
            Antineoplastic_agents = st.selectbox("Antineoplastic agents", ["NO", "Yes"], key="Antineoplastic_agents_AKD")
            cysC = st.number_input("cystatin C(mg/L )", value=0.0, format="%.2f", key="cystatin_C_AKD")
            History_of_surgery = st.selectbox("History of surgery", ["NO", "Yes"], key="History_of_surgery_AKD")
            hemoglobin = st.number_input("Hemoglobin (g/L)", value=0.0, format="%.2f", key="hemoglobin_AKD")

        # Map AKIGrade back to 0, 1, 2, 3 for prediction
            Diuretics_encoded = Diuretics_mapping[Diuretics]
            AKI_first_grade_encoded = AKI_first_grade_mapping[AKI_first_grade]
            Antineoplastic_agents_encoded = Antineoplastic_agents_mapping[Antineoplastic_agents]
            History_of_surgery_encoded = History_of_surgery_mapping[History_of_surgery]

            features.extend([Age, Diuretics_encoded, AKI_first_grade_encoded, RBC, Ca, Specific_gravity_Urinalysis,Antineoplastic_agents_encoded, cysC, History_of_surgery_encoded, hemoglobin])
            if st.button("Predict AKD Probability"):
                akd_prob = predict_akd_probability(np.array(features).reshape(1, -1))
                st.write(f"AKD Probability: {akd_prob:.2f}")

if __name__ == '__main__':
    main()
