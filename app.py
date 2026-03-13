import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3
from datetime import datetime
from streamlit_folium import st_folium
import folium

# 1. Настройка страницы
st.set_page_config(page_title="AI Market & Logistics Pro", layout="wide")

# 2. Инициализация базы данных
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

def save_to_db(name, price, profit, sales):
    conn = sqlite3.connect('market_data.db')
    c = conn.cursor()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO simulations (timestamp, product_name, price, profit, sales) VALUES (?, ?, ?, ?, ?)",
              (ts, name, price, profit, sales))
    conn.commit()
    conn.close()

init_db()

# 3. Боковая панель (Sidebar)
with st.sidebar:
    st.header("⚙️ Настройки бизнеса")
    product_name = st.text_input("Название товара", "Premium Perfume")
    user_price = st.slider("Ваша цена (TMT)", 100, 2000, 550)
    comp_price = st.slider("Цена конкурента (TMT)", 100, 2000, 600)
    cost_usd = st.number_input("Закупка за ед. ($)", value=15.0)
    
    st.divider()
    if st.button("💾 Сохранить расчет"):
        # Значения подтянутся из session_state после первого запуска
        p = st.session_state.get('current_profit', 0)
        s = st.session_state.get('current_sales', 0)
        save_to_db(product_name, user_price, p, s)
        st.success("Данные сохранены в базу!")

# 4. Основной интерфейс
st.title("🌍 AI Market Intelligence & Logistics")

# Секция логистики
st.subheader("Маршруты поставок")
col_map, col_log = st.columns([2, 1])

with col_map:
    # Создание карты
    m = folium.Map(location=[32, 60], zoom_start=4, tiles="CartoDB positron")
    dubai = [25.2048, 55.2708]
    tashkent = [41.2995, 69.2401]
    ashgabat = [37.9601, 58.3262]
    
    folium.PolyLine([dubai, ashgabat], color="blue", weight=3, tooltip="Дубай -> Ашхабад").add_to(m)
    folium.PolyLine([tashkent, ashgabat], color="green", weight=3, tooltip="Ташкент -> Ашхабад").add_to(m)
    
    folium.Marker(dubai, popup="Дубай (ОАЭ)", icon=folium.Icon(color='blue')).add_to(m)
    folium.Marker(tashkent, popup="Ташкент (УЗБ)", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(ashgabat, popup="Ашхабад (ТМ)", icon=folium.Icon(color='red')).add_to(m)
    
    st_folium(m, width="100%", height=350)

with col_log:
    st.info("ℹ️ Расходы на логистику")
    delivery_type = st.radio("Тип доставки", ["Авиа (Быстро)", "Наземный (Дешево)"])
    ship_cost = 8.0 if "Авиа" in delivery_type else 3.5
    st.write(f"**Стоимость доставки:** ${ship_cost} за кг")

# 5. Симуляция рынка (10,000 агентов)
st.divider()
st.subheader("🎯 Результаты симуляции (10,000 ИИ-агентов)")

# Расчет экономики (Курс 1$ = 20 TMT)
total_cost_tmt = (cost_usd + ship_cost) * 20
np.random.seed(42)
agents = pd.DataFrame({'budget': np.random.normal(4500, 1800, 10000)})
agents['buy'] = (agents['budget'] > user_price) & (user_price < comp_price * 1.15)

sales = int(agents['buy'].sum())
profit = int(sales * (user_price - total_cost_tmt))

# Сохраняем для базы
st.session_state['current_profit'] = profit
st.session_state['current_sales'] = sales

m1, m2, m3 = st.columns(3)
m1.metric("Прогноз продаж", f"{sales} ед.")
m2.metric("Чистая прибыль", f"{profit} TMT")
m3.metric("Себестоимость", f"{int(total_cost_tmt)} TMT")

# График
fig = px.histogram(agents, x="budget", color="buy", 
                   title="Распределение покупателей по доходам",
                   color_discrete_map={True: "#00CC96", False: "#EF553B"})
st.plotly_chart(fig, use_container_width=True)

# 6. История из базы
st.divider()
st.subheader("📜 История расчетов")
conn = sqlite3.connect('market_data.db')
history = pd.read_sql_query("SELECT timestamp, product_name, price, profit, sales FROM simulations ORDER BY id DESC LIMIT 5", conn)
conn.close()

if not history.empty:
    st.table(history)
else:
    st.write("История пока пуста.")
    
