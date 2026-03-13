import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3
from datetime import datetime
from streamlit_folium import st_folium
import folium

# Настройка страницы
st.set_page_config(page_title="AI Market & Logistics Pro", layout="wide")

# Инициализация базы данных (как в прошлом шаге)
def init_db():
    conn = sqlite3.connect('market_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS simulations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, product_name TEXT, price REAL, profit REAL, sales INTEGER)''')
    conn.commit()
    conn.close()

init_db()

st.title("🌍 AI Market Optimizer + Logistics Map")

# --- БЛОК ЛОГИСТИКИ И КАРТЫ ---
st.subheader("Маршрут поставки и логистика")

col_map, col_details = st.columns([2, 1])

with col_map:
    # Создаем карту с центром между ОАЭ и Туркменистаном
    m = folium.Map(location=[20, 55], zoom_start=4, tiles="CartoDB positron")
    
    # Координаты городов
    dubai = [25.2048, 55.2708]
    ashgabat = [37.9601, 58.3262]
    tashkent = [41.2995, 69.2401]
    
    # Рисуем линии маршрутов
    folium.PolyLine([dubai, ashgabat], color="blue", weight=3, opacity=0.7, tooltip="Dubai -> Ashgabat").add_to(m)
    folium.PolyLine([tashkent, ashgabat], color="green", weight=3, opacity=0.7, tooltip="Tashkent -> Ashgabat").add_to(m)
    
    # Добавляем маркеры
    folium.Marker(dubai, popup="Dubai (Закупка)", icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)
    folium.Marker(ashgabat, popup="Ashgabat (Рынок)", icon=folium.Icon(color='red', icon='home')).add_to(m)
    folium.Marker(tashkent, popup="Tashkent (Склад)", icon=folium.Icon(color='green')).add_to(m)
    
    # Отображаем карту в Streamlit
    st_folium(m, width=700, height=400)

with col_details:
    st.info("📊 Информация о маршруте")
    origin = st.selectbox("Откуда везем?", ["Дубай (ОАЭ)", "Ташкент (Узбекистан)"])
    distance = "~1,600 км" if "Дубай" in origin else "~1,100 км"
    st.write(f"**Дистанция:** {distance}")
    st.write("**Тип транспорта:** Авиа / Наземный")
    days = st.slider("Срок доставки (дни)", 1, 30, 7)

# --- БЛОК СИМУЛЯЦИИ (Твоя логика) ---
st.divider()
with st.sidebar:
    st.header("📦 Параметры")
    product_name = st.text_input("Товар", "Premium Perfume")
    user_price = st.slider("Цена (TMT)", 100, 2000, 600)
    if st.button("💾 Сохранить расчет"):
        # Функция сохранения (уже есть в твоем коде)
        st.success("Сохранено!")

# Симуляция 10,000 агентов
np.random.seed(42)
df_sim = pd.DataFrame({'budget': np.random.normal(5000, 2000, 10000), 'buy': np.random.choice([True, False], 10000)})
df_sim['buy'] = (user_price < df_sim['budget'])

st.subheader("Результаты анализа рынка")
fig = px.pie(df_sim, names='buy', title="Доля охвата рынка", color_discrete_sequence=['#00CC96', '#EF553B'])
st.plotly_chart(fig, use_container_width=True)
    
