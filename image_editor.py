import io
import requests
from PIL import Image, ImageDraw, ImageFont
from pypinyin import pinyin, Style


def generate_pinyin_with_tones(chinese_text):
    # Convert Chinese text to Pinyin with tone marks
    pinyin_with_tone = pinyin(chinese_text, style=Style.TONE)

    # Join the Pinyin syllables into a single string
    pinyin_text = " ".join(p[0] for p in pinyin_with_tone)

    return pinyin_text

def create_title_card(chinese_text, background_image_path, output_image_path='title_card.jpg'):
    try:
        # Generate the Pinyin text
        pinyin_text = generate_pinyin_with_tones(chinese_text)

        # Load the background image
        img = Image.open(background_image_path)

        # Create ImageDraw object
        draw = ImageDraw.Draw(img)

        # Choose some font, change the path to font file and font size according to your needs
        chinese_font = ImageFont.truetype('txt/fonts/chinese.ttf', 120)  # Assuming you have the font file
        pinyin_font = ImageFont.truetype('txt/fonts/chinese.ttf', 90)  # Default Arial font

        # Get the image dimensions
        width, height = img.size

        # Draw the text on the image
        draw.text((width / 2, height / 2), chinese_text, font=chinese_font, fill='white', anchor='mm')
        draw.text((width / 2, (height / 2) - 120), pinyin_text, font=pinyin_font, fill='white', anchor='mm')

        # Save the image
        img.save(output_image_path)

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def crop_image(image_path, left, top, right, bottom, output_path):
    # Open the image file
    img = Image.open(image_path)

    # Crop the image using the coordinates
    img_cropped = img.crop((left, top, right, bottom))

    # Save the cropped image
    img_cropped.save(output_path)

def make_prop(prop, output, background_image_path):
    API_TOKEN = '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'
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    image_bytes = query({
        "inputs": f"Picture of a {prop}",
    })

    prop_i = Image.open(io.BytesIO(image_bytes))
    prop_i = prop_i.convert('RGBA')
    background = Image.open(background_image_path)
    x = (background.width - prop_i.width) // 2
    y = (background.height - prop_i.height) // 2
    background.paste(prop_i, (x, y), prop_i)
    background.save(output)
