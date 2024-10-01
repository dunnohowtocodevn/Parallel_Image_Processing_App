from flask import Flask, render_template, request, redirect, url_for, Response
import os
from rq import Queue
from rq.job import Job
import sqlite3
from worker import conn
from tasks import handle_image_processing
from io import BytesIO
# Initialize Flask app
app = Flask(__name__)

# Initialize Redis Queue
q = Queue(connection=conn)

# SQLite Database
DATABASE = 'db.sqlite3'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_image BLOB,
        processed_image BLOB,
        original_filename TEXT,
        processed_filename TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    
    image = request.files['image']
    if image.filename == '':
        return redirect(url_for('index'))
    
    if image:
        image_data = image.read()
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO images (original_image, original_filename) VALUES (?, ?)
            ''', (image_data, image.filename))
            image_id = cursor.lastrowid
        return render_template('process.html', image_id=image_id, image_name=image.filename)

@app.route('/process/<int:image_id>', methods=['POST'])
def process_image(image_id):
    action = request.form['action']
    value = request.form.get('value')

    # Enqueue the task to the Redis queue
    job = q.enqueue(handle_image_processing, image_id, action, value)

    # Wait for the job to complete (this is not ideal for production, consider using websockets or polling)
    job.refresh()
    while not job.is_finished:
        job.refresh()

    return redirect(url_for('view_image', image_id=image_id))

@app.route('/view/<int:image_id>')
def view_image(image_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT original_filename, processed_filename FROM images WHERE id = ?', (image_id,))
        result = cursor.fetchone()
        if result:
            original_filename, processed_filename = result
        else:
            return 'Image not found', 404

    return render_template('view.html', image_id=image_id, 
                           original_filename=original_filename, 
                           processed_filename=processed_filename)

@app.route('/image/<int:image_id>/<image_type>')
def get_image(image_id, image_type):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        if image_type == 'original':
            cursor.execute('SELECT original_image FROM images WHERE id = ?', (image_id,))
        else:
            cursor.execute('SELECT processed_image FROM images WHERE id = ?', (image_id,))
        image_data = cursor.fetchone()

    if image_data and image_data[0]:
        return Response(image_data[0], mimetype='image/jpeg')
    else:
        return 'Image not found', 404

if __name__ == '__main__':
    app.run(debug=True)