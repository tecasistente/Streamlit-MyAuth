import streamlit as st
import pandas as pd
import plotly.express as px


def layout():
    st.title("Visualizador de datos")
    st.subheader("Grafico de lineas")
    data = {"a":[23, 12, 78, 4, 54], "b":[0, 13 ,88, 1, 3], "c":[45, 2, 546, 67, 56]} 
    df = pd.DataFrame(data)
    df
    st.line_chart(data=df)

    st.subheader("Grafico de barras")
    df
    st.bar_chart(data=df)

    st.subheader("Grafico de area")
    df
    st.area_chart(data=df)

    #grafico interactivo
    df_interactivo= px.data.gapminder()
    fig = px.scatter(
        df_interactivo.query("year==2007"),
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=60,
    )

    tab1, tab2 = st.tabs(["Tema #1", "Tema #2"])
    with tab1:
        # tema streamlit
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    with tab2:
        # ploty tema
        st.plotly_chart(fig, theme=None, use_container_width=True)