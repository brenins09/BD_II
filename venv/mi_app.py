import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Título de la aplicación
st.title("Unir dos archivos CSV y cargarlos en la base de datos")

# Cargar los archivos CSV
st.write("Sube dos archivos CSV para combinarlos en un DataFrame.")

# Subir archivos CSV
archivo_1 = st.file_uploader("Sube el primer archivo CSV", type="csv")
archivo_2 = st.file_uploader("Sube el segundo archivo CSV", type="csv")

# Si ambos archivos están cargados
if archivo_1 is not None and archivo_2 is not None:
    # Leer los archivos CSV como DataFrames
    df1 = pd.read_csv(archivo_1)
    df2 = pd.read_csv(archivo_2)

    # Mostrar los DataFrames originales
    st.write("Primer archivo CSV:")
    st.dataframe(df1)

    st.write("Segundo archivo CSV:")
    st.dataframe(df2)

    # Unificar los DataFrames por columnas (uno al lado del otro)
    df_unificado = pd.concat([df1, df2], axis=1)

    # Mostrar el DataFrame unificado
    st.write("DataFrame unificado:")
    st.dataframe(df_unificado)

    # Descargar CSV unificado
    csv_unificado = df_unificado.to_csv(index=False).encode('utf-8')
    st.download_button(label="Descargar CSV unificado", data=csv_unificado, file_name='unificado.csv', mime='text/csv')

    # Conectar a la base de datos local MySQL
    engine = create_engine('mysql+mysqlconnector://root:Brenins.123@localhost/miapp')

    # Cargar el DataFrame unificado en la tabla "data_credibanco"
    try:
        df_unificado.to_sql('data_credibanco', con=engine, if_exists='append', index=False)
        st.write("El DataFrame unificado ha sido cargado exitosamente en la base de datos.")
    except Exception as e:
        st.write("Error al cargar el DataFrame en la base de datos:")
        st.write(e)
