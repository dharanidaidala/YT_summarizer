import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import openai

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

# Header
st.title("Liquor Bottle Promotion Post Generator")

# Sidebar Inputs
st.sidebar.header("Promotion Details")
product_name = st.sidebar.text_input("Product Name", "Premium Whiskey")
discount = st.sidebar.number_input("Discount (%)", min_value=0, max_value=100, value=20)
price = st.sidebar.text_input("Price", "$50")
promotion_duration = st.sidebar.text_input("Promotion Duration", "Limited Time Offer")
cta_text = st.sidebar.text_input("Call-to-Action", "Shop Now!")

# Style Options
st.sidebar.header("Text Styling")
text_color = st.sidebar.color_picker("Text Color", "#FFFFFF")
font_size = st.sidebar.slider("Font Size", 20, 80, 40)
background_box = st.sidebar.checkbox("Add Background Box for Text", value=True)

# Image Upload
uploaded_image = st.sidebar.file_uploader("Upload Product Image", type=["png", "jpg", "jpeg"])

# Generate Caption using OpenAI GPT
if st.sidebar.button("Generate Caption"):
    prompt = f"Create a catchy promotional caption for {product_name} with a {discount}% discount, priced at {price}, available for {promotion_duration}. Add a call-to-action like {cta_text}."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    generated_caption = response["choices"][0]["text"].strip()
    st.sidebar.success(f"Generated Caption: {generated_caption}")
else:
    generated_caption = f"{product_name} - {discount}% OFF! Now at {price}. {cta_text}"

# Generate Post
if uploaded_image:
    image = Image.open(uploaded_image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", font_size)

    # Text Position and Background Box
    text = f"{product_name}\n{discount}% OFF\nNow at {price}\n{promotion_duration}\n{cta_text}"
    text_width, text_height = draw.multiline_textsize(text, font=font)
    position = (10, 10)  # Top-left corner
    if background_box:
        draw.rectangle(
            [position, (position[0] + text_width + 20, position[1] + text_height + 20)],
            fill="black"
        )
    draw.multiline_text(position, text, fill=text_color, font=font)

    # Display Image
    st.image(image, caption="Generated Post", use_column_width=True)

    # Download Button
    image.save("promotion_post_styled.png")
    with open("promotion_post_styled.png", "rb") as file:
        st.download_button("Download Post", file, "promotion_post_styled.png", "image/png")
else:
    st.warning("Please upload a product image.")
