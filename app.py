import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_folium import st_folium
import folium
import google.generativeai as genai

# --- ИНТЕГРАЦИЯ GEMINI ---
# Твой новый ключ
genai.configure(api_key="AIzaSyAjDrEkJdmMANfoCpJPd3AhahMBzELPWEA")
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_analysis(product, origin, cost, price, sales, margin, roi):
    prompt = f"""
    Ты бизнес-аналитик. Проанализируй данные для стартапа:
    Товар: {product}
    Закупка в: {origin}
    Себестоимость: {int(cost)} TMT, Цена продажи: {price} TMT
    Чистая прибыль: {int(margin)} TMT (ROI: {int(roi)}%)
    Прогноз продаж: {sales} из 10,000.
    Дай конкретный совет: стоит ли это запускать и какие главные риски?
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Ошибка Gemini: {str(e)}. Проверь, включен ли API ключ в Google AI Studio."

# --- ИНТЕРФЕЙС ---
st.set_page_config(page_title="AI Market Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: white; }
    div[data-testid="stMetric"] { background: rgba(255, 255, 255, 0.05); border: 1px solid #30363D; border-radius: 15px; padding: 15px; }
    .stButton>button { background: #4F46E5; color: white; border-radius: 10px; width: 100%; height: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Gemini AI Business Engine")

# Ввод данных
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        product_name = st.text_input("📦 Товар", "Smart Watch")
        origin_city = st.selectbox("🌍 Локация", ["Dubai", "Tashkent", "Istanbul"])
    with col2:
        cost_usd = st.number_input("Закупка ($)", value=20.0)
        ship_usd = st.number_input("Доставка ($)", value=4.0)
    with col3:
        price_tmt = st.number_input("Цена (TMT)", value=700)
        rate = st.number_input("Курс $", value=20.0)

# Экономика
unit_cost = (cost_usd + ship_usd) * rate
unit_margin = price_tmt - unit_cost
roi = (unit_margin / unit_cost) * 100 if unit_cost > 0 else 0

np.random.seed(42)
market = pd.DataFrame({'budget': np.random.normal(4500, 1500, 10000)})
sales = len(market[market['budget'] > price_tmt])

# Метрики
st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Прогноз продаж", f"{sales}")
m2.metric("Прибыль/ед", f"{int(unit_margin)} TMT")
m3.metric("ROI", f"{int(roi)}%")
m4.metric("Общая прибыль", f"{int(sales * unit_margin):,} TMT")

st.divider()

# Кнопка и Ответ AI
if st.button("🤖 ПОЛУЧИТЬ АНАЛИЗ GEMINI"):
    with st.spinner('Связываюсь с нейросетью...'):
        advice = get_gemini_analysis(product_name, origin_city, unit_cost, price_tmt, sales, unit_margin, roi)
        st.markdown("### 📝 Вердикт ИИ:")
        st.info(advice)

# Карта
st.subheader("Карта маршрута")
m = folium.Map(location=[35, 55], zoom_start=4, tiles="CartoDB dark_matter")
st_folium(m, width="100%", height=300)
