import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Lectura de Archivos", layout="wide")

st.title("📂 Práctica: Lectura de archivos")
st.markdown("Carga un archivo para procesar y visualizar su contenido de forma dinámica.")

# Selector de archivos
archivo = st.file_uploader(
    "Seleccione un archivo",
    type=["csv", "xlsx", "json", "xml"]
)

if archivo is not None:
    # Creamos dos columnas para mejorar la distribución visual
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("📊 Información del Archivo")
        st.info(f"**Nombre:** {archivo.name}\n\n**Tipo:** {archivo.type}")

    with col2:
        st.subheader("📋 Vista Previa de los Datos")
        
        try:
            # Identificación y lectura según la extensión
            if archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)

            elif archivo.name.endswith(".xlsx"):
                # Nota: Requiere tener instalado 'openpyxl' (pip install openpyxl)
                df = pd.read_excel(archivo)

            elif archivo.name.endswith(".json"):
                df = pd.read_json(archivo)

            elif archivo.name.endswith(".xml"):
                # Nota: Requiere tener instalado 'lxml' (pip install lxml)
                df = pd.read_xml(archivo)

            else:
                st.error("Formato no soportado.")
                st.stop()

            # Si todo sale bien, mostramos el éxito y el DataFrame
            st.success("¡Archivo cargado correctamente!")
            st.dataframe(df, use_container_width=True)

        except ModuleNotFoundError as e:
            # Captura específica por si faltan librerías en tu entorno Python
            st.error(f"Falta una librería necesaria para leer este formato: {e}. "
                     "Asegúrate de instalar `openpyxl` para Excel o `lxml` para XML.")
        except Exception as e:
            # Captura cualquier otro error de formato o lectura
            st.error(f"Error al leer el archivo: {e}")