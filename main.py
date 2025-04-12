from flask import Flask, render_template, request, redirect
import sqlite3

main = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        email TEXT,
        phone TEXT,
        skills TEXT,
        experience TEXT,
        education TEXT
    )''')
    conn.commit()
    conn.close()

@main.route('/')
def indx():
    return render_template('indx.html')

@main.route('/resume', methods=['POST'])
def resume():
    data = (
        request.form['name'],
        request.form['age'],
        request.form['email'],
        request.form['phone'],
        request.form['skills'],
        request.form['experience'],
        request.form['education']
    )

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO resumes (name, age, email, phone, skills, experience, education) VALUES (?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

    return render_template('resume.html', name=data[0], age=data[1], email=data[2], phone=data[3],
                           skills=data[4], experience=data[5], education=data[6])

@main.route('/search')
def search():
    return render_template('search.html')

@main.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM resumes WHERE name = ?', (name,))
    row = c.fetchone()
    conn.close()

    if row:
        return render_template('result.html', row=row)
    else:
        return "<h3>لا توجد سيرة ذاتية بهذا الاسم.</h3><a href='/search'>رجوع</a>"

@main.route('/edit/<int:id>')
def edit(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM resumes WHERE id = ?', (id,))
    row = c.fetchone()
    conn.close()
    return render_template('edit.html', row=row)

@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    data = (
        request.form['name'],
        request.form['age'],
        request.form['email'],
        request.form['phone'],
        request.form['skills'],
        request.form['experience'],
        request.form['education'],
        id
    )
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE resumes SET name=?, age=?, email=?, phone=?, skills=?, experience=?, education=? WHERE id=?
    ''', data)
    conn.commit()
    conn.close()

    return redirect('/search')

if __name__ == '__main__':
    init_db()
    main.run(host='0.0.0.0', port=5000, debug=False)

