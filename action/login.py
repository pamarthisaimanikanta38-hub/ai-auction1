import streamlit as st
from otp_system import generate_otp,verify_otp

def login():

    st.title("🔐 IPL Auction Login")

    phone = st.text_input("Enter Phone Number")

    if st.button("Send OTP"):

        otp = generate_otp()

        st.session_state.real_otp = otp

        st.success(f"OTP sent: {otp}")   # demo project

    user_otp = st.text_input("Enter OTP")

    if st.button("Login"):

        if verify_otp(int(user_otp),st.session_state.real_otp):

            st.session_state.logged=True
            st.success("Login Successful")

        else:
            st.error("Invalid OTP")