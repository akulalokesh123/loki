from flask import Flask, request, render_template, send_file, send_from_directory
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('indeximg.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    if file:
        img = Image.open(file.stream)
        action = request.form.get('action')

        # Convert image to black and white
        if action == 'black_white':
            img = img.convert('L')
        
        # Add a watermark
        elif action == 'watermark':
            size = (100, 100)
            imgwatermark = img.copy()
            imgwatermark.thumbnail(size)
            imgwatermarkfinal = img.copy()
            imgwatermarkfinal.paste(imgwatermark, (0, 0), imgwatermark)
            img = imgwatermarkfinal
        
        
        # Add text watermark
        elif action == 'text_watermark':
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 250)
            except IOError:
                font = ImageFont.load_default()
            draw.text((0, 0), "lokesh", (0, 0, 0), font=font)
        
        # Resize image
        elif action == 'resize':
            img = img.resize((300, 300))
        
                # Resize image
        elif action == 'resize1':
            img = img.resize((800, 600))
        # Crop image
        elif action == 'crop':
            img = img.crop((100, 100, 400, 400))
        
        # Enhance color
        elif action == 'enhance_color':
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(2.0)
        
        # Sharpen image
        elif action == 'sharpen':
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)
        
        # Rotate image
        elif action == 'rotate':
            img = img.rotate(90)
        
        # Blur image
        elif action == 'blur':
            img = img.filter(ImageFilter.BLUR)
        
        # Additional functionalities
        elif action == 'thumbnail':
            size = (100, 100)
            img.thumbnail(size)
        
        elif action == 'flip':
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        
        elif action == 'transpose':
            img = img.transpose(Image.Transpose.ROTATE_90)
        
        elif action == 'flip_top_bottom':
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        
        elif action == 'rotate_45':
            img = img.rotate(45)
        
        elif action == 'rotate_expand':
            img = img.rotate(45, expand=True)
        
        elif action == 'crop_large':
            img = img.crop((100, 100, 1200, 2000))
        
        elif action == 'resize_low_res':
            img = img.resize((img.width // 3, img.height // 3))

        # Contrast
        elif action == 'contrast':
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
        
        # Brightness
        elif action == 'brightness':
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(2.0)
        
        # Sharpness
        elif action == 'sharpness':
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)
        
        # Color
        elif action == 'color':
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(2.0)
        elif action == 'passport_size':
            # Crop to passport size (600 x 600 pixels)
            passport_size = (600, 600)
            img = img.resize((passport_size[0] * 2, passport_size[1] * 2))
            left = (img.width - passport_size[0]) / 2
            top = (img.height - passport_size[1]) / 2
            right = (img.width + passport_size[0]) / 2
            bottom = (img.height + passport_size[1]) / 2
            img = img.crop((left, top, right, bottom))

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        return send_file(img_byte_arr, mimetype='image/jpeg')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
