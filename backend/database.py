# backend/database.py
import sqlite3

DATABASE = 'data/database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            full_text TEXT,
            summary TEXT,
            template TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_user_data(email, full_text=None, summary=None, template=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email=?', (email,))
    if cursor.fetchone():
        cursor.execute('''
            UPDATE users SET full_text=?, summary=?, template=? WHERE email=?
        ''', (full_text, summary, template, email))
    else:
        cursor.execute('''
            INSERT INTO users (email, full_text, summary, template) VALUES (?, ?, ?, ?)
        ''', (email, full_text, summary, template))
    conn.commit()
    conn.close()

def get_user_data(email):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT full_text, summary, template FROM users WHERE email=?', (email,))
    data = cursor.fetchone()
    conn.close()
    if data:
        return {'full_text': data[0], 'summary': data[1], 'template': data[2]}
    else:
        return {}
