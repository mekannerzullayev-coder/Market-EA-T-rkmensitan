import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime

# Настройка страницы
st.set_page_config(page_title="AI Market Intelligence Pro", layout="wide")

# Работа с базой данных
def init_db():
    conn = sqlite3.connect('market_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS simulations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  product_name TEXT,
                  price REAL,
                  profit REAL,
                  sales INTEGER)''')
    conn.commit()
    conn.close()

def save_simulation(name, price, profit, sales):
    conn = sqlite3.connect('market_data.db')
    c = conn.cursor()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO simulations (timestamp, product_name, price, profit, sales) VALUES (?, ?, ?, ?, ?)",
              (ts, name, price, profit, sales))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('market_data.db')
    df = pd.read_sql_query("SELECT timestamp, product_name, price, profit, sales FROM simulations ORDER BY id DESC", conn)
    conn.close()
    return df

init_db()

# Интерфейс
st.title("🚀 AI Market Optimizer + Database")

with st.sidebar:
    st.header("📦 Параметры товара")
    product_name = st.text_input("Название товара", "Parfume Deluxe")
    user_price = st.slider("Цена продажи (TMT)", 100, 2000, 500)
    comp_price = st.slider("Цена конкурента (TMT)", 100, 2000, 550)
    cost_usd = st.number_input("Закупка ($)", value=20.0)
    
    if st.button("💾 Сохранить расчет в базу"):
        # Эти данные вычисляются ниже, берем текущие значения
        save_simulation(product_name, user_price, st.session_state.get('last_profit', 0), st.session_state.get('last_sales', 0))
        st.success("Данные сохранены!")

# Симуляция
np.random.seed(42)
df_sim = pd.DataFrame({
    'budget': np.random.normal(4000, 1500, 10000),
    'quality_need': np.random.uniform(0, 1, 10000)
})

df_sim['buy'] = (user_price < df_sim['budget']) & (user_price < comp_price * 1.1)
total_sales = int(df_sim['buy'].sum())
net_profit = int(total_sales * (user_price - (cost_usd * 20)))

# Сохраняем в состояние для кнопки записи
st.session_state['last_profit'] = net_profit
st.session_state['last_sales'] = total_sales

# Визуализация
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Анализ спроса")
    fig = px.histogram(df_sim, x="budget", color="buy", barmode="overlay",
                       title=f"Симуляция для {product_name}",
                       color_discrete_map={True: "#00CC96", False: "#EF553B"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💰 Экономика")
    st.metric("Прогноз продаж", f"{total_sales} ед.")
    st.metric("Чистая прибыль", f"{net_profit} TMT")
    
    # Кнопка скачивания Excel
    csv = df_sim.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Скачать сырые данные (CSV)", csv, "market_data.csv", "text/csv")

# Секция истории
st.divider()
st.subheader("📜 История ваших симуляций")
history_df = get_history()
if not history_df.empty:
    st.dataframe(history_df, use_container_width=True)
else:
    st.info("История пока пуста. Нажмите 'Сохранить', чтобы записать первый результат.")
