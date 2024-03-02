from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
from io import BytesIO

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/resize', methods=['POST'])
def resize():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Resize the image
        img = Image.open(file)
        img.thumbnail((300, 300))
        
        # Change the image format to JPEG
        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        # Save the resized image to the uploads folder
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'resized_image.jpg')
        img.save(filename)

        return render_template('result.html', filename=filename)

    return redirect(request.url)


if __name__ == '__main__':
    app.run(debug=True)
