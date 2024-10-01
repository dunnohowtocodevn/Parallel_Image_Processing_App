import sqlite3
from PIL import Image
from io import BytesIO

DATABASE = 'db.sqlite3'

def handle_image_processing(image_id, action, value):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT original_image, original_filename FROM images WHERE id = ?', (image_id,))
        original_image_data, original_filename = cursor.fetchone()

    image_buffer = BytesIO(original_image_data)
    img = Image.open(image_buffer)

    if action == 'rotate':
        img = img.rotate(int(value))
    elif action == 'resize':
        width, height = map(int, value.split('x'))
        img = img.resize((width, height))
    elif action == 'grayscale':
        img = img.convert('L')
    elif action == 'flip':
        if value == 'horizontal':
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif value == 'vertical':
            img = img.transpose(Image.FLIP_TOP_BOTTOM)

    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    processed_image_data = output_buffer.getvalue()
    processed_filename = f"processed_{original_filename}"

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE images SET processed_image = ?, processed_filename = ? WHERE id = ?
        ''', (processed_image_data, processed_filename, image_id))

    return processed_filename