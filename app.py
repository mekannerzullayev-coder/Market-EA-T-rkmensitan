import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_folium import st_folium
import folium

# Конфигурация страницы
st.set_page_config(page_title="Market Engine AI", layout="wide")

# Кастомный CSS для стиля "High-Tech Dark"
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: white; }
    div[data-testid="stMetric"] { 
        background: rgba(255, 255, 255, 0.05); 
        border: 1px solid #30363D; 
        border-radius: 15px; 
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #161B22; color: white; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("⚡ Market Intelligence Dashboard")

# Блок основных параметров продукта
with st.container():
    st.subheader("📦 Параметры бизнеса")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        product_name = st.text_input("Название продукта", "Perfume Elite")
        origin_city = st.selectbox("Откуда доставка", ["Dubai (UAE)", "Tashkent (UZB)", "Istanbul (TUR)"])
    
    with col2:
        cost_usd = st.number_input("Закупка за ед. ($)", value=20.0)
        shipping_usd = st.number_input("Доставка за ед. ($)", value=5.0)
        
    with col3:
        target_price_tmt = st.number_input("Цена продажи (TMT)", value=800)
        exchange_rate = st.number_input("Курс (1$ в TMT)", value=20.0)

# Математические расчеты
total_cost_tmt = (cost_usd + shipping_usd) * exchange_rate
margin_tmt = target_price_tmt - total_cost_tmt
roi = (margin_tmt / total_cost_tmt) * 100 if total_cost_tmt > 0 else 0
# Симуляция рынка (10,000 виртуальных покупателей)
np.random.seed(42)
market_data = pd.DataFrame({'budget': np.random.normal(4500, 1500, 10000)})
buyers = market_data[market_data['budget'] > target_price_tmt]
sales_count = len(buyers)
total_profit = sales_count * margin_tmt

st.write("") # Отступ
m1, m2, m3, m4 = st.columns(4)
m1.metric("Прогноз продаж", f"{sales_count} ед.", "из 10,000")
m2.metric("Чистая прибыль", f"{int(total_profit):,} TMT")
m3.metric("Маржа с единицы", f"{int(margin_tmt)} TMT", f"{int(roi)}% ROI")
m4.metric("Себестоимость", f"{int(total_cost_tmt)} TMT")
st.divider()
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown(f"### 🌍 Логистика: {origin_city} → Ашхабад")
    
    # Координаты для карты
    coords = {
        "Dubai (UAE)": [25.2, 55.2],
        "Tashkent (UZB)": [41.3, 69.2],
        "Istanbul (TUR)": [41.0, 28.9],
        "Ashgabat": [37.9, 58.3]
    }
    
    m = folium.Map(location=[35, 50], zoom_start=4, tiles="CartoDB dark_matter")
    start = coords[origin_city]
    end = coords["Ashgabat"]
    
    folium.PolyLine([start, end], color="#7C3AED", weight=4).add_to(m)
    folium.Marker(start, popup=origin_city).add_to(m)
    folium.Marker(end, popup="Ашхабад", icon=folium.Icon(color='red')).add_to(m)
    
    st_folium(m, width="100%", height=400)

with col_right:
    st.markdown("### 📊 Анализ аудитории")
    fig = px.area(market_data.sort_values('budget'), x='budget', template="plotly_dark")
    fig.update_traces(line_color='#7C3AED', fillcolor='rgba(124, 58, 237, 0.2)')
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=350)
    st.plotly_chart(fig, use_container_width=True)

# AI Фидбек
st.info(f"🤖 **AI Анализ:** Для товара '{product_name}' при цене {target_price_tmt} TMT вы получаете высокую маржу. Рекомендуем обратить внимание на сроки доставки из {origin_city}.")
