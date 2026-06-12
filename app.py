import streamlit as st
import numpy as np
import pickle
from PIL import Image
import os

# Load Model
@st.cache_resource
def load_model():
    return pickle.load(open("D:/PYTHON_PROJECTS/rfc.pkl", "rb"))

rfc = load_model()

# UI Setup
st.title("🌲 Forest Cover Type Prediction")

try:
    header_img = Image.open("img.jpg")
    st.image(header_img, caption="Forest Cover", use_container_width=True)
except:
    st.warning("Header image not found")

# Input
user_input = st.text_input("Enter features (comma-separated values)")

# Mapping Dictionary

cover_image_dict = {
    1: {"name": "Spruce/Fir", "image": "D:/PYTHON_PROJECTS/img_1.jpg"},
    2: {"name": "Lodgepole Pine", "image": "D:/PYTHON_PROJECTS/img_2.jpg"},
    3: {"name": "Ponderosa Pine", "image": "D:/PYTHON_PROJECTS/img_3.jpg"},
    4: {"name": "Cottonwood/Willow", "image": "D:/PYTHON_PROJECTS/img_4.jpg"},
    5: {"name": "Aspen", "image": "D:/PYTHON_PROJECTS/img_5.jpg"},
    6: {"name": "Douglas-fir", "image": "D:/PYTHON_PROJECTS/img_6.jpg"},
    7: {"name": "Krummholz", "image": "D:/PYTHON_PROJECTS/img_7.jpg"}
}

# =======================
# Main Logic
# =======================
if user_input:
    try:
        # 1. Process Input
        values = [x.strip() for x in user_input.split(',') if x.strip()]
        features = np.array([list(map(float, values))], dtype=np.float64)

        # 2. Prediction
        prediction = int(rfc.predict(features)[0])
        st.success(f"Prediction: {prediction}")

        # 3. Mapping
        info = cover_image_dict.get(prediction)

        if info:
            forest_name = info["name"]
            forest_image = info["image"]

            col1, col2 = st.columns([1, 2])

            # Left: Name
            with col1:
                st.markdown(f"### 🌳 {forest_name}")

            # Right: Image
            with col2:
                if os.path.exists(forest_image):
                    img = Image.open(forest_image)
                    st.image(img, caption=forest_name, use_container_width=True)
                else:
                    st.error("Image file not found")

        else:
            st.warning("No mapping found for this prediction")

    except ValueError:
        st.error("⚠️ Enter only numeric values separated by commas")