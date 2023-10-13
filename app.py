from sign_up import sign_up_layout
import streamlit as st
import authenticate as stauth
import Inicio_admin 
import Inicio_editor

authenticator = stauth.Authenticate("streamlit", "abcdef",30)

name, authentication_status, username, role = authenticator.login("Iniciar Sesion","main")

if authentication_status == False:
    st.error("Nombre de Usuario o Contraseña incorrectos")

if authentication_status == None:
    st.warning("Por favor, ingrese el nombre de usuario y contraseña")

if username=="new_user":
    sign_up_layout(authenticator)

if authentication_status and role =="Editor":
    Inicio_editor.inicio_layout(authenticator, username)

elif authentication_status and role =="Administrador":
    Inicio_admin.inicio_layout(authenticator, username)

elif authentication_status and role =="Invitado":
    authenticator.logout("Cerrar Sesión", "main")
    st.title(f"Bienvenido {username}")
    st.subheader("Página en construcción")
