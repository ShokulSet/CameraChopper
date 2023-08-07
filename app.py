import streamlit as st
import numpy as np
import cv2
import fn


def app():
    st.title("Camera Chopper")
    # Display a file uploader widget
    image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

    # Check if this file is an image
    if image_file:
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)

        st.subheader("Original Image")
        st.image(opencv_image, channels="BGR")

        # Crop the image
        eye, cropped_eye = fn.Crop(opencv_image,'models/haarcascade_eye.xml')
        body, cropped_body = fn.Crop(opencv_image,'models/haarcascade_fullbody.xml')
        face, cropped_face = fn.Crop(opencv_image,'models/haarcascade_frontalface_default.xml')

        # Display the cropped image
        st.subheader("Cropped Image")
        ceye, cbody, cface = st.columns(3)
        with ceye:
            if cropped_eye:
                st.subheader("Eye focused")
                st.image(eye,channels="BGR")
            else:
                st.subheader("No eyes found")
        with cbody:
            if cropped_body:
                st.subheader("Body focused")
                st.image(body,channels="BGR")
            else:
                st.subheader("No body found")
        with cface:
            if cropped_face:
                st.subheader("Face focused")
                st.image(face,channels="BGR")
            else:
                st.subheader("No face found")

# Run the app
if __name__ == "__main__":
    app()

