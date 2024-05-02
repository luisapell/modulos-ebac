import streamlit as st
import numpy as np
import pandas as pd
import random
import pydeck as pdk
import graphviz 
import datetime

st.title('Bem vindx!')

dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

st.title('Tabela 1')

st.write("Tabela aleatória:")
st.write(pd.DataFrame({
    'primeira coluna': [1, 2, 3, 4],
    'segunda coluna': [10, 20, 30, 40]
}))

"""
# Tabela 2
Tabela aleatória:
"""

df = pd.DataFrame({
  'primeira coluna': [1, 2, 3, 4],
  'segunda coluna': [10, 20, 30, 40]
})

df

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

import time

'Starting a long computation...'

# Visualização de dados nos últimos dias de acordo com os sites abaixo 

st.title('Visualização de dados nos últimos dias de acordo com os sites abaixo')

df = pd.DataFrame(
    {
        "name": ["Roadmap", "Extras", "Issues"],
        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
    }
)
st.dataframe(
    df,
    column_config={
        "name": "App name",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
        "views_history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    },
    hide_index=True,
)

# Medição de temperatura 

st.title('Medição de Temperatura')

col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

# Tabela interativa 

st.title('Tabela Interativa')

df = pd.DataFrame(
    [
       {"command": "st.selectbox", "rating": 4, "is_widget": True},
       {"command": "st.balloons", "rating": 5, "is_widget": False},
       {"command": "st.time_input", "rating": 3, "is_widget": True},
   ]
)
edited_df = st.data_editor(df, num_rows="dynamic")

favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(f"Seu comando favorito é: *{favorite_command}* 🎈")

# Gráfico de geleiras

st.title('Gráfico com geleiras com dados aleatórios')

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.area_chart(chart_data)

# Gráfico de barras 

st.title('Gráfico de barras')

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.bar_chart(chart_data)

# Gráfico com linhas 

st.title('Gráfico com linhas')

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)

# Gráfico scatter 

st.title('Gráfico Scatter')

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.scatter_chart(chart_data)

# Gráfico 3D

st.title('Gráfico em 3D')

chart_data = pd.DataFrame(
   np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
   columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-122.4,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=chart_data,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=chart_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))

# Árvore de decisão 

st.title('Árvore de decisão')

st.graphviz_chart('''
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
        run -> kernel
        kernel -> zombie
        kernel -> sleep
        kernel -> runmem
        sleep -> swap
        swap -> runswap
        runswap -> new
        runswap -> runmem
        new -> runmem
        sleep -> runmem
    }
''')

st.title('Seletor de cores')

color = st.color_picker('Escolha a cor', '#00f900')
st.write('A cor é:', color)

st.title('Caixa de seleção')

option = st.selectbox(
    'Como você deseja falar comigo? ',
    ('Email', 'Telefone celular', 'Telefone casa'))

st.write('Você escolheu:', option)

st.title('Caixa de seleção para datas')

d = st.date_input("Quando é seu aniversário?", datetime.date(2019, 7, 6))
st.write('Seu aniversário é:', d)

st.title('Botão com link')

st.link_button("Ir ao google", "https://www.google.com.br/")

st.title('Botão aceito')

agree = st.checkbox('Aceito')

if agree:
    st.write('Boa!')

st.title('Ativar')

on = st.toggle('Ative suas experiências em ciência de dados')

if on:
    st.write('Ativado!')

st.title('Opções códigos de cores')

options = st.multiselect(
    'Qual é sua cor favorita?',
    ['Verde', 'Amarelo', 'Vermelho', 'Azul'],
    ['Amarelo', 'Vermelho'])

st.write('Você escolheu:', options)