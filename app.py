import streamlit as st
import pandas as pd
import os

FILE_PATH = "submissions.csv"

st.title("📱 Form with Download Feature")

# Create file if not exists
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=["Name", "Age", "Email", "Feedback"])
    df.to_csv(FILE_PATH, index=False)

with st.form("form"):
    name = st.text_input("Name")
    age = st.number_input("Age", 0, 120)
    email = st.text_input("Email")
    feedback = st.text_area("Feedback")

    submit = st.form_submit_button("Submit")

if submit:
    new_data = pd.DataFrame([[name, age, email, feedback]],
                            columns=["Name", "Age", "Email", "Feedback"])

    old_data = pd.read_csv(FILE_PATH)
    updated = pd.concat([old_data, new_data], ignore_index=True)
    updated.to_csv(FILE_PATH, index=False)

    st.success("Saved!")

# Show data
df = pd.read_csv(FILE_PATH)
st.dataframe(df)

# ✅ DOWNLOAD BUTTON
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="submissions.csv",
    mime="text/csv"
)
