import streamlit as st  # Importar la biblioteca Streamlit para crear la aplicación web
import pyshorteners  # Importar la biblioteca pyshorteners para acortar y expandir URLs

shorter = pyshorteners.Shortener()  # Instanciar un objeto Shortener para utilizar sus métodos

def layout():
    st.title("Acortador de URL") 

    # Crear un formulario para acortar URLs
    form = st.form("URL", clear_on_submit=True)
    url = form.text_input("Colocar la URL para acortar:") 
    button = form.form_submit_button("Acortar") 

    # Crear una barra lateral en la interfaz de la aplicación
    with st.sidebar: 
        st.write("Herramienta para cortar o expandir un link usando tinyurl") 

    if button: 
        try:
            url_shorter = shorter.tinyurl.short(url)           # Acortar la URL utilizando el método short()
            st.success("El link acortado es: " + url_shorter)  
        except:
            st.error("Algo salió mal :(")  

    # Crear un formulario para expandir URLs acortadas
    form_expand = st.form("URL2", clear_on_submit=True)
    url_new = form.text_input("Colocar la URL acortada: ") 
    button_expand = form.form_submit_button("Expandir")

    if button_expand:  # Verificar si se presionó el botón de envío
        try:
            url_expand = shorter.tinyurl.expand(url_new)  # Expandir la URL acortada utilizando el método expand()
            st.success("El link expandido es: " + url_expand)  
        except:
            st.error("Algo salió mal :(") 
