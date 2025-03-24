import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import openai
import requests
from io import BytesIO

# OpenAI API key configuration
openai.api_key = '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'

# Function to generate marketing captions using OpenAI GPT-3
def generate_caption(product_name, discount, date):
    prompt = f"Generate a social media caption to promote {product_name}. The promotion offers a {discount}% discount and is valid until {date}. Make it engaging and include a call to action."
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=60,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Function to overlay text on an image
def add_text_to_image(image, text):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()  # Using default font
    text_width, text_height = draw.textsize(text, font=font)
    position = ((image.width - text_width) / 2, image.height - 50)  # Position text at the bottom
    draw.text(position, text, font=font, fill='white')
    return image

# Streamlit UI setup
st.title('Liquor Bottle Promotion Post Generator')

# User Inputs
product_name = st.text_input("Product Name", "Special Vodka")
discount = st.number_input("Discount Percentage", min_value=0, max_value=100, value=25)
promotion_duration = st.text_input("Promotion Duration", "April 30")
upload_image = st.file_uploader("Upload a bottle image", type=["png", "jpg", "jpeg"])

if upload_image is not None:
    image = Image.open(upload_image)

    # Call to GPT-3 to generate marketing text
    caption = generate_caption(product_name, discount, promotion_duration)
    
    # Display generated caption
    st.write("Generated Caption:")
    st.write(caption)

    # Overlay the generated text onto the image
    image_with_text = add_text_to_image(image, caption)

    # Display the resulting image
    st.image(image_with_text, caption='Promotional Post Image')
