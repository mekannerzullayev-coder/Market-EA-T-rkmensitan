import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_folium import st_folium
import folium

# Настройка страницы в стиле Dashboard
st.set_page_config(page_title="Market Intel Pro", layout="wide", initial_sidebar_state="expanded")

# Кастомный CSS для "дорогого" вида
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #1f2937; }
    div[data-testid="stMetricDelta"] { font-size: 16px; }
    .stPlotlyChart { border-radius: 15px; overflow: hidden; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Настройки) ---
with st.sidebar:
    st.title("💎 Global Logistics")
    st.subheader("Product Settings")
    product_name = st.text_input("Product Name", "Luxury Fragrance")
    user_price = st.slider("Retail Price (TMT)", 100, 3000, 750)
    
    st.divider()
    st.subheader("Logistics")
    route = st.selectbox("Shipping Route", ["Dubai ✈️ Ashgabat", "Tashkent 🚛 Ashgabat"])
    cost_usd = st.number_input("Unit Cost (USD)", value=25.0)
    
    st.divider()
    st.caption("v2.4 | Powered by AI Market Engines")

# --- MAIN INTERFACE ---
st.title("Market Intelligence Dashboard")
st.write(f"Real-time simulation for **{product_name}**")

# Расчеты (Бизнес-логика)
np.random.seed(42)
agents = pd.DataFrame({'income': np.random.gamma(5, 1000, 10000)})
agents['buy'] = agents['income'] > user_price

total_sales = int(agents['buy'].sum())
delivery_fee = 10.0 if "Dubai" in route else 4.0
margin_per_unit = user_price - ((cost_usd + delivery_fee) * 20)
total_profit = total_sales * margin_per_unit

# 1. Секция KPI (Метрики как в Stripe/Shopify)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Predicted Sales", f"{total_sales} units", "12% 📈")
m2.metric("Market Reach", f"{int(total_sales/100)}%", "Global")
m3.metric("Net Profit", f"{int(total_profit)} TMT", "High Margin" if margin_per_unit > 100 else "Low")
m4.metric("ROI", f"{int((margin_per_unit/user_price)*100)}%", "per unit")

st.divider()

# 2. Секция Визуализации (Карта и График в ряд)
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("Logistics Visualizer")
    # Создаем минималистичную карту
    m = folium.Map(location=[32, 62], zoom_start=4, tiles="CartoDB Positron")
    
    # Координаты
    dubai, tashkent, ashgabat = [25.2, 55.2], [41.3, 69.2], [37.9, 58.3]
    
    if "Dubai" in route:
        folium.PolyLine([dubai, ashgabat], color="#3b82f6", weight=4, opacity=0.8).add_to(m)
        folium.Marker(dubai, icon=folium.Icon(color='blue', icon='plane', prefix='fa')).add_to(m)
    else:
        folium.PolyLine([tashkent, ashgabat], color="#10b981", weight=4, opacity=0.8).add_to(m)
        folium.Marker(tashkent, icon=folium.Icon(color='green', icon='truck', prefix='fa')).add_to(m)
        
    folium.Marker(ashgabat, icon=folium.Icon(color='red', icon='star')).add_to(m)
    
    st_folium(m, width="100%", height=400, returned_objects=[])

with col_right:
    st.subheader("Demand Analysis")
    fig = px.area(agents.sort_values('income'), x='income', y=agents['buy'].astype(int).cumsum(),
                 title="Cumulative Potential Buyers",
                 labels={'income': 'Customer Budget', 'y': 'Total Sales Volume'},
                 color_discrete_sequence=['#3b82f6'])
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

# 3. Интеллектуальный вывод
st.info(f"💡 **AI Suggestion:** At {user_price} TMT, you are capturing the upper-middle class segment. To maximize profit, consider a small price increase to {user_price + 50} TMT.")
    
