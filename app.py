import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Form + CSV Storage", layout="centered")

st.title("📱 Streamlit Form with Data Storage")

# File where data will be stored
FILE_PATH = "submissions.csv"

# Create file if it doesn't exist
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=["Name", "Age", "Email", "Feedback"])
    df.to_csv(FILE_PATH, index=False)

# Form UI
with st.form("user_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", 0, 120)
    email = st.text_input("Email")
    feedback = st.text_area("Feedback")

    submit = st.form_submit_button("Submit")

# When submitted
if submit:
    new_entry = pd.DataFrame([[name, age, email, feedback]],
                             columns=["Name", "Age", "Email", "Feedback"])

    old_data = pd.read_csv(FILE_PATH)

    updated_data = pd.concat([old_data, new_entry], ignore_index=True)

    updated_data.to_csv(FILE_PATH, index=False)

    st.success("✅ Data saved successfully!")

# Show all data
st.subheader("📊 All Submitted Data")
df = pd.read_csv(FILE_PATH)
st.dataframe(df, use_container_width=True)
