import streamlit as st

st.set_page_config(page_title="Mobile Form Demo", layout="centered")

st.title("📱 Mobile Friendly Form")

st.write("Fill this form on your phone or desktop")

with st.form("user_form"):
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=0, max_value=120)
    email = st.text_input("Enter your email")

    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    feedback = st.text_area("Your feedback")

    submitted = st.form_submit_button("Submit")

if submitted:
    st.success("Form submitted successfully!")
    st.write("### Submitted Data:")
    st.write("Name:", name)
    st.write("Age:", age)
    st.write("Email:", email)
    st.write("Gender:", gender)
    st.write("Feedback:", feedback)
