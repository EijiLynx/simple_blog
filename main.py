from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         content TEXT NOT NULL,
         created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

with app.app_context():
    init_db()

def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    conn = get_db()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return render_template('post.html', post=post)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn = get_db()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                    (title, content))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    conn = get_db()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                    (title, content, post_id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('view_post', post_id=post_id))
    
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return render_template('edit.html', post=post)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    conn = get_db()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)