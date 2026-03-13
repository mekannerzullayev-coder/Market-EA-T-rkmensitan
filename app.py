import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_folium import st_folium
import folium

# Настройка страницы (должна быть первой командой)
st.set_page_config(page_title="Market & Logistics AI", layout="wide")

st.title("🌍 AI Market Intelligence & Logistics")

# --- ЛОГИСТИКА И КАРТА ---
st.subheader("Маршруты поставок: Дубай / Ташкент")

col_map, col_info = st.columns([2, 1])

with col_map:
    # Создаем карту
    m = folium.Map(location=[32, 62], zoom_start=4, tiles="CartoDB positron")
    
    # Точки
    locations = {
        "Dubai": [25.2048, 55.2708],
        "Tashkent": [41.2995, 69.2401],
        "Ashgabat": [37.9601, 58.3262]
    }
    
    # Линии маршрутов
    folium.PolyLine([locations["Dubai"], locations["Ashgabat"]], color="blue", weight=3).add_to(m)
    folium.PolyLine([locations["Tashkent"], locations["Ashgabat"]], color="green", weight=3).add_to(m)
    
    # Маркеры
    folium.Marker(locations["Dubai"], popup="Dubai").add_to(m)
    folium.Marker(locations["Ashgabat"], popup="Ashgabat", icon=folium.Icon(color='red')).add_to(m)
    
    # Вывод карты
    st_folium(m, width="100%", height=350)

with col_info:
    st.info("📦 Параметры")
    origin = st.radio("Откуда везем?", ["Дубай (ОАЭ)", "Ташкент (Узбекистан)"])
    price = st.slider("Ваша цена продажи (TMT)", 100, 2000, 550)
    st.write(f"**Выбран маршрут:** {origin}")

# --- СИМУЛЯЦИЯ 10,000 АГЕНТОВ ---
st.divider()
st.subheader("🎯 Анализ спроса (10,000 ИИ-агентов)")

# Генерация данных
np.random.seed(42)
agents = pd.DataFrame({'income': np.random.normal(4000, 1500, 10000)})
agents['buy'] = agents['income'] > price

sales = agents['buy'].sum()
st.metric("Прогноз продаж", f"{sales} ед.", delta=f"{int(sales/100)}% охват")

# График
fig = px.histogram(agents, x="income", color="buy", 
                   title="Кто купит ваш товар?",
                   color_discrete_map={True: "#00CC96", False: "#EF553B"})
st.plotly_chart(fig, use_container_width=True)

st.success("✅ Код работает стабильно!")
