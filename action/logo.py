import streamlit as st
from PIL import Image

img = Image.open("logos/csk.png")
st.image(img)