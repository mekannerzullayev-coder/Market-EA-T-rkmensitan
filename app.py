import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_folium import st_folium
import folium
import google.generativeai as genai

# --- ИНТЕГРАЦИЯ GEMINI ---
# Твой ключ вставлен сюда
genai.configure(api_key="AIzaSyDtpFdOzDLdkM3-S8mJGK8ZtEUMrWl93Zw")
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_analysis(product, origin, cost, price, sales, margin, roi):
    prompt = f"""
    Ты опытный бизнес-аналитик из Кремниевой долины. 
    Проанализируй следующие данные для предпринимателя из Туркменистана:
    - Товар: {product}
    - Маршрут: {origin} -> Ашхабад
    - Себестоимость (закупка+логистика): {int(cost)} TMT
    - Цена продажи: {price} TMT
    - Чистая прибыль с единицы: {int(margin)} TMT
    - Рентабельность (ROI): {int(roi)}%
    - Потенциальные продажи: {sales} чел. из 10,000 охваченных.

    Дай короткий (3-4 предложения), профессиональный и конкретный совет на русском языке. 
    Стоит ли запускать этот бизнес? На что обратить внимание?
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Ошибка связи с ИИ: {str(e)}"

# --- НАСТРОЙКИ ИНТЕРФЕЙСА (VIBE STYLE) ---
st.set_page_config(page_title="Gemini Market Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: white; }
    div[data-testid="stMetric"] { 
        background: rgba(255, 255, 255, 0.05); 
        border: 1px solid #30363D; 
        border-radius: 20px; 
        padding: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
        color: white; border: none; border-radius: 12px; width: 100%; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Gemini AI Business Intelligence")
st.markdown("##### Аналитическая платформа с искусственным интеллектом")

# --- БЛОК ВВОДА ДАННЫХ ---
with st.container():
    col_input1, col_input2, col_input3 = st.columns(3)
    with col_input1:
        product_name = st.text_input("📦 Название товара", "Elite Fragrance")
        origin_city = st.selectbox("🌍 Город закупки", ["Dubai (UAE)", "Tashkent (UZB)", "Istanbul (TUR)"])
    with col_input2:
        cost_usd = st.number_input("💵 Закупка ($)", value=25.0)
        shipping_usd = st.number_input("🚛 Доставка ($/ед)", value=5.0)
    with col_input3:
        sale_price_tmt = st.number_input("💰 Цена продажи (TMT)", value=850)
        rate = st.number_input("📊 Курс (1$ = ? TMT)", value=20.0)

# Математическая логика
unit_cost_tmt = (cost_usd + shipping_usd) * rate
unit_margin = sale_price_tmt - unit_cost_tmt
roi = (unit_margin / unit_cost_tmt) * 100 if unit_cost_tmt > 0 else 0

# Симуляция рынка (10,000 агентов)
np.random.seed(42)
market_data = pd.DataFrame({'budget': np.random.normal(5000, 1800, 10000)})
potential_sales = len(market_data[market_data['budget'] > sale_price_tmt])

# --- ВЫВОД МЕТРИК ---
st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Прогноз продаж", f"{potential_sales}", "из 10,000 чел.")
m2.metric("Чистая прибыль/ед", f"{int(unit_margin)} TMT")
m3.metric("Рентабельность", f"{int(roi)}%")
m4.metric("Общая прибыль", f"{int(potential_sales * unit_margin):,} TMT")

st.divider()

# --- СЕКЦИЯ GEMINI И ВИЗУАЛИЗАЦИИ ---
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("🤖 Анализ от Gemini AI")
    if st.button("Сгенерировать бизнес-совет"):
        with st.spinner('Нейросеть анализирует ваш рынок...'):
            advice = get_gemini_analysis(product_name, origin_city, unit_cost_tmt, sale_price_tmt, potential_sales, unit_margin, roi)
            st.info(advice)
    
    # Карта
    st.markdown("---")
    st.markdown(f"**Маршрут:** {origin_city} ✈️ Ашхабад")
    m = folium.Map(location=[35, 55], zoom_start=4, tiles="CartoDB dark_matter")
    st_folium(m, width="100%", height=300)

with col_right:
    st.subheader("📊 Глубина рынка")
    fig = px.area(market_data.sort_values('budget'), x='budget', template="plotly_dark")
    fig.update_traces(line_color='#7C3AED', fillcolor='rgba(124, 58, 237, 0.2)')
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=400)
    st.plotly_chart(fig, use_container_width=True)
    
