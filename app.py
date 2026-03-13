import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_folium import st_folium
import folium

# Настройка страницы
st.set_page_config(page_title="Market Engine AI", layout="wide")

# Темная тема и стилистика
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #ffffff; }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
    }
    section[data-testid="stSidebar"] { background-color: #161B22; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Все твои настройки здесь) ---
with st.sidebar:
    st.title("🕹️ Control Center")
    
    st.subheader("📦 Product Info")
    product_name = st.text_input("Название товара", "Luxury Fragrance")
    
    st.subheader("💰 Economics")
    buy_price_usd = st.number_input("Цена закупки ($)", value=25.0)
    target_price_tmt = st.slider("Цена продажи (TMT)", 100, 3000, 850)
    
    st.subheader("🚛 Logistics")
    origin = st.selectbox("Откуда везем?", ["Dubai (UAE)", "Tashkent (UZB)"])
    shipping_speed = st.select_slider("Скорость доставки", options=["Economy", "Standard", "Express"])
    
    st.divider()
    generate = st.button("Generate Insight", use_container_width=True)

# --- МАТЕМАТИКА БИЗНЕСА ---
# Курс доллара возьмем условно 20
exchange_rate = 20
shipping_cost = 8.0 if origin == "Dubai (UAE)" else 4.0
if shipping_speed == "Express": shipping_cost *= 1.5

total_cost_tmt = (buy_price_usd + shipping_cost) * exchange_rate

# Симуляция 10,000 агентов
np.random.seed(42)
data = pd.DataFrame({'val': np.random.normal(5000, 1500, 10000)})
sold_count = len(data[data['val'] > target_price_tmt])
net_profit = sold_count * (target_price_tmt - total_cost_tmt)

# --- ИНТЕРФЕЙС ---
st.title("⚡ Market Intelligence")
st.markdown(f"##### Анализ для: `{product_name}` | Маршрут: `{origin}`")

# Метрики
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Potential Sales", f"{sold_count} ед.")
with c2:
    st.metric("Net Profit", f"{int(net_profit):,} TMT", "Estimated")
with c3:
    st.metric("Cost per Unit", f"{int(total_cost_tmt)} TMT", "incl. Logistics")

st.write("") 

# Карта и График
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown("### Supply Chain Visualizer")
    m = folium.Map(location=[32, 62], zoom_start=4, tiles="CartoDB dark_matter")
    
    locations = {
        "Dubai (UAE)": [25.2, 55.2],
        "Tashkent (UZB)": [41.3, 69.2],
        "Ashgabat": [37.9, 58.3]
    }
    
    start_coords = locations[origin]
    end_coords = locations["Ashgabat"]
    
    folium.PolyLine([start_coords, end_coords], color="#7C3AED", weight=4, opacity=0.8).add_to(m)
    folium.CircleMarker(start_coords, radius=8, color="#4F46E5", fill=True, popup=origin).add_to(m)
    folium.CircleMarker(end_coords, radius=10, color="#EF4444", fill=True, popup="Market").add_to(m)
    
    st_folium(m, width="100%", height=400)

with col_right:
    st.markdown("### Price Strategy")
    fig = px.histogram(data, x='val', nbins=50, template="plotly_dark")
    fig.add_vline(x=target_price_tmt, line_dash="dash", line_color="#EF4444", annotation_text="Your Price")
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=350)
    st.plotly_chart(fig, use_container_width=True)

# Нижняя панель
st.info(f"🤖 **AI Strategy:** Для товара '{product_name}' при закупке в ${buy_price_usd}, ваша маржа составляет {int(target_price_tmt - total_cost_tmt)} TMT. Рекомендуем держать цену не выше {int(target_price_tmt * 1.1)} TMT для сохранения охвата.")
    
