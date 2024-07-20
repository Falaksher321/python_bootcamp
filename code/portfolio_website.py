import streamlit as st
import google.generativeai as genai
from streamlit_lottie import st_lottie
import requests
import time
import os

# Configure page layout and theme
st.set_page_config(page_title="Falak Sher - Portfolio", layout="wide", initial_sidebar_state="expanded")

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
    0% { box-shadow: 0 0 5px #4CAF50; }
    50% { box-shadow: 0 0 20px #4CAF50; }
    100% { box-shadow: 0 0 5px #4CAF50; }
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
.stImage > img {
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    transition: transform 0.3s ease-in-out;
    animation: glow 2s infinite;
}
.stImage > img:hover {
    transform: scale(1.1);
}
body {
    background-color: #121212;
    color: #ffffff;
}
h1, h2, h3, h4, h5, h6 {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# Load Lottie animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

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
    st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 100%;">', unsafe_allow_html=True)
    st.image("images/murtaza.png", width=250, output_format="PNG", use_column_width=False)
    st.markdown('</div>', unsafe_allow_html=True)

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
    st_lottie(lottie_coding, height=200, key="coding")

st.markdown("---")

# GitHub Section
st.markdown('<h2 class="fadeIn">GitHub</h2>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])

with col1:
    st_lottie(lottie_github, height=200, key="github")

with col2:
    st.markdown('<p class="fadeIn">Check out my projects on <a href="https://github.com/Falaksher321/python_bootcamp" target="_blank">GitHub</a>!</p>', unsafe_allow_html=True)

st.markdown("---")

# Setup section
st.markdown('<h2 class="fadeIn">My Setup</h2>', unsafe_allow_html=True)
st.image("images/setup.jpg", use_column_width=True)

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
        st.image(image, use_column_width=True)

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

# Debug information
st.markdown("---")
st.markdown('<h2 class="fadeIn">Debug Information</h2>', unsafe_allow_html=True)
st.write("Current working directory:", os.getcwd())
image_path = "images/murtaza.png"
if os.path.exists(image_path):
    st.write(f"Image file found: {image_path}")
else:
    st.write(f"Image file not found: {image_path}")
