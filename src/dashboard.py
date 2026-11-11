"""
Dashboard Streamlit: visualização das leituras de temperatura IoT
armazenadas no PostgreSQL (via views SQL).
"""
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

# ---------- Configuração da página ----------
st.set_page_config(page_title="Dashboard IoT", page_icon="🌡️", layout="wide")

# ---------- Conexão com o banco ----------
DB_URL = "postgresql+psycopg2://postgres:bruno123@localhost:5432/postgres"
engine = create_engine(DB_URL)


@st.cache_data(ttl=300)
def load_data(query: str) -> pd.DataFrame:
    """Executa uma consulta SQL e devolve um DataFrame."""
    return pd.read_sql(query, engine)


# ---------- Título ----------
st.title("🌡️ Dashboard de Temperaturas IoT")
st.caption("Leituras de sensores de temperatura (Kaggle) processadas com "
           "Python, Docker, PostgreSQL e Streamlit.")

# ---------- Carga dos dados ----------
df_avg = load_data("SELECT * FROM avg_temp_por_dispositivo")
df_hora = load_data("SELECT * FROM leituras_por_hora")
df_dia = load_data("SELECT * FROM temp_max_min_por_dia")
df_resumo = load_data(
    "SELECT COUNT(*) AS total, "
    "ROUND(AVG(temperature)::numeric, 1) AS media, "
    "MAX(temperature) AS maxima, "
    "MIN(temperature) AS minima "
    "FROM temperature_readings"
)

# ---------- Indicadores gerais ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total de leituras", f"{int(df_resumo['total'][0]):,}".replace(",", "."))
c2.metric("Temperatura média", f"{df_resumo['media'][0]} °C")
c3.metric("Temperatura máxima", f"{df_resumo['maxima'][0]} °C")
c4.metric("Temperatura mínima", f"{df_resumo['minima'][0]} °C")

st.divider()

# ---------- Gráfico 1: média por dispositivo ----------
st.header("Média de Temperatura por Dispositivo")
fig1 = px.bar(
    df_avg,
    x="device_id",
    y="avg_temp",
    color="location",
    barmode="group",
    text="avg_temp",
    labels={"device_id": "Dispositivo", "avg_temp": "Temperatura média (°C)",
            "location": "Local"},
)
st.plotly_chart(fig1, use_container_width=True)

# ---------- Gráfico 2: leituras por hora ----------
st.header("Leituras por Hora do Dia")
fig2 = px.line(
    df_hora,
    x="hora",
    y="contagem",
    markers=True,
    labels={"hora": "Hora do dia", "contagem": "Nº de leituras"},
)
st.plotly_chart(fig2, use_container_width=True)

# ---------- Gráfico 3: máximas e mínimas por dia ----------
st.header("Temperaturas Máximas e Mínimas por Dia")
fig3 = px.line(
    df_dia,
    x="data",
    y=["temp_max", "temp_min"],
    labels={"data": "Data", "value": "Temperatura (°C)", "variable": "Medida"},
)
st.plotly_chart(fig3, use_container_width=True)

# ---------- Tabela de apoio ----------
with st.expander("Ver dados diários (tabela)"):
    st.dataframe(df_dia, use_container_width=True)