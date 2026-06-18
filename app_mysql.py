# importar mysql.conector
import mysql.connector
import pandas as pd
import streamlit as st

#conectar a mysql
conexion= mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bd_lavadora"
)
#crear cursor
cursor=conexion.cursor()
#Consultar los datos de la tabla clientes mostrar en un dataframe, mostrar medisnte stramlit
cursor.execute("SELECT * FROM cliente")
resultados=cursor.fetchall()
df=pd.DataFrame(resultados, columns=[i[0] for i in cursor.description])
st.title("Datos de Clientes")
st.dataframe(df)
#leer directamente desde mysql a un dataframe
df_mysql=pd.read_sql("SELECT * FROM cliente", conexion)
st.title("Datos de Clientes desde MySQL a DataFrame")
st.dataframe(df_mysql)
df_productos=pd.read_sql("SELECT * FROM producto", conexion)
st.title("Datos de Productos")
st.dataframe(df_productos)
#mostrar datos mediante grafica con plotly
import plotly.express as px
fig=px.bar(df_productos, x="nombre", y="costo", title="Precio de Productos")
st.plotly_chart(fig)
#numero de clientes por ciudad obtener desde el dataframe df y mostrar en una grafica
df_clientes_ciudad=df.groupby("localidad").size().reset_index(name="cantidad")
fig_ciudad=px.bar(df_clientes_ciudad, x="localidad", y="cantidad", title="Número de Clientes por Ciudad")
st.plotly_chart(fig_ciudad)


