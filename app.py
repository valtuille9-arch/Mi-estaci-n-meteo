
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SAN ROMÁN DE LA VEGA", page_icon="🌤️", layout="wide")

# SUSTITUYE AQUÍ TUS CREDENCIALES
STATION_ID = "ISANJUST8"
API_KEY = "1cb031dea0a440a9b031dea0a400a91f"

# --- FUNCIONES DE DATOS ---
def get_current_weather():
    url = f"https://api.weather.com/v2/pws/observations/current?stationId={STATION_ID}&format=json&units=m&apiKey={API_KEY}"
    response = requests.get(url)
    return response.json()['observations'][0]

def get_history_weather():
    # Obtenemos los datos de hoy (últimas 24h aprox)
    url = f"https://api.weather.com/v2/pws/observations/all/1day?stationId={STATION_ID}&format=json&units=m&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    # Convertimos a DataFrame para graficar fácilmente
    df = pd.json_normalize(data['observations'])
    df['obsTimeLocal'] = pd.to_datetime(df['obsTimeLocal'])
    return df

# --- INTERFAZ DE LA APP ---
st.title(f"📊 Estación: {STATION_ID}")

try:
    # 1. Obtener datos actuales
    obs = get_current_weather()
    m = obs['metric']

    # 2. Mostrar métricas principales en columnas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Temperatura", f"{m['temp']} °C")
    col2.metric("Humedad", f"{obs['humidity']} %")
    col3.metric("Viento", f"{m['windSpeed']} km/h")
    col4.metric("Presión", f"{m['pressure']} hPa")

    st.markdown("---")

    # 3. Gráfica de Historial
    st.subheader("📈 Tendencia de Temperatura (Últimas 24h)")
    df_hist = get_history_weather()
    
    # Creamos una gráfica interactiva
    fig = px.line(df_hist, x='obsTimeLocal', y='metric.temp', 
                  labels={'obsTimeLocal': 'Hora', 'metric.temp': 'Temp (°C)'},
                  template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.caption(f"Última actualización: {obs['obsTimeLocal']}")

except Exception as e:
    st.error("⚠️ No se pudieron cargar los datos. Revisa tu Station ID y API Key.")
    st.info("Asegúrate de que tu estación esté enviando datos a Weather Underground ahora mismo.")

# Botón de refresco manual
if st.sidebar.button('🔄 Actualizar Datos'):
    st.rerun()