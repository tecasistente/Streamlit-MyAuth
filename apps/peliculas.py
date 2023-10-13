import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def layout():
    #leer el archivo desde la nube
    movies_data = pd.read_csv("https://tinyurl.com/2nej9f8a")

    # Crear un sidebar con los valores unicos del dataset
    #se crea lista de puntuación, genero y año
    score_rating = movies_data['score'].unique().tolist() 
    genre_list = movies_data['genre'].unique().tolist()
    year_list = movies_data['year'].unique().tolist()

    #Filtros apareceran el el slider y no en la pantalla
    with st.sidebar:
        st.write("Selecciona un rango para la calificación de la película \
        Género de la película y un año para realizar la busqueda ")
        #un slider para la calificacion
        new_score_rating = st.slider(label = "Selecciona un valor:",min_value = 1.0,max_value = 10.0)

        #seleccion multiple para el genero de las peliculas
        new_genre_list = st.multiselect('Selecciona un género:',genre_list, default=["Comedy", "Action"])
        #seleccionar un año para la busqueda
        year = st.selectbox('Selecciona un año:',year_list, 0)

    #peliculas que si cumlen con la calificacion 
    score_info = (movies_data['score'].between(1, new_score_rating))
    #fitrar segun la busquedas del usuario
    new_genre_year = (movies_data['genre'].isin(new_genre_list)) & (movies_data['year'] == year) & score_info

    #ver la lista delas peliculas segpun los filtros en un dataframe
    st.write("""#### Lista de películas filtradas por año, género y puntuación """)
    dataframe_genre_year = movies_data[new_genre_year].groupby(['name',  'genre',"score"])['year'].sum()
    dataframe_genre_year = dataframe_genre_year.reset_index()
    st.dataframe(dataframe_genre_year, width = 800)

