import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import tempfile
import time  
from sklearn.preprocessing import LabelEncoder



# Load the pre-trained model and label encoder
model = tf.keras.models.load_model('model.h5')
label_encoder = LabelEncoder()
label_encoder.classes_ = np.load('label_encoder_classes.npy') 

# Function to classify the image
def classify_image(img):
    img = img.resize((128, 128))
    img = img.convert('RGB')
    img = np.array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    st.markdown(
        """
        <style>
        .class2 {
            margin-top: 40px;
            margin-bottom: 10px;
        }
        </style>
        <div class="class2">
        Converted Image :
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.image(img, caption="Binary Representation of the File", use_column_width=True)

    
    prediction = model.predict(img)
    class_idx = np.argmax(prediction)
    class_name = label_encoder.inverse_transform([class_idx])[0]
    return class_name

def convert_to_pixel_art(binary_data):
    # Define the color palette (grayscale with 256 shades)
    color_palette = [(i, i, i) for i in range(256)]

    # Calculate the image dimensions based on the file size
    image_size = len(binary_data)
    image_width = int(image_size ** 0.5)
    image_height = (image_size + image_width - 1) // image_width

    # Create a new image with the specified dimensions
    image = Image.new('RGB', (image_width, image_height))

    # Iterate over the binary data and assign pixel values
    for i, byte in enumerate(binary_data):
        # Ensure the pixel value is within the range of the color palette
        pixel_value = min(max(byte, 0), len(color_palette) - 1)

        # Calculate the pixel coordinates
        x = i % image_width
        y = i // image_width

        # Set the pixel color
        image.putpixel((x, y), color_palette[pixel_value])

    return image

# Streamlit app
def main():

    st.markdown(
        """
        <style>
        .title {
            font-size: 75px;
            font-weight: bold;
            color: #ff6600; /* Orange color */
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        <div class="title">
            RansomAI Detectron
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .main-header {
            font-size:28px;
            font-weight: bold;
            # color: #ffffff;
            text-align: center;
            margin-bottom: 50px;
        }
        </style>
        <div class="main-header">
            Unleash the Power of AI: Detecting Ransomware
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <style>
        .class4 {
            # font-size:28px;
            # font-weight: bold;
            # color: #ffffff;
            text-align: center;
            margin-bottom: 50px;
        }
        </style>
        <div class="class4">
            Welcome to RansomAI Detectron, your all-in-one security solution. Upload any file, and instantly discover its safety status or let our advanced technology classify it into the latest 28 ransomware classes. We utilize cutting-edge deep learning, powered by a specially trained model with over 95% accuracy.
        </div>
        """,
        unsafe_allow_html=True
    )

    class_name = ""

    option = st.selectbox("Select Analysis Type :", ["🖼️ Analyze Binary Image Directly", "📁 Analyze File"])

    st.markdown(
        """
        <style>
        .class1 {
            margin-bottom: 40px;
        }
        </style>
        <div class="class1">
            
        </div>
        """,
        unsafe_allow_html=True
    )

    if option == "🖼️ Analyze Binary Image Directly":
        uploaded_image = st.file_uploader("🔍 Upload Binary Image to Analyze :", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            with st.spinner('Analyzing the image...⏳'):
                img = Image.open(uploaded_image)    
                class_name = classify_image(img)
            

    elif option == "📁 Analyze File":
        # st.image('file_conversion_animation.gif', use_column_width=True) 
        uploaded_file = st.file_uploader("🕵️ Upload File to Analyze :")

        if uploaded_file is not None:
            # st.write("Uploaded File:", uploaded_file.name)

            # Create an empty element to display the "Please wait" message
            wait_message = st.empty()
            with st.spinner("🔓 Decrypting Data... Hold tight for a secure reveal."):
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_file_path = temp_file.name

                with open(temp_file_path, 'rb') as file:
                    binary_data = file.read()
                    binary_image = convert_to_pixel_art(binary_data)

                    # Resize the image to (128 x 128)
                    resized_image = binary_image.resize((128, 128))

                    # Introduce a delay to ensure the message is cleared after conversion
                    time.sleep(1)  # Adjust the delay as needed

                    # Clear the spinner
                    st.spinner(False)

                    # Clear the "Please wait" message
                    wait_message.empty()
                    with st.spinner('Analyzing the image...⏳'):
                        class_name = classify_image(resized_image)


    if class_name is not "":

        st.markdown(
            """
            <div class="prediction">
            """,
            unsafe_allow_html=True
        )

        if "benign" in class_name.lower():
            st.success(f"✅ No worries, the uploaded file is SAFE 🛡️ ")
            st.success(f"🧩 Predicted class : {class_name}")
        else:
            st.error(f"⚠️ The uploaded file is INFECTED☠️, avoid opening it to protect your device.")
            st.error(f"🛑 Predicted class : {class_name}")
            # st.image('unsafe_image_icon.png', use_column_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
