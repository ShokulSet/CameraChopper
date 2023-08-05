import streamlit as st
import numpy as np
import cv2
import fn



def app():
    st.title("Camera Chopper")
    # Display a file uploader widget
    image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

    # Check if this file is an image
    if image_file is not None:
        # Convert the file to an opencv image.
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)

        # Now do something with the image! For example, let's display it:
        st.subheader("Original Image")
        st.image(opencv_image, channels="BGR")

        # Crop the image
        cropped_image = fn.Crop(opencv_image,'models/haarcascade_eye.xml')

        # Display the cropped image
        st.subheader("Cropped Image")
        st.image(cropped_image, channels="BGR")

# Run the app
if __name__ == "__main__":
    app()