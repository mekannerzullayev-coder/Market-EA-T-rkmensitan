import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Интерфейс
st.title("🚀 AI Market Optimizer (Turkmenistan)")
st.write("Симуляция рынка на 10,000 агентов")

# Настройки в боковой панели
price = st.sidebar.slider("Ваша цена (TMT)", 10, 500, 150)

# Простая логика
data = pd.DataFrame({
    'income': np.random.normal(2000, 500, 10000),
    'buy': np.random.choice([True, False], 10000)
})

# График
fig = px.histogram(data, x="income", color="buy", title="Анализ покупателей")
st.plotly_chart(fig)

st.success("Приложение работает!")
