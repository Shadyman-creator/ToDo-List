import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            done BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date TIMESTAMP,
            repeat TEXT,  -- 'daily', 'weekly', 'monthly'
            repeat_interval INTEGER -- интервал повторения
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']
    repeat = request.form.get('repeat')
    repeat_interval = request.form.get('repeat_interval')

    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, due_date, repeat, repeat_interval)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, description, due_date, repeat, repeat_interval))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['GET'])
def complete(task_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET done = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/uncomplete/<int:task_id>')
def uncomplete(task_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET done = 0 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/update/<int:id>')
def update(id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET done = NOT done WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
