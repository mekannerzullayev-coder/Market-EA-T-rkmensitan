from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect('agri_app.db')

@app.route('/')
def index():
    search = request.args.get('search', '')
    conn = get_db()
    cursor = conn.cursor()
    try:
        if search:
            cursor.execute("SELECT id, name, area, coordinates, owner_name, owner_phone, status, price, description FROM lands WHERE name LIKE ? OR owner_name LIKE ?", ('%'+search+'%', '%'+search+'%'))
        else:
            cursor.execute("SELECT id, name, area, coordinates, owner_name, owner_phone, status, price, description FROM lands")
        lands = cursor.fetchall()
    except:
        return "Ошибка базы! Проверьте Шаг 1."
    conn.close()
    
    return render_template_string('''
        <style>
            body{font-family:sans-serif; background:#f0f2f5; padding:10px;}
            .card{background:white; padding:15px; margin-bottom:10px; border-radius:10px; border-left:5px solid #4CAF50; box-shadow:0 2px 4px rgba(0,0,0,0.1);}
            .desc{color:#555; font-size:0.9em; font-style:italic; margin:10px 0; background:#f9f9f9; padding:5px; border-radius:4px;}
            .btn{display:block; text-align:center; padding:15px; background:#4CAF50; color:white; text-decoration:none; border-radius:8px; font-weight:bold;}
            input, textarea {width:100%; padding:10px; margin:5px 0; border:1px solid #ccc; border-radius:5px;}
        </style>
        <h2>Agro App 🚜</h2>
        <form method="get"><input type="text" name="search" placeholder="Поиск..."><button type="submit" style="width:100%; background:#ddd; border:none; padding:10px;">Найти</button></form><br>
        {% for land in lands %}
        <div class="card">
            <div style="float:right; color:{{ 'green' if land[6]=='Свободно' else 'red' }}">{{ land[6] }}</div>
            <h3>{{ land[1] }}</h3>
            <p>👤 {{ land[4] }} | 📞 {{ land[5] }}<br>📏 {{ land[2] }} га | 💰 {{ land[7] }} TMT</p>
            <div class="desc">📝 <b>Описание:</b> {{ land[8] or "Нет описания" }}</div>
            <a href="https://www.google.com/maps?q={{ land[3] }}" target="_blank" style="color:blue;">📍 Карта</a> | 
            <a href="/edit/{{ land[0] }}" style="color:orange;">✏️ Изменить</a>
            <a href="/delete/{{ land[0] }}" style="color:red; float:right;">🗑 Удалить</a>
        </div>
        {% endfor %}
        <br><a href="/add" class="btn">+ ДОБАВИТЬ ЗЕМЛЮ</a>
    ''', lands=lands)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        conn = get_db()
        conn.execute("INSERT INTO lands (name, area, coordinates, owner_name, owner_phone, delete_code, price, status, description) VALUES (?,?,?,?,?,?,?,?,?)",
                     (request.form['name'], request.form['area'], request.form['coords'], request.form['owner'], request.form['phone'], request.form['del_code'], request.form['price'], 'Свободно', request.form['desc']))
        conn.commit()
        conn.close()
        return redirect('/')
    return '''
        <form method="post" style="padding:20px; font-family:sans-serif;">
            <h3>Новая запись</h3>
            <input name="name" placeholder="Название поля" required>
            <input name="owner" placeholder="Имя хозяина">
            <input name="phone" placeholder="Телефон">
            <input name="area" placeholder="Площадь (га)">
            <input name="price" placeholder="Цена (TMT)">
            <input name="coords" placeholder="Координаты (37.95, 58.38)">
            <textarea name="desc" placeholder="Описание земли (почва, вода, дорога...)"></textarea>
            <input name="del_code" placeholder="Секретный код (для удаления)" required style="border:2px solid orange;">
            <button type="submit" style="width:100%; padding:15px; background:green; color:white; border:none; border-radius:8px;">Сохранить</button>
        </form>
    '''

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, status, delete_code, description FROM lands WHERE id=?", (id,))
    land = cursor.fetchone()
    if request.method == 'POST':
        if request.form['code'] == land[3]:
            conn.execute("UPDATE lands SET price=?, status=?, description=? WHERE id=?", (request.form['price'], request.form['status'], request.form['desc'], id))
            conn.commit()
            return redirect('/')
        return "Неверный код!"
    return f'''
        <form method="post" style="padding:20px; font-family:sans-serif;">
            <h3>Изменить: {land[0]}</h3>
            Цена: <input name="price" value="{land[1]}">
            Описание: <textarea name="desc">{land[4]}</textarea>
            Статус: <select name="status" style="width:100%; padding:10px;"><option value="Свободно">Свободно</option><option value="Продано">Продано</option></select><br><br>
            Код автора: <input name="code" type="password" required style="border:2px solid orange;">
            <button type="submit" style="width:100%; padding:15px; background:orange; color:white; border:none; border-radius:8px;">Обновить</button>
        </form>
    '''

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT delete_code FROM lands WHERE id=?", (id,))
        if cursor.fetchone()[0] == request.form['code']:
            cursor.execute("DELETE FROM lands WHERE id=?", (id,))
            conn.commit()
            return redirect('/')
        return "Неверный код!"
    return '<form method="post" style="padding:20px;"><h3>Код для удаления:</h3><input name="code" type="password"><br><br><button type="submit">Удалить</button></form>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

