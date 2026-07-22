from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            enrollment_no TEXT UNIQUE NOT NULL,
            branch TEXT NOT NULL,
            cgpa REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route: View all students
@app.route('/')
def index():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    students = c.fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Route: Add a new student
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    enrollment_no = request.form['enrollment_no']
    branch = request.form['branch']
    cgpa = request.form['cgpa']
    
    try:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute('INSERT INTO students (name, enrollment_no, branch, cgpa) VALUES (?, ?, ?, ?)', 
                  (name, enrollment_no, branch, cgpa))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # In a production app, you would flash an error message here about duplicate enrollment IDs
    finally:
        conn.close()
        
    return redirect(url_for('index'))

# Route: Delete a student
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
