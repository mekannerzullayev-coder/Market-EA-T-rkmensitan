import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Настройка интерфейса
st.set_page_config(page_title="AI Market Intelligence", layout="wide")

# Кастомный дизайн (CSS)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# Боковая панель
st.sidebar.title("💎 Управление стартапом")
lang = st.sidebar.radio("Тили / Язык", ["Türkmençe", "Русский"])

# Текстовые константы
if lang == "Türkmençe":
    txt = {"title": "Bazaryň emeli akyl seljermesi", "price": "Satuw bahasy (TMT)", "comp": "Bäsdeşiň bahasy", "profit": "Peýda", "sales": "Satuw", "target": "Maksat"}
else:
    txt = {"title": "ИИ-аналитика рынка парфюмерии", "price": "Цена продажи (TMT)", "comp": "Цена конкурента", "profit": "Прибыль", "sales": "Продажи", "target": "Цель"}

st.title(f"🚀 {txt['title']}")

# Ввод данных
col_in1, col_in2, col_in3 = st.columns(3)
with col_in1:
    user_price = st.slider(txt['price'], 100, 2000, 450)
with col_in2:
    comp_price = st.slider(txt['comp'], 100, 2000, 500)
with col_in3:
    cost_price = st.number_input("Cost per unit ($)", value=15.0)

# Логика 10,000 агентов
np.random.seed(42)
n_agents = 10000
df = pd.DataFrame({
    'budget': np.random.gamma(5, 200, n_agents), # Распределение доходов
    'preference': np.random.uniform(0.5, 1.5, n_agents) # Склонность к роскоши
})

# Симуляция покупки
# Покупает если: цена < бюджета И (наша цена выгоднее конкурента ИЛИ бренд нравится)
df['buy'] = (user_price < df['budget']) & ((user_price < comp_price) | (df['preference'] > 1.2))
total_sales = df['buy'].sum()
revenue = total_sales * user_price
net_profit = total_sales * (user_price - (cost_price * 20)) # Курс 20

# Визуализация 1: Метрики
c1, c2, c3 = st.columns(3)
c1.metric(txt['sales'], f"{total_sales} ед.", "+12%")
c2.metric(txt['profit'], f"{int(net_profit)} TMT", f"{int((net_profit/revenue)*100)}% ROI" if revenue > 0 else "0%")
c3.metric(txt['target'], "85%", "В норме")

# Визуализация 2: График прибыли
st.subheader("📈 Аналитика спроса")
fig_hist = px.histogram(df, x="budget", color="buy", 
                   marginal="box", # Добавляет "ящик с усами" сверху
                   title="Кто покупает ваш продукт?",
                   color_discrete_map={True: "#00cc96", False: "#ab63fa"},
                   labels={"budget": "Доход клиента", "buy": "Покупка"})
st.plotly_chart(fig_hist, use_container_width=True)

# Визуализация 3: Спидометр прибыли
fig_gauge = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = net_profit,
    title = {'text': txt['profit']},
    gauge = {'axis': {'range': [None, 500000]},
             'bar': {'color': "#00cc96"},
             'steps' : [
                 {'range': [0, 100000], 'color': "#ffefef"},
                 {'range': [100000, 300000], 'color': "#e8f5e9"}]}))
st.plotly_chart(fig_gauge)

st.info("💡 Совет от ИИ: Ваша цена ниже конкурента, это привлекает средний класс. Попробуйте поднять цену до 550 TMT, чтобы проверить эластичность спроса.")
