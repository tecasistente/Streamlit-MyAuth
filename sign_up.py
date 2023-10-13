import streamlit as st
import authenticate as stauth

def sign_up_layout(authenticator):
    sidebar=st.sidebar
    
    authenticator.create_user("Crear Cuenta", "main")