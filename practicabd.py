import mysql.connector
import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Practica con Base de Datos")
conexion=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bd_lavadora" 
)
if conexion.is_connected():
    st.success("Conexión exitosa a la base de datos")
    df=pd.read_sql("SELECT * FROM CLIENTE",conexion)
    st.dataframe(df)
    df_localidad=df.groupby("localidad").size().reset_index(name="cantidad")
    st.dataframe(df_localidad)
    fig=px.bar(df_localidad, x="localidad", y="cantidad", title="Cantidad de clientes")
    st.plotly_chart(fig)

    df_productos=pd.read_sql("SELECT * FROM producto",conexion)
    st.header("Datos de productos")
    st.dataframe(df_productos)
    fig_producto=px.bar(df_productos, x="nombre", y="costo", title="Productos vs costo")
    st.plotly_chart(fig_producto)
    st.title("COMANDOS BÁSICOS")
    st.dataframe(df.head())
    st.dataframe(df.tail())
    print(df.info())
    st.write("Información del DataFrame: ", df.info())
    st.write("Número de filas y columnas: ", df.shape)
    st.write("Nombres de columnas: ", df.columns)
    st.dataframe(df.describe())
    st.write("valores nullos: ", df.isnull().sum())
    st.write("Tipos de datos de las columnas: ", df.dtypes)
    st.write("Valores duplicados clientes: ", df.duplicated().sum())
    st.write("Valores duplicados productos: ", df_productos.duplicated().sum())

else:
    st.error("Error en la conexión")


