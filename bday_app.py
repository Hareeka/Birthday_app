import streamlit as st
from streamlit_lottie import st_lottie
import json
import os
import base64
import streamlit.components.v1 as components


# --- Import the new components for microphone and audio analysis ---
from streamlit_mic_recorder import mic_recorder
import numpy as np
import scipy.io.wavfile as wavfile

st.markdown(
    """
    <style>
    /* Keep your base background */
    .stApp {
        background-color: #ffe4e1;
        color: #6B4C3B;
    }

    /* Set lighter default text color for visibility */
    body, h1, h2, h3, h4, h5, h6, p {
        color: #6B4C3B;
    }

    /* Fix buttons */
    .stButton>button {
        background-color: #fff0f5 !important;  /* very soft pink */
        color: #6B4C3B !important;             /* warm brown */
        border: 2px solid #E5989B !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #f7c6cc !important;
        color: #4a342e !important;
    }

    /* Cards or letter containers */
    .envelope .letter {
        color: #6B4C3B;
        background-color: #fff; /* white background for readability */
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        max-height: 400px;
        overflow-y: auto;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# --- SET PAGE CONFIG ---
st.set_page_config(page_title="Happy Birthday Sherly 🎂", layout="wide")

st.markdown(
    """
    <style>
    /* Center everything inside the main container */
    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }

    /* Also center components inside columns */
    [data-testid="stHorizontalBlock"] {
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- INITIAL SESSION STATE ---
# Check if the volume check has been done
if "volume_checked" not in st.session_state:
    st.session_state.volume_checked = False
    st.session_state.volume_high = None

# Check if the main app has started
if "start_clicked" not in st.session_state:
    st.session_state.start_clicked = False

# Check the state of the candle
if "candle_blown" not in st.session_state:
    st.session_state.candle_blown = False

if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0

if "show_slideshow" not in st.session_state:
    st.session_state.show_slideshow = False

if "show_candle" not in st.session_state:
    st.session_state.show_candle = False


# --- FUNCTION DEFINITIONS ---

def show_volume_question():
    """Displays the initial question about the music volume."""
    st.markdown("""
        <h2 style='text-align: center; color: #B5838D;'>Is your volume high enough to hear the background music? 🔊</h2>""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, it's high! ✅"):
            st.session_state.volume_checked = True
            st.session_state.volume_high = True
            st.rerun()
    with col2:
        if st.button("No, it's low! 🔇"):
            st.session_state.volume_checked = True
            st.session_state.volume_high = False
            st.rerun()

def show_volume_feedback():
    music_path = "assets/music.mp3"
    if os.path.exists(music_path):
        audio_bytes = open(music_path, "rb").read()
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
    else:
        st.warning("Background music file missing!")

    if st.session_state.volume_high:
        col1, col2 = st.columns([1, 2])
        with col1:
            if os.path.exists("assets/good_girl.jpg"):
                st.image("assets/good_girl.jpg", caption="Good girl! Enjoy the music 🎶", use_container_width=True)
    else:
        if os.path.exists("assets/funny_increase_volume.jpg"):
            st.image("assets/funny_increase_volume.jpg", caption="Then increase the volume! 🔊😂", use_container_width=True)



def load_lottie(filepath):
    """Loads a Lottie animation from a JSON file."""
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None

def show_cats():
    """Displays the cat memes section."""
    cat1, cat2, cat3 = st.columns(3)
    with cat1:
        st.video("assets/cat1.mp4")
    with cat2:
        st.image("assets/cat2.gif", use_container_width=True)
    with cat3:
        # Corrected: Use st.video for .mp4 file
        st.video("assets/cat3.mp4", width=400)

def show_slideshow(gallery):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Previous"):
            st.session_state.slide_index -= 1
            st.rerun()
    with col3:
        if st.button("Next ➡️") and st.session_state.slide_index < len(gallery) - 1:
            st.session_state.slide_index += 1
            st.rerun()

    index = st.session_state.slide_index
    file_path, caption = gallery[index]

    if file_path.endswith(".mp4"):
        st.video(file_path, width=600)
    else:
        st.image(file_path, use_container_width=True)

    if caption:
        st.markdown(f"<div style='text-align: center; font-style: italic; color: #6D6875;'>{caption}</div>", unsafe_allow_html=True)
    
    # Add special text slides
    if index == 1:
        st.markdown("<h3 style='text-align:center;'>📝 Model bolthe pics of yours cause you are already model 😎</h3>", unsafe_allow_html=True)
    elif index == 7:
        st.markdown("<h3 style='text-align:center;'>💡 Some talents of yours</h3>", unsafe_allow_html=True)
    elif index == 9:
        st.markdown("<h3 style='text-align:center;'>🔥 Remember the name: OG SHS</h3>", unsafe_allow_html=True)
    elif index == 18:
        st.markdown("<h3 style='text-align:center;'>🧡 You and me? 👉👈</h3>", unsafe_allow_html=True)
    elif index == 20:
        st.markdown("<h3 style='text-align:center;'>🎬 Leaked script of 'I would listen whatever you say'</h3>", unsafe_allow_html=True)

    st.markdown(f"**Slide {index + 1} of {len(gallery)}**", unsafe_allow_html=True)
    st.divider()

    st.markdown("<h3 style='text-align: center;'>Enjoy some cat memes before you blow out the candles! 😺</h3>", unsafe_allow_html=True)
    show_cats()
    st.divider()



# --- MAIN APP LOGIC ---

# Show the initial volume check question
if not st.session_state.volume_checked:
    show_volume_question()
# Otherwise, show the feedback
else:
    show_volume_feedback()

# Show the disclaimer if the app hasn't started yet
if not st.session_state.start_clicked:
    st.markdown("""
        <div style='text-align: center; padding-top: 100px;'>
            <h2 style='color: #B5838D;'>DISCLAIMER 😓</h2>
            <p style='font-size: 24px; color: #6D6875;'>
                Don't judge me by this shi, beginner hui yr 😭🫠
            </p>
        </div>
    """, unsafe_allow_html=True)
    if os.path.exists("assets/cat_disclaimer.jpg"):
        st.image("assets/cat_disclaimer.jpg", width=300)
    else:
        st.warning("Couldn't find cat_disclaimer.jpg — make sure it's in the assets folder.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👉👈 WANT TO CONTINUE"):
            st.session_state.start_clicked = True
            st.rerun()
    with col2:
        # Note: both buttons do the same thing, but are on the same line
        if st.button("👉👈 WANT TO CONTIUE"):
            st.session_state.start_clicked = True
            st.rerun()

# This is the main part of the app that runs after the user clicks "Continue"
if st.session_state.start_clicked:
    decorations = load_lottie("assets/decorations.json")
    if decorations:
        st_lottie(decorations, speed=1, loop=True, height=300)

    st.markdown("""
        <h1 style='text-align: center; color: #E5989B;'>🎉 Happy Birthday My Love 🎉</h1>
        <h3 style='text-align: center; color: #6D6875;'>Sherly Leona</h3>
    """, unsafe_allow_html=True)

    if not st.session_state.show_slideshow:
        if st.button("💖 Want to know how special you are? 💖"):
            st.session_state.show_slideshow = True
            st.session_state.slide_index = 0
            st.rerun()
    
    if st.session_state.show_slideshow:
        st.success("Here are some memories we made together 💫")

        # Your slideshow gallery logic
        gallery = [
            ("media/video1.mp4", "hehe Mandatory post🤭"),
            ("media/photo1.jpg", "Oops! That's an angel pic though"),
            ("media/photo2.jpg", "Aa expression chudu 😍"),
            ("media/photo3.jpg", "Topper pilla"),
            ("media/photo4.jpg", "That suit suits you (ignore the clarity i stole it from random source)"),
            ("media/photo5.jpg", "🫠you look so beautiful."),
            ("media/photo6.jpg", "Even in this and always!!"),
            ("media/photo7.jpg", "No words asala. MIND BLOWING"),
            ("media/photo8.jpg", "Evaro chef avutharu anaru, cap sariga petukodam kuda radhu😓"),
            ("media/photo9.jpg", "(let's omit me😎🙏)"),
            ("media/photo10.jpg", "Home celebration 🏠"),
            ("media/video2.mp4", "Pani pata leni manushulu part 1"),
            ("media/video3.mp4", "Part 2"),
            ("media/video4.mp4", "Part 3"),
            ("media/photo12.jpg", "Part 4"),
            ("media/photo13.jpg", "Part 5"),
            ("media/photo14.jpg", "pichi stage: unreachable😋"),
            ("media/photo15.jpg", "How cute naa"),
            ("media/photo16.jpg", ""),
            ("media/photo17.jpg", ""),
            ("media/photo18.jpg", ""),
            ("media/photo19.jpg", ""),
            ("media/photo20.jpg", ""),
            ("media/photo21.jpg", "Sassy People"),
            ("media/photo22.jpg", "")
        ]

        show_slideshow(gallery)

        if st.button("Go back"):
            st.session_state.show_slideshow = False
            st.rerun()

        # 🎂 Cake section - this is the new, correct, and working code.
                # 🎂 Cake section
        st.markdown("<h3 style='text-align: center;'>🎂 Blow the candles on your cake 🎂</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Make a wish and blow near your mic 🎤</p>", unsafe_allow_html=True)

        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_left:
            st.video("assets/cat1.mp4")
        with col_center:
            if st.session_state.candle_blown:
                st.image("assets/cake_blown.gif", use_container_width=True)
                st.success("You blew out the candles! Happy Birthday! 🥳")
            else:
                st.image("assets/cake_with_candles.gif", use_container_width=True)
        with col_right:
            st.video("assets/cat3.mp4")

        def get_base64_gif(path):
            with open(path, "rb") as f:
                data = f.read()
            return "data:image/gif;base64," + base64.b64encode(data).decode()

        candle_unlit_b64 = get_base64_gif("assets/cake_with_candles.gif")
        candle_blown_b64 = get_base64_gif("assets/cake_blown.gif")

        with open("blow_candle.html", "r", encoding="utf-8") as f:
            html_template = f.read()

        html_code = html_template.replace("{{candle_unlit}}", candle_unlit_b64)\
                                 .replace("{{candle_blown}}", candle_blown_b64)

        components.html(html_code, height=600)

        if st.session_state.candle_blown and st.button("Light the candles again"):
            st.session_state.candle_blown = False
            st.rerun()


    else:
        st.info("Click the button to unlock a surprise! 💌")
