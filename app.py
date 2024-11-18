import streamlit as st
import requests
import json
from PIL import Image, ImageDraw, ImageFont

# Title for the app
st.title("Kidney Stone Detection App")

# Sidebar for input options
st.sidebar.title("Input Options")
input_option = st.sidebar.radio("Choose input type", ("Upload Image", "Use Camera"))

# Initialize variables
img_file_buffer = None
uploaded_image = None

# Use the camera
if input_option == "Use Camera":
    img_file_buffer = st.camera_input("Take a picture")

# Upload image
elif input_option == "Upload Image":
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Image handling
image_path = None
if img_file_buffer or uploaded_image:
    # Display the captured or uploaded image
    image = img_file_buffer if img_file_buffer else uploaded_image
    st.image(image, caption="Selected Image")

    # Save the image to a file
    image_path = "selected_image.jpg"
    with open(image_path, "wb") as file:
        file.write(image.getbuffer())
        st.success(f"Image saved as '{image_path}'")

# Inference and Overlay
if image_path and st.button("Run Prediction"):
    # URL and API setup
    url = "https://predict.ultralytics.com"
    headers = {"x-api-key": "ba9e29dcecf5b19a768e56a4f616df5d03baeef036"}
    data = {
        "model": "https://hub.ultralytics.com/models/DuZ63st9j4BtDfXb3CW3",
        "imgsz": 640,
        "conf": 0.1,
        "iou": 0.35,
    }

    try:
        # Send the image for inference
        with open(image_path, "rb") as f:
            response = requests.post(url, headers=headers, data=data, files={"file": f})
        response.raise_for_status()

        # Parse results
        results = response.json()
        # st.subheader("Prediction Results")
        # st.json(results)

        # Load the image
        original_image = Image.open(image_path)
        draw = ImageDraw.Draw(original_image)

        # Optional: Load a font for text (fallback if not found)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        # Overlay bounding boxes and labels
        for detection in results["images"][0]["results"]:
            box = detection["box"]
            x1, y1, x2, y2 = box["x1"], box["y1"], box["x2"], box["y2"]
            label = f'{detection["name"]} ({detection["confidence"]:.2f})'

            # Draw rectangle
            draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=3)
            # Draw label
            draw.text((x1, y1 - 10), label, fill="red", font=font)

        # Convert the image to RGB if it has an alpha channel
        if original_image.mode == "RGBA":
            original_image = original_image.convert("RGB")

        # Save and display the image with annotations
        annotated_image_path = "annotated_image.jpg"
        original_image.save(annotated_image_path)
        st.image(original_image, caption="Annotated Image with Predictions")

        # Optionally download the annotated image
        with open(annotated_image_path, "rb") as f:
            st.download_button(
                label="Download Annotated Image",
                data=f,
                file_name="annotated_image.jpg",
                mime="image/jpeg"
            )

    except Exception as e:
        st.error(f"Error during prediction: {e}")
