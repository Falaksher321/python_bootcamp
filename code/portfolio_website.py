import streamlit as st
import google.generativeai as genai
from streamlit_lottie import st_lottie
import requests
import time
import os
import base64

# Configure page layout and theme (this must be the first Streamlit command)
st.set_page_config(page_title="Falak Sher - Portfolio", layout="wide", initial_sidebar_state="expanded")

# Function to encode the image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set background image
def set_bg_hack(main_bg):
    bin_str = get_base64_of_bin_file(main_bg)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set the background image
try:
    set_bg_hack('images/background.jpg')
except FileNotFoundError:
    st.warning("Background image not found. Please check if 'images/background.jpg' exists.")

# Custom CSS for animations and styling
st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
@keyframes wave {
    0% { transform: rotate(0deg); }
    10% { transform: rotate(14deg); }
    20% { transform: rotate(-8deg); }
    30% { transform: rotate(14deg); }
    40% { transform: rotate(-4deg); }
    50% { transform: rotate(10deg); }
    60% { transform: rotate(0deg); }
    100% { transform: rotate(0deg); }
}
@keyframes glow {
    0% { box-shadow: 0 0 5px #4CAF50, 0 0 5px #4CAF50 inset; }
    50% { box-shadow: 0 0 20px #4CAF50, 0 0 20px #4CAF50 inset; }
    100% { box-shadow: 0 0 5px #4CAF50, 0 0 5px #4CAF50 inset; }
}
@keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.fadeIn { animation: fadeIn 1.5s ease-in; }
.wave { animation: wave 2s infinite; transform-origin: 70% 70%; display: inline-block; }
.stButton>button {
    background-color: #4CAF50;
    color: white;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #45a049;
    transform: scale(1.05);
}
.profile-pic-container {
    width: 250px;
    height: 250px;
    margin: auto;
    position: relative;
    overflow: hidden;
}
.profile-pic {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
    transition: transform 0.3s ease-in-out;
    animation: glow 2s infinite;
}
.profile-pic:hover {
    transform: scale(1.1);
}
.profile-pic-border {
    position: absolute;
    top: -5px;
    left: -5px;
    right: -5px;
    bottom: -5px;
    border: 3px solid #4CAF50;
    border-radius: 50%;
    animation: rotate 10s linear infinite;
}
body {
    color: #ffffff;
}
h1, h2, h3, h4, h5, h6 {
    color: #ffffff;
}
.stApp > header {
    background-color: transparent;
}
.stApp {
    background-color: rgba(0,0,0,0.7);
}
.stTextInput > div > div > input {
    color: white;
}
.stMarkdown {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Load Lottie animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    lottie_json = r.json()
    # Set the background to be transparent
    if 'assets' in lottie_json:
        for asset in lottie_json['assets']:
            if 'p' in asset:  # 'p' stands for path, which often defines the background
                asset['p'] = ''  # Set to empty string to make it transparent
    return lottie_json

# Load Lottie animations
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
lottie_github = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_vnikrcia.json")

# Gemini AI setup
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Header section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="fadeIn">', unsafe_allow_html=True)
    st.markdown("<h3>Hi <span class='wave'>👋</span></h3>", unsafe_allow_html=True)
    st.title("I am Falak Sher.")
    st.markdown('</p>', unsafe_allow_html=True)

with col2:
    try:
        with open("images/murtaza.png", "rb") as f:
            contents = f.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            st.markdown(f"""
            <div class="profile-pic-container">
                <img src="data:image/png;base64,{data_url}" class="profile-pic">
                <div class="profile-pic-border"></div>
            </div>
            """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Profile picture not found. Please check if 'images/murtaza.png' exists.")

# About Me section
st.markdown('<h2 class="fadeIn">About Me</h2>', unsafe_allow_html=True)
st.write("I'm a student passionate about Computer Vision and Robotics, exploring the fascinating world of AI and its applications.")

# AI Bot section
st.markdown('<h2 class="fadeIn">Falak AI Bot</h2>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    user_question = st.text_input("Ask anything about me")
    if st.button("ASK", use_container_width=True):
        with st.spinner("Thinking..."):
            persona = """
            You are Falak AI bot. You help people answer questions about yourself (i.e Falak Sher).
            Answer as if you are responding. Don't answer in second or third person.
            If you don't know the answer, you simply say "That's a secret".
            Here is more info about Falak Sher: 
            
            Falak Sher is a student in the field of Computer Vision and Robotics.
            He is also a lecturer and a design engineer, evaluating and developing rapid prototypes of US patents.
            """
            prompt = persona + "Here is the question that the user asked: " + user_question
            response = model.generate_content(prompt)
            st.write(response.text)

with col2:
    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0); padding: 10px; border-radius: 10px;">
    """, unsafe_allow_html=True)
    if lottie_coding:
        st_lottie(lottie_coding, height=200, key="coding")
    else:
        st.warning("Lottie animation failed to load.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# GitHub Section
st.markdown('<h2 class="fadeIn">GitHub</h2>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0); padding: 10px; border-radius: 10px;">
    """, unsafe_allow_html=True)
    if lottie_github:
        st_lottie(lottie_github, height=200, key="github")
    else:
        st.warning("GitHub Lottie animation failed to load.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<p class="fadeIn">Check out my projects on <a href="https://github.com/Falaksher321/python_bootcamp" target="_blank">GitHub</a>!</p>', unsafe_allow_html=True)

st.markdown("---")

# Setup section
st.markdown('<h2 class="fadeIn">My Setup</h2>', unsafe_allow_html=True)
try:
    st.image("images/setup.jpg", use_column_width=True)
except FileNotFoundError:
    st.warning("Setup image not found. Please check if 'images/setup.jpg' exists.")

# Skills section
st.markdown('<h2 class="fadeIn">My Skills</h2>', unsafe_allow_html=True)
skills = {
    "Programming": 50,
    "Robotics": 30
}

for skill, value in skills.items():
    st.markdown(f"<p class='fadeIn'>{skill}</p>", unsafe_allow_html=True)
    progress_bar = st.progress(0)
    for i in range(value + 1):
        time.sleep(0.01)
        progress_bar.progress(i)

st.markdown("---")

# Gallery section
st.markdown('<h2 class="fadeIn">Gallery</h2>', unsafe_allow_html=True)
gallery_images = [f"images/g{i}.jpg" for i in range(1, 3)]

cols = st.columns(3)
for i, image in enumerate(gallery_images):
    with cols[i % 3]:
        try:
            st.image(image, use_column_width=True)
        except FileNotFoundError:
            st.warning(f"Image not found: {image}")

# Contact section
st.markdown("---")
st.markdown('<h2 class="fadeIn">Contact</h2>', unsafe_allow_html=True)
st.markdown('<p class="fadeIn">For any inquiries, email at:</p>', unsafe_allow_html=True)
st.markdown('<h3 class="fadeIn">mfalaksher901@gmail.com</h3>', unsafe_allow_html=True)

# Friendly Ending Section
st.markdown("---")
st.markdown('<h2 class="fadeIn">Thank You for Visiting!</h2>', unsafe_allow_html=True)
st.markdown('<p class="fadeIn">Feel free to connect with me on <a href="https://www.linkedin.com/in/your-linkedin-username" target="_blank">LinkedIn</a> or follow me on <a href="https://twitter.com/your-twitter-username" target="_blank">Twitter</a>.</p>', unsafe_allow_html=True)
st.markdown('<p class="fadeIn">Stay tuned for more updates and projects!</p>', unsafe_allow_html=True)
