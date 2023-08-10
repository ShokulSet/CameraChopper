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
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8);
        img = cv2.imdecode(file_bytes, 1);

        st.header("Original Image");
        st.image(img, channels="BGR");

        # Crop the image
        eye, cropped_eye = fn.Crop(img,'models/haarcascade_eye.xml');
        body, cropped_body = fn.Crop(img,'models/haarcascade_fullbody.xml');
        face, cropped_face = fn.Crop(img,'models/haarcascade_frontalface_default.xml');

        cropped_images = [i for i in [cropped_eye, cropped_body, cropped_face] if i]
        img_list = [eye, body, face]
        phrase_list = ["Eyes focused", "Body focused", "Face focused"]
        valid_list =[cropped_eye,cropped_body,cropped_face]
        # Display the cropped image
        st.header("Cropped Image")
        columns = []
        columns[0:len(cropped_images)+1] = st.columns(len(cropped_images)+1)
        for i in range(len(cropped_images)+1):
            with columns[i]:
                if valid_list[i]:
                    st.subheader(phrase_list[i])
                    st.image(img_list[i], channels="BGR")
    else:
        st.subheader("Please input your image")
        
# Run the app
if __name__ == "__main__":
    app()