import streamlit as st
import os
import io
import base64
import requests
import time
import urllib.parse
from PIL import Image
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Creative AI Studio - AI Gallery",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Resolve paths dynamically
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BG_PATH = os.path.join(CURRENT_DIR, "assets", "background.jpg")

# Helper to get base64 string of the background image
def get_base64_img(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

base64_bg = get_base64_img(BG_PATH)

# Custom premium CSS injection
css_style = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=JetBrains+Mono:wght@400;500&display=swap');

/* Main background & page container */
.stApp {{
    background: linear-gradient(135deg, #F7F4ED 0%, #EAE7DA 100%) !important;
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #3F352E !important;
}}

/* Hide Streamlit elements */
header, footer, [data-testid="stHeader"] {{
    visibility: hidden !important;
    height: 0 !important;
}}

/* Background Animation Layers */
.bg-layer-1 {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: linear-gradient(135deg, #F7F4ED 0%, #EAE7DA 100%);
    z-index: -3;
    pointer-events: none;
}}
.bg-layer-2 {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -2;
    pointer-events: none;
    overflow: hidden;
}}
.halo-1 {{
    position: absolute;
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, rgba(225, 209, 186, 0.45) 0%, rgba(225, 209, 186, 0) 70%);
    top: -150px;
    left: -150px;
}}
.halo-2 {{
    position: absolute;
    width: 900px;
    height: 900px;
    background: radial-gradient(circle, rgba(164, 137, 119, 0.16) 0%, rgba(164, 137, 119, 0) 80%);
    bottom: -250px;
    right: -250px;
}}
.bg-layer-3 {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1;
    pointer-events: none;
    overflow: hidden;
}}

/* Parallax floating sketch animations */
@keyframes float-slow {{
    0% {{ transform: translateY(0px) rotate(0deg); }}
    50% {{ transform: translateY(-15px) rotate(4deg); }}
    100% {{ transform: translateY(0px) rotate(0deg); }}
}}
@keyframes float-medium {{
    0% {{ transform: translateY(0px) rotate(0deg); }}
    50% {{ transform: translateY(-25px) rotate(-6deg); }}
    100% {{ transform: translateY(0px) rotate(0deg); }}
}}
@keyframes float-fast {{
    0% {{ transform: translateY(0px) rotate(0deg); }}
    50% {{ transform: translateY(-20px) rotate(5deg); }}
    100% {{ transform: translateY(0px) rotate(0deg); }}
}}
.floating-sketch {{
    position: absolute;
    z-index: 0;
    pointer-events: none;
    opacity: 0.05; /* 5% opacity, fits 3% - 8% perfectly */
    stroke: #A48977;
    stroke-width: 1.2;
    fill: none;
}}

/* Custom Typography */
h1, h2, h3, h4, h5, h6, .main-title, .logo-title {{
    font-family: 'Playfair Display', serif !important;
    color: #3F352E !important;
}}

