import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Настройка страницы
st.set_page_config(page_title="Market Optimizer Pro", layout="wide")

# Выбор языка
lang = st.sidebar.selectbox("Language / Dil", ["Русский", "Türkmençe"])

if lang == "Русский":
    t = {
        "title": "📊 Оптимизатор Рынка (Парфюмерия)",
        "settings": "Настройки бизнеса",
        "price": "Ваша цена продажи (TMT)",
        "cost": "Цена закупки ($)",
        "shipping": "Доставка за единицу ($)",
        "competitor": "Цена конкурента (TMT)",
        "results": "Результаты симуляции",
        "sales": "Прогноз продаж",
        "profit": "Ожидаемая прибыль",
        "margin": "Маржинальность",
        "chart_title": "Анализ потенциальных покупателей"
    }
else:
    t = {
        "title": "📊 Bazar Optimizatory (Parfümeriýa)",
        "settings": "Biznes sazlamalary",
        "price": "Satuw bahasy (TMT)",
        "cost": "Satyn alyş bahasy ($)",
        "shipping": "Eltip berme çykdajysy ($)",
        "competitor": "Bäsdeşiň bahasy (TMT)",
        "results": "Simulýasiýanyň netijeleri",
        "sales": "Satuw prognozy",
        "profit": "Garaşylýan peýda",
        "margin": "Rentabellik",
        "chart_title": "Potensial alyjylaryň seljermesi"
    }

st.title(t["title"])

# Боковая панель
st.sidebar.header(t["settings"])
user_price = st.sidebar.slider(t["price"], 50, 1500, 350)
buy_price_usd = st.sidebar.number_input(t["cost"], value=25.0)
shipping_usd = st.sidebar.number_input(t["shipping"], value=5.0)
comp_price = st.sidebar.slider(t["competitor"], 50, 1500, 400)

# Экономика (условный курс 20 TMT за 1$)
exchange_rate = 20 
total_cost_tmt = (buy_price_usd + shipping_usd) * exchange_rate

# Симуляция 10,000 агентов
np.random.seed(42)
df = pd.DataFrame({
    'income': np.random.normal(3000, 1000, 10000), # Доходы населения
    'brand_love': np.random.uniform(0, 1, 10000)   # Лояльность
})

# Логика покупки (учитываем цену, доход и конкурента)
df['will_buy'] = (df['income'] > user_price * 2) & \
                 (user_price < comp_price * 1.1) & \
                 (df['brand_love'] > 0.3)

# Расчеты
total_sales = df['will_buy'].sum()
total_revenue = total_sales * user_price
total_profit = total_sales * (user_price - total_cost_tmt)
margin = ((user_price - total_cost_tmt) / user_price) * 100 if user_price > 0 else 0

# Вывод метрик
col1, col2, col3 = st.columns(3)
col1.metric(t["sales"], f"{total_sales} шт.")
col2.metric(t["profit"], f"{int(total_profit)} TMT")
col3.metric(t["margin"], f"{int(margin)}%")

# График
fig = px.histogram(df, x="income", color="will_buy", 
                   title=t["chart_title"],
                   color_discrete_map={True: "#00CC96", False: "#EF553B"})
st.plotly_chart(fig, use_container_width=True)

if total_profit > 0:
    st.success("✅ Бизнес-модель прибыльна")
else:
    st.error("⚠️ Убыточная модель. Нужно снизить затраты или поднять цену.")
