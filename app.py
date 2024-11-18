import streamlit as st

# Title for the app
st.title("Camera App with Streamlit")

# Access the camera
img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer:
    # Display the captured image
    st.image(img_file_buffer, caption="Captured Image")

    # Save the image to a file (optional)
    with open("captured_image.jpg", "wb") as file:
        file.write(img_file_buffer.getbuffer())
        st.success("Image saved as 'captured_image.jpg'")
