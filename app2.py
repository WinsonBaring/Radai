
import cv2
import av
import numpy as np
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Title for the app
st.title("Real-Time Camera App with AI Detection")

# Define a VideoTransformer class for real-time processing
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # (Optional) Add AI inference logic here
        # For example: Dummy bounding box
        height, width, _ = img.shape
        cv2.rectangle(img, (100, 100), (200, 200), (0, 0, 255), 2)  # Example box
        cv2.putText(img, "Object", (100, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return img

# Start real-time video streamer
webrtc_streamer(
    key="example",
    video_transformer_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},
)
