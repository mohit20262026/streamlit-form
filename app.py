import streamlit as st

st.set_page_config(page_title="Mobile Form", layout="centered")

st.title("📱 Contact Form")

name = st.text_input("👤 Name")
phone = st.text_input("📞 Phone Number")
email = st.text_input("📧 Email")
message = st.text_area("💬 Message")

if st.button("Submit"):
    if name and phone:
        st.success("✅ Submitted successfully!")
        st.write({
            "Name": name,
            "Phone": phone,
            "Email": email,
            "Message": message
        })
    else:
        st.error("⚠️ Name and Phone are required")