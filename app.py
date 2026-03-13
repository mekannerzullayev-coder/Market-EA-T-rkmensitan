import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_folium import st_folium
import folium

# Настройка в стиле Modern Tech
st.set_page_config(page_title="Market Engine AI", layout="wide")

# Применяем стиль "Modern Dark" через CSS
st.markdown("""
    <style>
    /* Главный фон */
    .main { background-color: #0E1117; color: #ffffff; }
    
    /* Карточки метрик */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Заголовки */
    h1, h2, h3 { font-family: 'Inter', sans-serif; letter-spacing: -1px; }
    
    /* Сайдбар */
    section[data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
    
    /* Кнопки */
    .stButton>button {
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
        color: white; border: none; border-radius: 12px; font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50) # Иконка ракеты
    st.title("Console")
    st.caption("Market Intelligence v3.0")
    
    st.subheader("Control Center")
    user_price = st.slider("Target Price (TMT)", 100, 2500, 850)
    route = st.select_slider("Logistics Hub", options=["Dubai Hub", "Tashkent Hub"])
    
    st.divider()
    if st.button("Generate Insight"):
        st.toast("AI is analyzing the market...")

# --- MAIN PAGE ---
st.title("⚡ Market Intelligence")
st.markdown("##### Simulation for: `High-End Fragrance` | Batch: `2026-A`")

# Логика расчета
np.random.seed(42)
data = pd.DataFrame({'val': np.random.normal(5000, 1200, 10000)})
sold = data[data['val'] > user_price]
reach = len(sold)
revenue = reach * user_price

# 1. Секция Top Metrics (как в крипто-кошельках)
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Potential Reach", f"{reach}", "10k agents")
with c2:
    st.metric("Est. Revenue", f"{revenue:,} TMT", "+$1.2k", delta_color="normal")
with c3:
    st.metric("Efficiency", "94.2%", "Optimized", delta_color="off")

st.write("") # Отступ

# 2. Визуализация (Карта и Аналитика)
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown("### Logistics Network")
    # Тёмная карта (CartoDB Dark Matter)
    m = folium.Map(location=[32, 62], zoom_start=4, tiles="CartoDB dark_matter")
    
    # Красивая светящаяся линия
    locations = {"Dubai": [25.2, 55.2], "Ashgabat": [37.9, 58.3]}
    folium.PolyLine(list(locations.values()), color="#7C3AED", weight=4, opacity=0.9).add_to(m)
    
    # Кастомные маркеры
    folium.CircleMarker(locations["Dubai"], radius=8, color="#4F46E5", fill=True).add_to(m)
    folium.CircleMarker(locations["Ashgabat"], radius=10, color="#EF4444", fill=True).add_to(m)
    
    st_folium(m, width="100%", height=400)

with col_right:
    st.markdown("### Market Depth")
    # Прозрачный современный график
    fig = px.area(data.sort_values('val'), x='val', 
                 title=None, template="plotly_dark")
    fig.update_traces(line_color='#7C3AED', fillcolor='rgba(124, 58, 237, 0.2)')
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=350)
    st.plotly_chart(fig, use_container_width=True)

# 3. AI Insights (Нижняя панель)
st.markdown("---")
st.warning("🤖 **AI Insights:** High demand detected in the 800-950 TMT range. Moving price higher might trigger a 15% drop in volume but a 5% increase in net profit.")
