import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from PIL import Image, ImageDraw, ImageFont

# Load pre-trained model tokenizer (vocabulary)
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Load pre-trained model
model = GPT2LMHeadModel.from_pretrained('gpt2')

def generate_caption(product_name, discount, date):
    # Input text to guide the model's generation
    input_text = f"Generate a social media caption to promote {product_name}. The promotion offers a {discount}% discount and is valid until {date}. Make it engaging and include a call to action."
    inputs = tokenizer.encode(input_text, return_tensors='pt')
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def add_text_to_image(image, text):
    # Add text overlay to an image
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text_width, text_height = draw.textsize(text, font=font)
    position = ((image.width - text_width) / 2, image.height - 50)  # Place text at the bottom center
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

    # Call to generate marketing text
    caption = generate_caption(product_name, discount, promotion_duration)
    
    # Display generated caption
    st.write("Generated Caption:")
    st.write(caption)

    # Overlay the generated text onto the image
    image_with_text = add_text_to_image(image, caption)

    # Display the resulting image
    st.image(image_with_text, caption='Promotional Post Image')
