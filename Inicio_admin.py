import streamlit as st
import apps.peliculas as peliculas
import apps.acortador_url as acortador

def main_page(authenticator):
    st.title("Página Principal")
    st.subheader("Proyectos realizados: ")
    st.markdown("<li>Visualizador de Noticias</li><li>Buscador de películas</li>", unsafe_allow_html=True)

    st.sidebar.markdown("# Inicio 🎈")

def page2(authenticator):
    st.sidebar.markdown("# Acortador")
    acortador.layout()
    

def page3(authenticator): 
    st.sidebar.markdown("# Películas ")
    peliculas.layout()

def page4(authenticator):
    authenticator.reset_password(st.session_state['username'], "Cambiar Contraseña")


page_names_to_funcs= {
    "Inicio": main_page,
    "Acortador": page2,
    "Peliculas": page3,
    "Cambiar Contraseña": page4
    
}


def inicio_layout(authenticator, username):
    sidebar=st.sidebar
    authenticator.logout("Cerrar Sesión", "sidebar")    
    sidebar.title(f"Bienvenido {username}")
    selected_page = st.sidebar.selectbox("Selecciona una página", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page](authenticator)

    