/* Glassmorphism card utility */
.glass-card {{
    background: rgba(234, 231, 218, 0.72) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border: 1px solid rgba(164, 137, 119, 0.18) !important;
    border-radius: 20px !important;
    padding: 24px;
    box-shadow: 0 8px 32px 0 rgba(164, 137, 119, 0.06) !important;
    margin-bottom: 24px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}
.glass-card:hover {{
    border-color: rgba(164, 137, 119, 0.3) !important;
    box-shadow: 0 12px 40px 0 rgba(164, 137, 119, 0.1) !important;
}}

/* Logo and brand styles */
.logo-container {{
    display: flex;
    align-items: center;
    margin-bottom: 25px;
}}
.logo-icon {{
    border: 1.5px solid #A48977;
    background: transparent;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin-right: 14px;
    display: inline-block;
    position: relative;
}}
.logo-icon::after {{
    content: '';
    position: absolute;
    width: 12px;
    height: 12px;
    border: 1px solid #A48977;
    border-radius: 50%;
    top: 8px;
    left: 8px;
}}
.logo-text-block {{
    display: flex;
    flex-direction: column;
}}
.logo-title {{
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 20px;
    letter-spacing: 0.5px;
    color: #3F352E;
    line-height: 1.1;
}}
.logo-subtitle {{
    font-size: 9px;
    color: #A48977;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 600;
    font-family: 'Outfit', sans-serif;
}}

/* Main titles */
.main-title {{
    font-family: 'Playfair Display', serif;
    font-size: 48px;
    font-weight: 700;
    color: #3F352E !important;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}}
.main-subtitle {{
    font-size: 15px;
    color: #A48977;
    margin-bottom: 35px;
    font-weight: 400;
    font-family: 'Outfit', sans-serif;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

/* AI Gallery frame style for result image */
.gallery-frame {{
    background: #F7F4ED !important;
    border: 8px solid #EAE7DA !important;
    outline: 1px solid rgba(164, 137, 119, 0.25) !important;
    border-radius: 4px !important;
    padding: 16px !important;
    box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.03), 0 10px 25px rgba(164, 137, 119, 0.1) !important;
    margin-bottom: 24px !important;
    text-align: center;
}}
.gallery-frame img {{
    border: 1px solid rgba(164, 137, 119, 0.15) !important;
}}

/* Custom placeholder / box for generated image */
.generated-box {{
    border: 1px dashed rgba(164, 137, 119, 0.3) !important;
    border-radius: 20px !important;
    background: rgba(234, 231, 218, 0.35) !important;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    color: #A48977;
    padding: 24px;
    text-align: center;
}}
.generated-title-text {{
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 20px;
    color: #3F352E;
    font-family: 'Playfair Display', serif;
}}

/* Custom styling for standard Streamlit Text Area */
div[data-testid="stTextArea"] textarea {{
    background: rgba(254, 253, 250, 0.8) !important;
    border: 1px solid rgba(164, 137, 119, 0.25) !important;
    border-radius: 12px !important;
    color: #3F352E !important;
    font-size: 15px !important;
    padding: 16px !important;
    font-family: 'Outfit', sans-serif !important;
    transition: all 0.3s ease !important;
}}
div[data-testid="stTextArea"] textarea:focus {{
    border-color: #A48977 !important;
    box-shadow: 0 0 10px rgba(164, 137, 119, 0.15) !important;
}}
div[data-testid="stTextArea"] label p {{
    color: #A48977 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    margin-bottom: 6px !important;
}}

/* Custom styling for streamlit buttons */
div.stButton > button {{
    background: #A48977 !important;
    border: none !important;
    border-radius: 12px !important;
    color: #F7F4ED !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 14px 28px !important;
    width: 100% !important;
    box-shadow: 0 4px 12px rgba(164, 137, 119, 0.15) !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
    letter-spacing: 0.8px !important;
}}
div.stButton > button:hover {{
    background: #8F7564 !important;
    box-shadow: 0 6px 18px rgba(164, 137, 119, 0.25) !important;
    color: #F7F4ED !important;
    transform: translateY(-1px) !important;
}}
div.stButton > button:active {{
    transform: translateY(1px) !important;
}}

/* Mode Cards Overlay Mechanics */
div[data-testid="column"]:has(.mode-card-wrapper) {{
    position: relative !important;
}}
div[data-testid="column"]:has(.mode-card-wrapper) div.stButton {{
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    z-index: 10 !important;
    margin: 0 !important;
    padding: 0 !important;
}}
div[data-testid="column"]:has(.mode-card-wrapper) div.stButton > button {{
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    opacity: 0 !important;
    border: none !important;
    background: transparent !important;
    cursor: pointer !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}}

.mode-card-wrapper {{
    position: relative;
    width: 100%;
    height: 120px;
    margin-bottom: 20px;
}}
.mode-card {{
    background: rgba(255, 255, 255, 0.85) !important;
    border: 1px solid rgba(164, 137, 119, 0.35) !important;
    border-radius: 18px !important;
    padding: 20px !important;
    color: #4A2E1F !important;
    box-shadow: 0 10px 30px rgba(164, 137, 119, 0.12) !important;
    transition: all 0.3s ease !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}}
.mode-card.card-active {{
    border: 2px solid #A48977 !important;
    background: rgba(164, 137, 119, 0.12) !important;
}}
.mode-card:hover, div[data-testid="column"]:has(.mode-card-wrapper):hover .mode-card {{
    transform: translateY(-4px) !important;
    border-color: #A48977 !important;
    box-shadow: 0 14px 35px rgba(164, 137, 119, 0.18) !important;
}}
.card-title {{
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #4A2E1F !important;
    margin-bottom: 6px !important;
}}
.card-desc {{
    color: #7A6A5E !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}}

/* Badge styling */
.badge-container {{
    display: flex;
    gap: 10px;
    margin-top: 14px;
    align-items: center;
}}
.badge-label {{
    font-size: 12px;
    color: #A48977;
}}
.badge-tag {{
    background: rgba(234, 231, 218, 0.6);
    border: 1px solid rgba(164, 137, 119, 0.25);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 11px;
    font-family: 'Outfit', sans-serif;
    color: #3F352E;
}}

/* Tip list items */
.tip-item {{
    display: flex;
    align-items: flex-start;
    margin-bottom: 12px;
    font-size: 13.5px;
    color: #3F352E;
    line-height: 1.4;
}}
.tip-bullet {{
    color: #A48977;
    margin-right: 10px;
    font-size: 14px;
}}

/* Styled header for section cards */
.section-title {{
    font-family: 'Playfair Display', serif;
    font-size: 16px;
    font-weight: 700;
    color: #3F352E;
    margin-bottom: 16px;
    letter-spacing: 0.5px;
    border-bottom: 1px solid rgba(164, 137, 119, 0.18);
    padding-bottom: 8px;
}}

/* Styled Alert elements */
.alert-card {{
    background: rgba(164, 137, 119, 0.1);
    border: 1px solid rgba(164, 137, 119, 0.3);
    border-radius: 12px;
    padding: 16px;
    color: #3F352E;
    font-size: 14px;
    margin-bottom: 20px;
}}

/* --- FLOATING AI GALLERY (POLAROIDS) --- */
.floating-gallery-container {{
    position: fixed;
    top: 0;
    right: 0;
    width: 32%;
    height: 100vh;
    pointer-events: none;
    z-index: -1 !important;
    overflow: hidden;
}}
.polaroid-card {{
    background: #FFFFFF !important;
    border: 1px solid rgba(164, 137, 119, 0.15) !important;
    border-radius: 8px !important;
    padding: 10px !important;
    padding-bottom: 25px !important;
    box-shadow: 0 10px 25px rgba(164, 137, 119, 0.08) !important;
    position: absolute;
    width: 120px !important;
    opacity: 0.35; /* 20% to 40% range */
    transition: all 0.3s ease;
    pointer-events: none;
    text-align: center;
}}
.polaroid-card .art-placeholder {{
    width: 100%;
    aspect-ratio: 1;
    background: #F7F4ED;
    border: 1px solid rgba(164, 137, 119, 0.08);
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 6px;
}}
.polaroid-card .art-placeholder svg {{
    width: 100%;
    height: 100%;
}}
.polaroid-card .art-caption {{
    font-family: 'Playfair Display', serif;
    font-size: 9px;
    color: #A48977;
    margin-top: 6px;
    font-weight: 500;
}}

/* Polaroids layout & animations */
.pc-1 {{ top: 12%; right: 14%; filter: blur(0.5px); animation: float-polaroid-1 12s infinite ease-in-out; }}
.pc-2 {{ top: 35%; right: 3%; filter: blur(1px); animation: float-polaroid-2 15s infinite ease-in-out; }}
.pc-3 {{ top: 58%; right: 15%; filter: blur(0.5px); animation: float-polaroid-3 14s infinite ease-in-out; }}
.pc-4 {{ top: 22%; right: 2%; filter: blur(1.5px); animation: float-polaroid-4 16s infinite ease-in-out; }}
.pc-5 {{ top: 48%; right: 9%; filter: blur(0.5px); animation: float-polaroid-5 13s infinite ease-in-out; }}
.pc-6 {{ top: 72%; right: 3%; filter: blur(1px); animation: float-polaroid-6 17s infinite ease-in-out; }}

@keyframes float-polaroid-1 {{
    0%, 100% {{ transform: translateY(0) rotate(-5deg); }}
    50% {{ transform: translateY(-12px) rotate(-3deg); }}
}}
@keyframes float-polaroid-2 {{
    0%, 100% {{ transform: translateY(0) rotate(4deg); }}
    50% {{ transform: translateY(-18px) rotate(6deg); }}
}}
@keyframes float-polaroid-3 {{
    0%, 100% {{ transform: translateY(0) rotate(-3deg); }}
    50% {{ transform: translateY(-14px) rotate(-1deg); }}
}}
@keyframes float-polaroid-4 {{
    0%, 100% {{ transform: translateY(0) rotate(5deg); }}
    50% {{ transform: translateY(-16px) rotate(3deg); }}
}}
@keyframes float-polaroid-5 {{
    0%, 100% {{ transform: translateY(0) rotate(-4deg); }}
    50% {{ transform: translateY(-10px) rotate(-6deg); }}
}}
@keyframes float-polaroid-6 {{
    0%, 100% {{ transform: translateY(0) rotate(6deg); }}
    50% {{ transform: translateY(-15px) rotate(4deg); }}
}}

/* --- BUBBLE TO ART BACKGROUND ANIMATION --- */
.bubble-container {{
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: -2;
    overflow: hidden;
}}

.art-bubble {{
    position: absolute;
    bottom: -100px;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
}}

.bubble-shell-wrapper {{
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.bubble-shell {{
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    border: 1px solid rgba(164, 137, 119, 0.25);
    background: radial-gradient(circle at 30% 30%, rgba(241, 230, 216, 0.3) 0%, rgba(164, 137, 119, 0.08) 70%, rgba(164, 137, 119, 0.15) 100%);
    box-shadow: inset 0 0 8px rgba(255, 255, 255, 0.4), 0 2px 10px rgba(164, 137, 119, 0.05);
}}

.bubble-cracks {{
    position: absolute;
    width: 90%;
    height: 90%;
    opacity: 0;
    pointer-events: none;
}}

.pop-icon-wrapper {{
    position: absolute;
    width: 60%;
    height: 60%;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
}}

.pop-icon-wrapper svg {{
    width: 100%;
    height: 100%;
}}

/* Individual bubble configurations */
.ab-1 {{ width: 70px; height: 70px; left: 10%; --max-op: 0.08; --icon-op: 0.28; --sway-x: -15px; animation: rise-translate 15s infinite linear; }}
.ab-2 {{ width: 85px; height: 85px; left: 26%; --max-op: 0.11; --icon-op: 0.32; --sway-x: 20px; animation: rise-translate 18s infinite linear 3s; }}
.ab-3 {{ width: 60px; height: 60px; left: 42%; --max-op: 0.07; --icon-op: 0.25; --sway-x: -10px; animation: rise-translate 13s infinite linear 1.5s; }}
.ab-4 {{ width: 90px; height: 90px; left: 58%; --max-op: 0.12; --icon-op: 0.35; --sway-x: 18px; animation: rise-translate 17s infinite linear 4.5s; }}
.ab-5 {{ width: 65px; height: 65px; left: 74%; --max-op: 0.09; --icon-op: 0.30; --sway-x: -20px; animation: rise-translate 16s infinite linear 2s; }}
.ab-6 {{ width: 75px; height: 75px; left: 88%; --max-op: 0.06; --icon-op: 0.26; --sway-x: 12px; animation: rise-translate 19s infinite linear 5.5s; }}

/* Animation assignments */
.art-bubble .bubble-shell {{ animation: shell-pop 15s infinite linear inherit; }}
.art-bubble .bubble-cracks {{ animation: cracks-pop 15s infinite linear inherit; }}
.art-bubble .pop-icon-wrapper {{ animation: icon-release 15s infinite linear inherit; }}

/* Apply inheritance properties to inner animations to sync duration and delay */
.ab-1 .bubble-shell, .ab-1 .bubble-cracks, .ab-1 .pop-icon-wrapper {{ animation-duration: 15s; animation-delay: 0s; }}
.ab-2 .bubble-shell, .ab-2 .bubble-cracks, .ab-2 .pop-icon-wrapper {{ animation-duration: 18s; animation-delay: 3s; }}
.ab-3 .bubble-shell, .ab-3 .bubble-cracks, .ab-3 .pop-icon-wrapper {{ animation-duration: 13s; animation-delay: 1.5s; }}
.ab-4 .bubble-shell, .ab-4 .bubble-cracks, .ab-4 .pop-icon-wrapper {{ animation-duration: 17s; animation-delay: 4.5s; }}
.ab-5 .bubble-shell, .ab-5 .bubble-cracks, .ab-5 .pop-icon-wrapper {{ animation-duration: 16s; animation-delay: 2s; }}
.ab-6 .bubble-shell, .ab-6 .bubble-cracks, .ab-6 .pop-icon-wrapper {{ animation-duration: 19s; animation-delay: 5.5s; }}

/* Keyframe Animations */
@keyframes rise-translate {{
    0% {{ transform: translateY(110vh) translateX(0); opacity: 0; }}
    8% {{ opacity: 1; }}
    50% {{ transform: translateY(50vh) translateX(var(--sway-x)); opacity: 1; }}
    50.1% {{ opacity: 0.35; }}
    100% {{ transform: translateY(-5vh) translateX(calc(var(--sway-x) * -1.2)); opacity: 0; }}
}}

@keyframes shell-pop {{
    0% {{ opacity: calc(var(--max-op) * 0.8); transform: scale(0.8); }}
    8% {{ opacity: var(--max-op); }}
    40% {{ opacity: var(--max-op); transform: scale(1) rotate(0deg); }}
    44% {{ opacity: calc(var(--max-op) * 1.2); transform: scale(1.05) rotate(3deg); }}
    47% {{ opacity: calc(var(--max-op) * 0.9); transform: scale(0.95) rotate(-3deg); }}
    49% {{ opacity: calc(var(--max-op) * 1.3); transform: scale(1.1) rotate(1deg); }}
    49.9% {{ opacity: calc(var(--max-op) * 1.3); transform: scale(1.15) rotate(0deg); }}
    50% {{ opacity: 0; transform: scale(1.4); }}
    100% {{ opacity: 0; transform: scale(1.4); }}
}}

@keyframes cracks-pop {{
    0%, 40% {{ opacity: 0; transform: scale(0.8); }}
    44% {{ opacity: 0.08; transform: scale(0.95); }}
    49% {{ opacity: 0.15; transform: scale(1.05); }}
    49.9% {{ opacity: 0.18; transform: scale(1.1); }}
    50%, 100% {{ opacity: 0; }}
}}

@keyframes icon-release {{
    0%, 49.9% {{ opacity: 0; transform: scale(0.5) translateY(15px); }}
    50% {{ opacity: var(--icon-op); transform: scale(1.2) translateY(0); }}
    60% {{ opacity: calc(var(--icon-op) * 0.8); transform: scale(1) translateY(-15px); }}
    100% {{ opacity: 0; transform: scale(0.7) translateY(-60px); }}
}}

/* Ensure all interactive elements stack above backgrounds */
div[data-testid="stTextArea"], 
div[data-testid="stTextInput"], 
div[data-testid="stSelectbox"], 
div.stButton, 
.mode-card-wrapper,
.glass-card {{
    position: relative;
    z-index: 10 !important;
}}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# Initialize Session States
if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = ""
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None
if "error_message" not in st.session_state:
    st.session_state.error_message = None
if "generation_mode" not in st.session_state:
    st.session_state.generation_mode = "快速圖片生成"
if "generated_mode" not in st.session_state:
    st.session_state.generated_mode = "快速圖片生成"
if "last_api_prompt" not in st.session_state:
    st.session_state.last_api_prompt = ""

# Example selection helper
def set_prompt(text):
    st.session_state.prompt_text = text
    st.session_state.error_message = None

# Helper to translate text to English using Google Translate free endpoint (with auto-detect)
def translate_to_english(text: str) -> str:
    if not text.strip():
        return ""
    
    # Check if text is pure ASCII
    try:
        text.encode('ascii')
        return text
    except UnicodeEncodeError:
        pass
        
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={urllib.parse.quote(text)}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            result = response.json()
            translated_text = "".join([sentence[0] for sentence in result[0] if sentence[0]])
            return translated_text
    except Exception:
        pass
    return text

def translate_and_enhance_prompt(prompt_text: str, mode: str) -> str:
    # 1. Translate to English
    translated = translate_to_english(prompt_text.strip())
    
    # 2. Format / Clean / Reinforce
    if mode == "商業 Logo 生成":
        # Remove keywords like "logo", "Logo" to avoid redundancies in template wrapping
        cleaned = translated.replace("logo", "").replace("Logo", "").replace("LOGO", "").strip()
        cleaned = cleaned.strip(",. ").strip()
        enhanced = f"Professional business logo for {cleaned}, minimalist vector logo, modern fintech brand identity, clean geometric symbol, premium corporate identity, vector graphic, no mockup, no watermark"
    elif mode == "精準深層生成":
        enhanced = f"{translated}, masterpiece, ultra detailed, professional composition, cinematic lighting, commercial quality, realistic textures, premium visual quality"
    else: # 快速圖片生成
        enhanced = translated
        
    return enhanced

# Core Inference API Call function
def run_image_generation(prompt: str):
    raw_token = os.getenv("HF_TOKEN")
    if not raw_token:
        st.session_state.error_message = "🔑 API Token is missing! Please configure the `HF_TOKEN` environment variable or Streamlit Secrets."
        return
    
    # Sanitize token to avoid UnicodeEncodeError (latin-1) caused by copy-pasted smart quotes, white spaces or invisible unicode characters
    hf_token = raw_token.strip().strip("'\"").replace("“", "").replace("”", "").replace("‘", "").replace("’", "")
    hf_token = "".join(c for c in hf_token if ord(c) < 128)
    
    # Try the CloudFront router endpoint first (bypasses DNS block issues in some networks) with the standard domain as fallback
    api_urls = [
        "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell",
        "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    ]
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": prompt}
    
    max_retries = 3
    retry_delay = 6
    
    for api_url in api_urls:
        for attempt in range(max_retries):
            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=60)
                
                if response.status_code == 200:
                    try:
                        img_bytes = response.content
                        image = Image.open(io.BytesIO(img_bytes))
                        st.session_state.generated_image = image
                        st.session_state.error_message = None
                        return
                    except Exception as img_err:
                        st.session_state.error_message = f"🖼️ Image loading error: Received bytes could not be decoded. Details: {str(img_err)}"
                        return
                        
                elif response.status_code == 503:
                    # Model is currently loading, wait and retry
                    try:
                        error_json = response.json()
                        wait_time = float(error_json.get("estimated_time", retry_delay))
                    except Exception:
                        wait_time = retry_delay
                    
                    if attempt < max_retries - 1:
                        with st.spinner(f"⏳ AI system is initializing (attempt {attempt+1}/{max_retries}). Waiting {int(wait_time)}s..."):
                            time.sleep(wait_time)
                        continue
                    else:
                        break
                        
                elif response.status_code == 401:
                    st.session_state.error_message = "🔒 Authentication Failed: The provided `HF_TOKEN` is invalid or does not have permissions. Please check your credentials."
                    return
                else:
                    try:
                        error_msg = response.json().get("error", f"HTTP status {response.status_code}")
                    except Exception:
                        error_msg = f"HTTP {response.status_code} error response"
                    st.session_state.error_message = f"🚨 API Error: {error_msg}"
                    break
                    
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                break  # Try next api_url if this one fails to connect
            except requests.exceptions.RequestException as e:
                st.session_state.error_message = f"🔌 Network connection failure: Details: {str(e)}"
                return
                
        if st.session_state.generated_image:
            return
            
    if not st.session_state.error_message:
        st.session_state.error_message = "❌ Failed to connect to the generation server. Please verify your internet connection."



# --- PAGE LAYOUT SETUP ---

# Background三層結構與浮動線稿插畫 SVG 注入
background_html = """
<div class="bg-layer-1"></div>
<div class="bg-layer-2">
    <div class="halo-1"></div>
    <div class="halo-2"></div>
</div>
<div class="bg-layer-3">
    <!-- Coffee Cup -->
    <svg class="floating-sketch" style="width:120px; height:120px; top:12%; left:4%; animation: float-slow 18s infinite;" viewBox="0 0 100 100">
        <path d="M30 40 h40 v30 c0 10 -8 18 -18 18 s-18 -8 -18 -18 z M70 45 h6 c5 0 8 3 8 8 s-3 8 -8 8 h-6 M25 90 h50 M45 20 v10 M55 18 v12 M35 22 v8" stroke="#A48977" stroke-width="1" fill="none"/>
    </svg>
    <!-- Cake -->
    <svg class="floating-sketch" style="width:110px; height:110px; top:75%; left:6%; animation: float-fast 12s infinite;" viewBox="0 0 100 100">
        <path d="M20 50 h60 v30 h-60 z M25 50 c0-5 5-10 10-10 h30 c5 0 10 5 10 10 M50 25 v15 M50 25 c0-3 3-5 5-5 s5 2 5 5-3 5-5 5-5-2-5-5 M20 65 h60 M20 75 h60" stroke="#A48977" stroke-width="1" fill="none"/>
    </svg>
    <!-- Burger -->
    <svg class="floating-sketch" style="width:120px; height:120px; top:45%; left:50%; animation: float-slow 22s infinite;" viewBox="0 0 100 100">
        <path d="M20 45 c0-15 15-20 30-20 s30 5 30 20 z M15 50 h70 v5 h-70 z M20 60 c0 10 15 15 30 15 s30-5 30-15 z M25 50 c2 4 6 4 8 0 s6-4 8 0 s6 4 8 0 s6-4 8 0 s6 4 8 0 s6-4 8 0" stroke="#A48977" stroke-width="1" fill="none"/>
    </svg>
    <!-- Luxury Car -->
    <svg class="floating-sketch" style="width:160px; height:160px; top:70%; left:48%; animation: float-medium 20s infinite;" viewBox="0 0 100 100">
        <path d="M10 70 h10 c2-8 10-8 12 0 h36 c2-8 10-8 12 0 h10 v-10 c0-5-5-10-15-12 l-15-15 h-20 l-15 25 h-15 z M22 70 c0-5 4-9 9-9 s9 4 9 9 s-4 9-9 9 s-9-4-9-9 M68 70 c0-5 4-9 9-9 s9 4 9 9 s-4 9-9 9 s-9-4-9-9" stroke="#A48977" stroke-width="1" fill="none"/>
    </svg>
    <!-- Camera -->
    <svg class="floating-sketch" style="width:130px; height:130px; top:35%; left:3%; animation: float-slow 16s infinite;" viewBox="0 0 100 100">
        <path d="M15 35 h20 l5-10 h20 l5 10 h20 v45 h-70 z M50 62 c10 0 18-8 18-18 s-8-18-18-18 s-18 8-18 18 s8 18 18 18 M50 54 c5 0 10-5 10-10 s-5-10-10-10 s-10 5-10 10 s-5 10-10 10 M75 42 h5 v5 h-5 z" stroke="#A48977" stroke-width="1" fill="none"/>
    </svg>
    <!-- Building -->
    <svg class="floating-sketch" style="width:150px; height:150px; top:15%; right:5%; animation: float-medium 24s infinite;" viewBox="0 0 100 100">
        <path d="M20 90 v-60 l30-15 l30 15 v60 z M20 45 h60 M50 15 v75 M30 35 h10 v10 h-10 z M30 55 h10 v10 h-10 z M30 75 h10 v15 h-10 z M60 35 h10 v10 h-10 z M60 55 h10 v10 h-10 z M60 75 h10 v15 h-10 z" stroke="#A48977" stroke-width="1" fill="none"/>
    </svg>
    <!-- Geometric Logo -->
    <svg class="floating-sketch" style="width:140px; height:140px; top:48%; right:2%; animation: float-fast 14s infinite;" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="30" stroke="#A48977" stroke-width="1" fill="none"/>
        <rect x="20" y="20" width="60" height="60" stroke="#A48977" stroke-width="1" stroke-dasharray="2,2" fill="none"/>
        <line x1="10" y1="10" x2="90" y2="90" stroke="#A48977" stroke-width="0.5" stroke-dasharray="4,4"/>
        <line x1="90" y1="10" x2="10" y2="90" stroke="#A48977" stroke-width="0.5" stroke-dasharray="4,4"/>
        <circle cx="50" cy="50" r="18" stroke="#A48977" stroke-width="0.5" stroke-dasharray="2,2"/>
    </svg>
    <!-- Artwork Frame -->
    <svg class="floating-sketch" style="width:150px; height:150px; top:75%; right:6%; animation: float-medium 21s infinite;" viewBox="0 0 100 100">
        <rect x="15" y="15" width="70" height="70" stroke="#A48977" stroke-width="1" fill="none"/>
        <rect x="25" y="25" width="50" height="50" stroke="#A48977" stroke-width="0.5" stroke-dasharray="2,2" fill="none"/>
        <line x1="50" y1="0" x2="50" y2="15" stroke="#A48977" stroke-width="1"/>
        <circle cx="50" cy="5" r="2" fill="#A48977"/>
    </svg>
</div>

<!-- Floating Polaroid AI Gallery (Right side) -->
<div class="floating-gallery-container">
    <!-- Polaroid 1: Fantasy Castle -->
    <div class="polaroid-card pc-1">
        <div class="art-placeholder">
            <svg viewBox="0 0 100 100" stroke="#A48977" stroke-width="1.2" fill="none">
                <path d="M25 80 h50 M30 80 v-30 h8 v30 M62 80 v-30 h8 v30 M38 80 v-20 h24 v20 M45 60 v-15 h10 v15" />
                <path d="M28 50 l6-12 6 12 Z M60 50 l6-12 6 12 Z M42 40 l8-15 8 15 Z" />
                <path d="M50 25 v-8 l4 2-4 2" />
                <path d="M15 65 c-3-3-8 0-6 4 c-2 5 3 7 7 5 M85 65 c3-3 8 0 6 4 c2 5-3 7-7 5" stroke-dasharray="2,2" />
            </svg>
        </div>
        <div class="art-caption">Fantasy Castle</div>
    </div>
    <!-- Polaroid 2: Cute Animal -->
    <div class="polaroid-card pc-2">
        <div class="art-placeholder">
            <svg viewBox="0 0 100 100" stroke="#A48977" stroke-width="1.2" fill="none">
                <circle cx="50" cy="55" r="22" />
                <path d="M33 39 L22 15 L38 35 M67 39 L78 15 L62 35" />
                <circle cx="42" cy="50" r="1.5" fill="#A48977" />
                <circle cx="58" cy="50" r="1.5" fill="#A48977" />
                <path d="M48 56 l2 2 l2-2 M45 61 c2-1 8-1 10 0" />
                <path d="M23 54 h8 M23 58 l8-1 M77 54 h-8 M77 58 l-8-1" />
            </svg>
        </div>
        <div class="art-caption">Cute Animal</div>
    </div>
    <!-- Polaroid 3: Cyber City -->
    <div class="polaroid-card pc-3">
        <div class="art-placeholder">
            <svg viewBox="0 0 100 100" stroke="#A48977" stroke-width="1.2" fill="none">
                <path d="M15 85 v-40 h15 v40 M30 85 v-60 h20 v65 M50 85 v-50 h15 v45 M65 85 v-30 h20 v30" />
                <path d="M20 50 h5 M20 60 h5 M20 70 h5 M37 35 h6 M37 45 h6 M37 55 h6 M37 65 h6 M37 75 h6 M58 45 h4 M58 55 h4 M58 65 h4 M58 75 h4" />
                <path d="M10 25 l30 20 M90 20 l-40 30" stroke-dasharray="3,3" />
            </svg>
        </div>
        <div class="art-caption">Cyber City</div>
    </div>
    <!-- Polaroid 4: AI Portrait -->
    <div class="polaroid-card pc-4">
        <div class="art-placeholder">
            <svg viewBox="0 0 100 100" stroke="#A48977" stroke-width="1.2" fill="none">
                <path d="M35 75 C38 65, 42 55, 45 48 C42 42, 42 35, 45 30 C48 25, 55 25, 58 30 C62 35, 62 42, 58 48 C62 55, 66 65, 70 75 M50 20 C52 18, 55 18, 57 20 M48 36 h4 M54 36 h4 M47 42 C50 44, 54 44, 57 42" />
                <path d="M45 28 C35 25, 30 35, 32 45 C34 55, 30 65, 25 70" />
                <path d="M58 28 C68 25, 73 35, 71 45 C69 55, 73 65, 78 70" stroke-dasharray="2,2" />
            </svg>
        </div>
        <div class="art-caption">AI Portrait</div>
    </div>
    <!-- Polaroid 5: Logo Design -->
    <div class="polaroid-card pc-5">
        <div class="art-placeholder">
            <svg viewBox="0 0 100 100" stroke="#A48977" stroke-width="1.2" fill="none">
                <circle cx="50" cy="50" r="24" />
                <circle cx="50" cy="50" r="14" />
                <path d="M20 50 h60 M50 20 v60 M28 28 l44 44 M28 72 l44-44" stroke-dasharray="2,2" />
                <rect x="47" y="17" width="6" height="6" />
                <rect x="47" y="77" width="6" height="6" />
                <rect x="17" y="47" width="6" height="6" />
                <rect x="77" y="47" width="6" height="6" />
            </svg>
        </div>
        <div class="art-caption">Logo Design</div>
    </div>
    <!-- Polaroid 6: Watercolor Art -->
    <div class="polaroid-card pc-6">
        <div class="art-placeholder">
            <svg viewBox="0 0 100 100" stroke="#A48977" stroke-width="1" fill="none">
                <path d="M30 45 c-10-5-20 5-15 15 s15 25 30 20 s15-20 10-25 s-15-5-25-10 Z" style="fill: rgba(225,209,186,0.3); stroke: none;" />
                <path d="M50 35 c10-5 20 5 15 15 s-5 25-20 20 s-15-20-10-25 s5-5 15-10 Z" style="fill: rgba(164,137,119,0.25); stroke: none;" />
                <path d="M42 52 c8-8 18-4 14 12 s-12 12-20 4 s0-12 8-16 Z" style="fill: rgba(234,231,218,0.45); stroke: none;" stroke="#A48977" stroke-width="1" />
                <circle cx="48" cy="48" r="30" stroke-dasharray="3,3" />
            </svg>
        </div>
        <div class="art-caption">Watercolor Art</div>
    </div>
</div>
"""
st.markdown(background_html, unsafe_allow_html=True)

# Bubble To Art Background Animation HTML
bubble_html = """
<div class="bubble-container">
    <!-- Bubble 1: Logo -->
    <div class="art-bubble ab-1">
        <div class="bubble-shell-wrapper">
            <div class="bubble-shell"></div>
            <svg class="bubble-cracks" viewBox="0 0 100 100">
                <path d="M50 50 L45 35 M50 50 L58 40 M50 50 L40 55 M50 50 L55 62 M50 50 L62 52 M50 50 L38 45" stroke="#A48977" stroke-width="1.5" stroke-linecap="round" fill="none" />
            </svg>
        </div>
        <div class="pop-icon-wrapper">
            <svg viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="30" stroke="#A48977" stroke-width="1.2" fill="none"/>
                <circle cx="50" cy="50" r="15" stroke="#A48977" stroke-width="0.8" fill="none"/>
                <line x1="50" y1="10" x2="50" y2="90" stroke="#A48977" stroke-width="0.5" stroke-dasharray="2,2"/>
                <line x1="10" y1="50" x2="90" y2="50" stroke="#A48977" stroke-width="0.5" stroke-dasharray="2,2"/>
            </svg>
        </div>
    </div>
    
    <!-- Bubble 2: Paint Brush -->
    <div class="art-bubble ab-2">
        <div class="bubble-shell-wrapper">
            <div class="bubble-shell"></div>
            <svg class="bubble-cracks" viewBox="0 0 100 100">
                <path d="M50 50 L42 38 M50 50 L60 38 M50 50 L38 52 M50 50 L58 60 M50 50 L64 48 M50 50 L36 44" stroke="#A48977" stroke-width="1.5" stroke-linecap="round" fill="none" />
            </svg>
        </div>
        <div class="pop-icon-wrapper">
            <svg viewBox="0 0 100 100">
                <path d="M35 65 L60 40 L65 45 L40 70 Z M60 40 L70 30 C72 28, 76 28, 78 30 C80 32, 80 36, 78 38 L68 48 Z M35 65 L25 75 L30 70 Z" stroke="#A48977" stroke-width="1.2" fill="none" stroke-linejoin="round"/>
                <path d="M25 75 L20 80 L22 73 Z" fill="#A48977"/>
            </svg>
        </div>
    </div>
    
    <!-- Bubble 3: Camera -->
    <div class="art-bubble ab-3">
        <div class="bubble-shell-wrapper">
            <div class="bubble-shell"></div>
            <svg class="bubble-cracks" viewBox="0 0 100 100">
                <path d="M50 50 L46 34 M50 50 L56 36 M50 50 L42 56 M50 50 L54 64 M50 50 L64 54 M50 50 L36 46" stroke="#A48977" stroke-width="1.5" stroke-linecap="round" fill="none" />
            </svg>
        </div>
        <div class="pop-icon-wrapper">
            <svg viewBox="0 0 100 100">
                <path d="M20 40 h15 l5-8 h20 l5 8 h15 v35 h-60 z" stroke="#A48977" stroke-width="1.2" fill="none" stroke-linejoin="round"/>
                <circle cx="50" cy="58" r="14" stroke="#A48977" stroke-width="1.2" fill="none"/>
                <circle cx="50" cy="58" r="7" stroke="#A48977" stroke-width="0.8" fill="none"/>
                <circle cx="70" cy="46" r="3" fill="#A48977"/>
            </svg>
        </div>
    </div>
    
    <!-- Bubble 4: Palette -->
    <div class="art-bubble ab-4">
        <div class="bubble-shell-wrapper">
            <div class="bubble-shell"></div>
            <svg class="bubble-cracks" viewBox="0 0 100 100">
                <path d="M50 50 L44 32 M50 50 L60 42 M50 50 L38 54 M50 50 L56 66 M50 50 L66 52 M50 50 L34 42" stroke="#A48977" stroke-width="1.5" stroke-linecap="round" fill="none" />
            </svg>
        </div>
        <div class="pop-icon-wrapper">
            <svg viewBox="0 0 100 100">
                <path d="M50 20 C25 20, 20 38, 20 55 C20 72, 38 80, 55 80 C68 80, 80 72, 80 58 C80 44, 75 42, 68 42 C64 42, 60 46, 56 46 C52 46, 50 38, 50 20 Z" stroke="#A48977" stroke-width="1.2" fill="none" stroke-linejoin="round"/>
                <circle cx="35" cy="40" r="3" fill="#A48977"/>
                <circle cx="45" cy="62" r="3" fill="#A48977"/>
                <circle cx="65" cy="62" r="3" fill="#A48977"/>
                <circle cx="68" cy="32" r="2.5" stroke="#A48977" stroke-width="0.8" fill="none"/>
            </svg>
        </div>
    </div>
    
    <!-- Bubble 5: AI Image -->
    <div class="art-bubble ab-5">
        <div class="bubble-shell-wrapper">
            <div class="bubble-shell"></div>
            <svg class="bubble-cracks" viewBox="0 0 100 100">
                <path d="M50 50 L45 36 M50 50 L57 38 M50 50 L40 57 M50 50 L55 64 M50 50 L63 50 M50 50 L37 46" stroke="#A48977" stroke-width="1.5" stroke-linecap="round" fill="none" />
            </svg>
        </div>
        <div class="pop-icon-wrapper">
            <svg viewBox="0 0 100 100">
                <rect x="22" y="22" width="56" height="56" rx="6" stroke="#A48977" stroke-width="1.2" fill="none"/>
                <circle cx="38" cy="38" r="6" stroke="#A48977" stroke-width="1.2" fill="none"/>
                <path d="M22 66 L42 46 L62 66 M54 58 L66 46 L78 58" stroke="#A48977" stroke-width="1.2" fill="none" stroke-linejoin="round"/>
            </svg>
        </div>
    </div>
    
    <!-- Bubble 6: Creative Frame -->
    <div class="art-bubble ab-6">
        <div class="bubble-shell-wrapper">
            <div class="bubble-shell"></div>
            <svg class="bubble-cracks" viewBox="0 0 100 100">
                <path d="M50 50 L43 35 M50 50 L59 39 M50 50 L39 53 M50 50 L57 63 M50 50 L65 51 M50 50 L35 45" stroke="#A48977" stroke-width="1.5" stroke-linecap="round" fill="none" />
            </svg>
        </div>
        <div class="pop-icon-wrapper">
            <svg viewBox="0 0 100 100">
                <rect x="20" y="20" width="60" height="60" stroke="#A48977" stroke-width="1.2" fill="none"/>
                <path d="M10 20 h20 M20 10 v20 M80 10 v20 M70 20 h20 M80 90 v-20 M70 80 h20 M10 80 h20 M20 70 v20" stroke="#A48977" stroke-width="1" fill="none"/>
                <circle cx="50" cy="50" r="8" stroke="#A48977" stroke-width="1" fill="none" stroke-dasharray="2,2"/>
            </svg>
        </div>
    </div>
</div>
"""
st.markdown(bubble_html, unsafe_allow_html=True)

# Brand Logo
logo_html = """
<div class="logo-container">
    <div class="logo-icon"></div>
    <div class="logo-text-block">
        <div class="logo-title">CREATIVE AI STUDIO</div>
        <div class="logo-subtitle">PROMPT TO ART</div>
    </div>
</div>
"""
st.markdown(logo_html, unsafe_allow_html=True)

# Main 2-Column top section to align title/input on the left and keep background globe visible
col_top_left, col_top_right = st.columns([6, 4])

with col_top_left:
    st.markdown('<div class="main-title">AI IMAGE GENERATOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Creative AI Studio  •  Prompt to Art  •  AI Gallery</div>', unsafe_allow_html=True)
    
    # Generation Mode Selector
    st.markdown('<p style="color:#A48977; font-size:14px; font-weight:500; margin-bottom: 8px; font-family: \'Outfit\', sans-serif;">Generation Mode</p>', unsafe_allow_html=True)
    
    col_card1, col_card2, col_card3 = st.columns(3)
    
    with col_card1:
        is_active = (st.session_state.generation_mode == "快速圖片生成")
        active_class = "card-active" if is_active else ""
        st.markdown(f'''
        <div class="mode-card-wrapper">
            <div class="mode-card {active_class}">
                <div class="card-title">🖼️ 快速圖片生成</div>
                <div class="card-desc">快速生成精美圖片</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("Select Fast", key="select_fast"):
            st.session_state.generation_mode = "快速圖片生成"
            st.rerun()
            
    with col_card2:
        is_active = (st.session_state.generation_mode == "精準深層生成")
        active_class = "card-active" if is_active else ""
        st.markdown(f'''
        <div class="mode-card-wrapper">
            <div class="mode-card {active_class}">
                <div class="card-title">✨ 精準深層生成</div>
                <div class="card-desc">更高品質、更細緻</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("Select Precise", key="select_precise"):
            st.session_state.generation_mode = "精準深層生成"
            st.rerun()
            
    with col_card3:
        is_active = (st.session_state.generation_mode == "商業 Logo 生成")
        active_class = "card-active" if is_active else ""
        st.markdown(f'''
        <div class="mode-card-wrapper">
            <div class="mode-card {active_class}">
                <div class="card-title">🏷️ 商業 Logo 生成</div>
                <div class="card-desc">打造品牌專屬 Logo</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("Select Logo", key="select_logo"):
            st.session_state.generation_mode = "商業 Logo 生成"
            st.rerun()
        
    # Dynamic placeholder and input label
    if st.session_state.generation_mode == "商業 Logo 生成":
        placeholder_text = "Enter brand name or logo concept (e.g., AI Trading)..."
        input_label = "Enter brand name or logo concept"
    else:
        placeholder_text = "Describe the image you want to generate..."
        input_label = "Describe the image you want to generate"
        
    # Input Area
    st.markdown(f'<p style="color:#A48977; font-size:14px; font-weight:500; margin-bottom: 8px;">{input_label}</p>', unsafe_allow_html=True)
    prompt = st.text_area(
        label="Prompt input label",
        value=st.session_state.prompt_text,
        placeholder=placeholder_text,
        max_chars=500,
        label_visibility="collapsed"
    )
    
    # Synchronize state when user types manually
    st.session_state.prompt_text = prompt
    
    # Generate Button
    generate_clicked = st.button("GENERATE IMAGE")
    
    # Active Mode display badge
    st.markdown(
        f"""
        <div class="badge-container">
            <span class="badge-label">Active Mode</span>
            <span class="badge-tag">{st.session_state.generation_mode}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_top_right:
    pass


# Horizontal spacing
st.write("---")

# Bottom layout containing output image container and right sidebar cards
col_bot_left, col_bot_right = st.columns([65, 35])

with col_bot_left:
    # Set the header label based on generated_mode
    if st.session_state.generated_mode == "快速圖片生成":
        header_text = "AI 圖片生成結果"
    elif st.session_state.generated_mode == "精準深層生成":
        header_text = "高品質 AI 圖片生成結果"
    elif st.session_state.generated_mode == "商業 Logo 生成":
        header_text = "商業 Logo 生成結果"
    else:
        header_text = "AI 圖片生成結果"
        
    st.markdown(f'<div class="generated-title-text">{header_text}</div>', unsafe_allow_html=True)
    
    # Error rendering
    if st.session_state.error_message:
        st.markdown(f'<div class="alert-card">{st.session_state.error_message}</div>', unsafe_allow_html=True)
        
    # Trigger image generation
    if generate_clicked:
        if not prompt.strip():
            if st.session_state.generation_mode == "商業 Logo 生成":
                st.session_state.error_message = "Warning: Please enter a brand name or logo concept before clicking Generate."
            else:
                st.session_state.error_message = "Warning: Please write a description before clicking Generate."
            st.session_state.generated_image = None
        else:
            # Clear previous outputs
            st.session_state.generated_image = None
            st.session_state.error_message = None
            st.session_state.last_api_prompt = ""
            
            with st.spinner("Generating artwork..."):
                api_prompt = translate_and_enhance_prompt(prompt, st.session_state.generation_mode)
                run_image_generation(api_prompt)
                if st.session_state.generated_image:
                    st.session_state.generated_mode = st.session_state.generation_mode
                    st.session_state.last_api_prompt = api_prompt
                    st.rerun()
                
    # Image Display Box
    if st.session_state.generated_image:
        st.markdown('<div class="gallery-frame">', unsafe_allow_html=True)
        st.image(st.session_state.generated_image, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download button
        buf = io.BytesIO()
        st.session_state.generated_image.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="DOWNLOAD IMAGE",
            data=byte_im,
            file_name="ai_studio_generated.jpg",
            mime="image/jpeg"
        )
        
        # Optimized prompt card
        if st.session_state.last_api_prompt:
            st.markdown(
                f"""
                <div style="background: rgba(234, 231, 218, 0.45); border: 1px solid rgba(164, 137, 119, 0.2); border-radius: 12px; padding: 16px; margin-top: 20px;">
                    <p style="color: #A48977; font-size: 13px; font-weight: 600; margin-bottom: 8px; font-family: 'Outfit', sans-serif; text-transform: uppercase; letter-spacing: 0.5px;">AI Optimized Prompt</p>
                    <p style="color: #3F352E; font-size: 13.5px; line-height: 1.5; margin: 0; font-family: 'JetBrains Mono', monospace; word-break: break-all;">{st.session_state.last_api_prompt}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        # Placeholder image card (using clean SVG icon instead of emoji)
        st.markdown(
            """
            <div class="generated-box">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#A48977" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.6; margin-bottom: 15px;">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                    <circle cx="8.5" cy="8.5" r="1.5" />
                    <polyline points="21 15 16 10 5 21" />
                </svg>
                <div style="font-family: 'Outfit', sans-serif; font-size: 15px; color: #A48977;">Your generated artwork will be framed here</div>
            </div>
            """,
            unsafe_allow_html=True
        )

with col_bot_right:
    # Tips Card
    tips_card_content = """
    <div class="glass-card">
        <div class="section-title">Tips</div>
        <div class="tip-item">
            <span class="tip-bullet">•</span>
            <div><b>Be specific and descriptive:</b> Mention the main subject, environment, materials, color palette, and textures.</div>
        </div>
        <div class="tip-item">
            <span class="tip-bullet">•</span>
            <div><b>Use artistic styles:</b> Add terms like <i>cinematic, anime, oil painting, 3D render, digital art, cyberpunk</i>.</div>
        </div>
        <div class="tip-item">
            <span class="tip-bullet">•</span>
            <div><b>Include lighting details:</b> Specify mood lights e.g. <i>neon glow, golden hour, volumetric lighting, dramatic shadow</i>.</div>
        </div>
        <div class="tip-item">
            <span class="tip-bullet">•</span>
            <div><b>Experiment and have fun:</b> The generation engine excels at text-rendering and complex composition. Try typing text in quotes!</div>
        </div>
    </div>
    """
    st.markdown(tips_card_content, unsafe_allow_html=True)
    
    # Examples Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Examples</div>', unsafe_allow_html=True)
    
    # Dynamic Examples based on mode
    if st.session_state.generation_mode == "快速圖片生成":
        ex_list = [
            ("Futuristic City", "A futuristic cyber city night view, glowing skyscrapers, holographic billboards, flying cars, deep blue colors"),
            ("Astronaut On Mars", "An astronaut standing on the red dusty desert surface of Mars, dramatic lighting, futuristic spacesuit, 8k"),
            ("Cyberpunk Street", "A rainy cyberpunk alleyway, neon signs reflections, a mysterious figure under an umbrella, high detail"),
            ("Fantasy Castle", "A majestic fantasy castle floating on white clouds, golden sun rays piercing through, dreamlike atmosphere"),
            ("Digital Art", "Abstract vibrant digital art, swirling neural networks, glowing tech particles, high contrast design")
        ]
    elif st.session_state.generation_mode == "精準深層生成":
        ex_list = [
            ("Luxury Watch", "A premium luxury smartwatch lying on black volcanic sand, water droplets on the screen, cinematic lighting, product commercial photo"),
            ("Cyberpunk Alley", "A narrow Tokyo alleyway at night after rain, hyper-detailed cyberpunk storefronts, neon signs reflecting in puddles, steam rising from vents"),
            ("Sci-Fi Robot", "A futuristic combat android deactivated in a dusty abandoned workshop, intricate wiring exposed, cinematic volumetric lighting, highly detailed textures"),
            ("Fantasy Landscape", "A majestic ancient tree with glowing blue leaves at the edge of a crystal clear lake under a starry cosmic sky, dreamlike atmosphere, masterpiece"),
            ("Premium Perfume", "A minimalist glass perfume bottle standing on a smooth marble slab, dramatic shadows, warm cinematic lighting, professional composition")
        ]
    else: # 商業 Logo 生成
        ex_list = [
            ("AI Trading", "AI Trading"),
            ("Cyber Bistro", "Cyber Bistro"),
            ("Organic Food", "Organic Food"),
            ("Infinity Cloud", "Infinity Cloud"),
            ("Pixel Studio", "Pixel Studio")
        ]
    
    for label, text in ex_list:
        if st.button(label, key=f"btn_{st.session_state.generation_mode}_{label.lower().replace(' ', '_')}"):
            set_prompt(text)
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
