from PIL import Image
from collections import Counter
from flask import Flask, render_template, redirect, request, flash, url_for
from flask_bootstrap import Bootstrap5
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
Bootstrap5(app)


def apply_delta(color, delta):
    return tuple((value // delta) * delta for value in color)


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def extract_colors(image_path, num_colors, delta):
    image = Image.open(image_path)
    image = image.convert('RGB')
    image = image.resize((150, 150))
    pixels = list(image.getdata())
    adjusted_pixels = [apply_delta(pixel, delta) for pixel in pixels]
    color_counts = Counter(adjusted_pixels)
    most_common_colors = color_counts.most_common(num_colors)
    hex_colors = [(rgb_to_hex(color), count) for color, count in most_common_colors]
    return hex_colors


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['image']
        if file and file.filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            file.save(file_path)
            num_colors = int(request.form["num_colors"])
            delta = int(request.form["delta"])
            colors = extract_colors(file_path, num_colors, delta)
            return render_template('index.html', colors=colors, picture=file_path)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)