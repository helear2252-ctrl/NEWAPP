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
/* Reference image visual-only overrides: keep inside css_style */
.stApp {{
    background:
        radial-gradient(circle at 50% 4%, rgba(255, 255, 255, 0.86), rgba(255, 255, 255, 0) 34%),
        radial-gradient(circle at 12% 24%, rgba(255, 246, 232, 0.78), rgba(255, 246, 232, 0) 32%),
        radial-gradient(circle at 86% 18%, rgba(201, 167, 126, 0.22), rgba(201, 167, 126, 0) 36%),
        linear-gradient(125deg, #FAF7EF 0%, #F8F1E7 48%, #EFE2D0 100%) !important;
    color: #6E4E3D !important;
}}
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    z-index: -2;
    pointer-events: none;
    background-image:
        radial-gradient(circle, rgba(255, 255, 255, 0.95) 0 1px, transparent 2px),
        radial-gradient(circle, rgba(201, 167, 126, 0.34) 0 1px, transparent 2px),
        radial-gradient(circle, rgba(255, 244, 226, 0.72) 0 2px, transparent 4px);
    background-size: 42px 42px, 76px 76px, 128px 128px;
    background-position: 8px 10px, 28px 19px, 42px 34px;
    opacity: 0.52;
    filter: blur(0.25px);
}}
.bg-layer-1 {{
    background:
        radial-gradient(circle at 48% 0%, rgba(255, 255, 255, 0.74), rgba(255, 255, 255, 0) 30%),
        linear-gradient(125deg, #FAF7EF 0%, #F8F1E7 44%, #EFE2D0 100%) !important;
    z-index: -6;
}}
.bg-layer-2 {{ z-index: -5; }}
.bg-layer-3 {{ z-index: -4; }}
.halo-1 {{
    background: radial-gradient(circle, rgba(255, 255, 255, 0.72) 0%, rgba(248, 231, 207, 0.42) 42%, rgba(248, 231, 207, 0) 72%);
    filter: blur(5px);
}}
.halo-2 {{
    background: radial-gradient(circle, rgba(201, 167, 126, 0.18) 0%, rgba(255, 255, 255, 0.36) 32%, rgba(201, 167, 126, 0) 74%);
    filter: blur(6px);
}}
.logo-title,
.main-title,
.generated-title-text,
.section-title,
.card-title {{
    color: #6E4E3D !important;
}}
.logo-subtitle,
.main-subtitle,
.badge-label,
.card-desc,
div[data-testid="stTextArea"] label p {{
    color: #9A806D !important;
}}
.main-title {{
    text-shadow: 0 8px 30px rgba(110, 78, 61, 0.10), 0 1px 0 rgba(255, 255, 255, 0.75);
}}
.glass-card,
.mode-card,
.generated-box,
.alert-card {{
    background: rgba(255, 250, 242, 0.72) !important;
    border-color: rgba(201, 167, 126, 0.28) !important;
    box-shadow: 0 18px 45px rgba(110, 78, 61, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.82) !important;
    backdrop-filter: blur(18px) saturate(1.08) !important;
    -webkit-backdrop-filter: blur(18px) saturate(1.08) !important;
}}
.mode-card.card-active {{
    background: linear-gradient(135deg, rgba(255, 252, 246, 0.88), rgba(201, 167, 126, 0.18)) !important;
    border-color: rgba(185, 143, 101, 0.58) !important;
}}
div[data-testid="stTextArea"] textarea {{
    background: rgba(255, 250, 242, 0.78) !important;
    border: 1px solid rgba(201, 167, 126, 0.34) !important;
    color: #6E4E3D !important;
    box-shadow: 0 18px 45px rgba(110, 78, 61, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.95) !important;
}}
div.stButton > button {{
    background: linear-gradient(135deg, #C9A77E 0%, #A97852 100%) !important;
    color: #FFF8EF !important;
    box-shadow: 0 18px 38px rgba(169, 120, 82, 0.22), inset 0 1px 0 rgba(255, 255, 255, 0.35) !important;
}}
.floating-gallery-container {{
    z-index: -2 !important;
    overflow: visible;
}}
.polaroid-card {{
    background: rgba(255, 255, 255, 0.88) !important;
    border-color: rgba(255, 255, 255, 0.82) !important;
    opacity: 0.72 !important;
    box-shadow: 0 24px 48px rgba(110, 78, 61, 0.16), inset 0 1px 0 rgba(255, 255, 255, 0.96) !important;
    filter: blur(0.25px) saturate(0.92);
}}
.polaroid-card .art-placeholder {{
    background:
        radial-gradient(circle at 30% 22%, rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0) 24%),
        linear-gradient(135deg, rgba(239, 226, 208, 0.86), rgba(201, 167, 126, 0.28)) !important;
}}
.polaroid-card .art-caption {{
    color: #8F7564;
    font-style: italic;
}}
.bubble-container {{
    z-index: -3;
    overflow: visible;
}}
.bubble-shell {{
    border: 1px solid rgba(255, 255, 255, 0.78);
    background:
        radial-gradient(circle at 28% 22%, rgba(255, 255, 255, 0.92) 0 4%, rgba(255, 255, 255, 0.18) 11%, transparent 23%),
        radial-gradient(circle at 68% 72%, rgba(201, 167, 126, 0.19), rgba(255, 255, 255, 0) 46%),
        radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0.04) 60%, rgba(185, 143, 101, 0.16) 100%);
    box-shadow:
        inset 8px 10px 18px rgba(255, 255, 255, 0.34),
        inset -12px -18px 28px rgba(185, 143, 101, 0.08),
        0 0 24px rgba(255, 255, 255, 0.62),
        0 18px 42px rgba(185, 143, 101, 0.10);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}}
.pop-icon-wrapper {{
    background: radial-gradient(circle, rgba(255, 250, 242, 0.36), rgba(201, 167, 126, 0.10));
    border-radius: 50%;
    filter: blur(0.35px) saturate(0.9);
}}
div[data-testid="stTextArea"],
div[data-testid="stTextInput"],
div[data-testid="stSelectbox"],
div.stButton,
.mode-card-wrapper,
.glass-card,
.gallery-frame,
.generated-box,
.alert-card {{
    position: relative;
    z-index: 20 !important;
}}
/* Full homepage composition pass: layout-like styling without touching generation logic */
.main .block-container {{
    max-width: 1220px !important;
    padding-top: 30px !important;
    padding-bottom: 64px !important;
}}
.champagne-particles {{
    position: fixed;
    inset: 0;
    z-index: -5;
    pointer-events: none;
    opacity: .68;
    background-image:
        radial-gradient(circle, rgba(255,255,255,.96) 0 1px, transparent 2px),
        radial-gradient(circle, rgba(201,167,126,.44) 0 1px, transparent 2px),
        radial-gradient(circle, rgba(255,242,224,.86) 0 2px, transparent 4px);
    background-size: 38px 38px, 73px 73px, 128px 128px;
    background-position: 8px 14px, 28px 20px, 42px 36px;
    filter: blur(.25px);
    animation: particle-drift 24s linear infinite;
}}
@keyframes particle-drift {{
    from {{ transform: translateY(0); }}
    to {{ transform: translateY(-38px); }}
}}
.background-bubble {{
    position: fixed;
    border-radius: 50%;
    z-index: -4;
    pointer-events: none;
    background:
        radial-gradient(circle at 28% 22%, rgba(255,255,255,.95) 0 5%, rgba(255,255,255,.25) 13%, transparent 25%),
        radial-gradient(circle at 68% 72%, rgba(201,167,126,.18), rgba(255,255,255,0) 48%),
        radial-gradient(circle at 50% 50%, rgba(255,255,255,.18), rgba(255,255,255,.04) 62%, rgba(185,143,101,.16) 100%);
    border: 1px solid rgba(255,255,255,.72);
    box-shadow: inset 10px 12px 22px rgba(255,255,255,.38), inset -14px -18px 30px rgba(185,143,101,.08), 0 0 30px rgba(255,255,255,.58);
    opacity: var(--op);
    filter: blur(var(--blur));
    animation: soft-orbit var(--speed) ease-in-out infinite;
}}
.bb-1 {{ width: 178px; height: 178px; left: 3vw; top: 16vh; --op: .72; --blur: 0px; --speed: 18s; }}
.bb-2 {{ width: 96px; height: 96px; left: 13vw; top: 34vh; --op: .52; --blur: .8px; --speed: 21s; }}
.bb-3 {{ width: 42px; height: 42px; left: 38vw; top: 9vh; --op: .42; --blur: 1px; --speed: 16s; }}
.bb-4 {{ width: 260px; height: 260px; left: 58vw; top: 17vh; --op: .32; --blur: 1.5px; --speed: 26s; }}
.bb-5 {{ width: 84px; height: 84px; right: 18vw; top: 43vh; --op: .46; --blur: .7px; --speed: 17s; }}
.bb-6 {{ width: 210px; height: 210px; left: 1vw; bottom: 4vh; --op: .42; --blur: .6px; --speed: 23s; }}
.bb-7 {{ width: 54px; height: 54px; right: 7vw; top: 3vh; --op: .46; --blur: .9px; --speed: 19s; }}
@keyframes soft-orbit {{
    0%, 100% {{ transform: translate3d(0, 0, 0) scale(1); }}
    45% {{ transform: translate3d(16px, -20px, 0) scale(1.035); }}
    72% {{ transform: translate3d(-8px, 10px, 0) scale(.99); }}
}}
.hero-panel {{
    position: relative;
    z-index: 24;
    text-align: center;
    padding-top: 12px;
}}
.main-title {{
    text-align: center;
    max-width: 780px;
    margin: 46px auto 8px !important;
    font-size: clamp(52px, 6.7vw, 84px) !important;
    line-height: .92 !important;
}}
.main-subtitle {{
    text-align: center;
    letter-spacing: 1.75px !important;
}}
.mode-label {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 24px;
    margin: 10px auto 16px;
    color: #8F7564;
    font-size: 16px;
    font-weight: 700;
}}
.mode-label::before,
.mode-label::after {{
    content: "";
    width: 112px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,167,126,.46), transparent);
}}
.prompt-heading {{
    text-align: center;
    margin: 18px auto 12px;
}}
.prompt-heading-title {{
    color: #7B5A46;
    font-size: 18px;
    font-weight: 700;
}}
.prompt-heading-subtitle {{
    color: #9A806D;
    font-size: 13px;
    margin-top: 4px;
}}
div[data-testid="stTextArea"] {{
    max-width: 760px;
    margin: 0 auto !important;
}}
.photo-scene {{
    width: 100%;
    height: 100%;
    border-radius: 4px;
    position: relative;
    overflow: hidden;
    background: var(--scene-bg);
}}
.photo-scene::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 28% 18%, rgba(255,255,255,.78), transparent 28%);
}}
.scene-castle {{ --scene-bg: linear-gradient(145deg, #efe0c8 0%, #b9a68c 48%, #f8f1e7 100%); }}
.scene-corgi {{ --scene-bg: linear-gradient(145deg, #f5d9bd 0%, #d89e6f 45%, #f8f1e7 100%); }}
.scene-city {{ --scene-bg: linear-gradient(145deg, #40314b 0%, #946a83 45%, #f4c794 100%); }}
.scene-portrait {{ --scene-bg: linear-gradient(145deg, #ead2bd 0%, #c49275 50%, #fff6ea 100%); }}
.scene-logo {{ --scene-bg: linear-gradient(145deg, #f6eadb 0%, #c9a77e 54%, #fffaf2 100%); }}
.scene-water {{ --scene-bg: linear-gradient(145deg, #e9d7c2 0%, #b9c5bd 48%, #fffaf2 100%); }}
.photo-mark {{
    position: absolute;
    inset: 18%;
    border: 1px solid rgba(110,78,61,.38);
    border-radius: 50%;
    box-shadow: inset 0 0 22px rgba(255,255,255,.35);
}}
.photo-mark::after {{
    content: "";
    position: absolute;
    left: 20%;
    right: 20%;
    bottom: 18%;
    height: 28%;
    border-radius: 50% 50% 0 0;
    background: rgba(110,78,61,.18);
}}
.pc-1 {{ top: 4%; right: 25%; width: 162px !important; filter: blur(.1px); }}
.pc-2 {{ top: 23%; right: 3%; width: 146px !important; filter: blur(.25px); }}
.pc-3 {{ top: 48%; right: 7%; width: 170px !important; filter: blur(.1px); }}
.pc-4 {{ top: 70%; right: 24%; width: 154px !important; filter: blur(.45px); }}
.pc-5 {{ top: 9%; right: 1%; width: 104px !important; opacity: .50 !important; filter: blur(1.1px); }}
.pc-6 {{ top: 76%; right: 2%; width: 110px !important; opacity: .42 !important; filter: blur(1.2px); }}
.bubble-art-thumb {{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    opacity: .72;
    background: var(--bubble-art);
    box-shadow: inset 0 0 20px rgba(255,255,255,.45);
}}
.thumb-1 {{ --bubble-art: linear-gradient(135deg, #f2d9ba, #b98f65 45%, #fff6ea); }}
.thumb-2 {{ --bubble-art: linear-gradient(135deg, #f7e3c8, #c9996f 48%, #fdf7ee); }}
.thumb-3 {{ --bubble-art: linear-gradient(135deg, #efd6bf, #9f7d6a 46%, #fff8f0); }}
.thumb-4 {{ --bubble-art: linear-gradient(135deg, #f5e5d2, #c9a77e 52%, #fffaf2); }}
.thumb-5 {{ --bubble-art: linear-gradient(135deg, #d7c1aa, #71506a 45%, #f2c58f); }}
.thumb-6 {{ --bubble-art: linear-gradient(135deg, #fff1dc, #c49275 48%, #fdf7ee); }}
.bubble-label {{
    position: fixed;
    left: 52px;
    top: 53vh;
    z-index: -1;
    color: rgba(110,78,61,.46);
    border: 1px solid rgba(185,143,101,.22);
    border-radius: 10px;
    padding: 12px 14px;
    font-size: 14px;
    line-height: 1.2;
    text-align: center;
    background: rgba(255,250,242,.20);
}}
.flow-rail {{
    position: fixed;
    right: 17%;
    top: 50%;
    z-index: -1;
    transform: translateY(-50%);
    color: rgba(110,78,61,.34);
    font-size: 12px;
    line-height: 2.2;
    text-align: center;
}}
.flow-rail span {{ display: block; }}
div[data-testid="stTextArea"],
div[data-testid="stTextInput"],
div[data-testid="stSelectbox"],
div.stButton,
.mode-card-wrapper,
.glass-card,
.gallery-frame,
.generated-box,
.alert-card {{
    z-index: 40 !important;
}}
@media (max-width: 900px) {{
    .floating-gallery-container {{ opacity: .26; width: 100%; }}
    .pc-2, .pc-3, .pc-4, .pc-5, .pc-6, .flow-rail {{ display: none; }}
    .pc-1 {{ right: -24px; top: 8%; width: 118px !important; }}
    .main-title {{ font-size: 48px !important; margin-top: 20px !important; }}
    .mode-label::before, .mode-label::after {{ width: 44px; }}
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

# Core Inference API Call functions

def run_nvidia_generation(prompt: str):
    raw_token = os.getenv("HF_TOKEN")
    if not raw_token:
        st.session_state.error_message = "🔑 API Token is missing! Please configure the `HF_TOKEN` environment variable or Streamlit Secrets."
        return

    hf_token = raw_token.strip().strip("'\"").replace("“", "").replace("”", "").replace("‘", "").replace("’", "")
    hf_token = "".join(c for c in hf_token if ord(c) < 128)

    api_urls = [
        "https://router.huggingface.co/hf-inference/models/nvidia/Cosmos3-Super-Text2Image",
        "https://api-inference.huggingface.co/models/nvidia/Cosmos3-Super-Text2Image",
    ]
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": prompt}

    max_retries = 3
    retry_delay = 5

    for api_url in api_urls:
        for attempt in range(max_retries):
            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=60)

                if response.status_code == 200:
                    try:
                        image = Image.open(io.BytesIO(response.content))
                        image.load()
                        st.session_state.generated_image = image
                        st.session_state.error_message = None
                        return
                    except Exception as img_err:
                        st.session_state.error_message = f"🖼️ NVIDIA image loading error: {str(img_err)}"
                        return

                if response.status_code == 503:
                    try:
                        error_json = response.json()
                        wait_time = float(error_json.get("estimated_time", retry_delay))
                    except Exception:
                        wait_time = retry_delay

                    if attempt < max_retries - 1:
                        with st.spinner(f"⏳ NVIDIA Cosmos model is initializing (attempt {attempt+1}/{max_retries}). Waiting {int(wait_time)}s..."):
                            time.sleep(wait_time)
                        continue
                    break

                if response.status_code == 401:
                    st.session_state.error_message = "🔒 Authentication Failed: The provided `HF_TOKEN` is invalid or does not have permissions. Please check your credentials."
                    return

                try:
                    error_json = response.json()
                    error_msg = error_json.get("error", "")
                except Exception:
                    error_msg = ""
                st.session_state.error_message = f"🚨 NVIDIA API Error: {error_msg if error_msg else f'HTTP status {response.status_code}'}"
                break

            except requests.exceptions.RequestException as err:
                if isinstance(err, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)) and attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                break

        if st.session_state.generated_image:
            return

    if not st.session_state.error_message:
        st.session_state.error_message = "⚠️ NVIDIA 免費生成模型目前忙碌或暫時無法使用，請稍後再試。"


def run_flux_generation(prompt: str):
    raw_token = os.getenv("HF_TOKEN")
    if not raw_token:
        st.session_state.error_message = "🔑 API Token is missing! Please configure the `HF_TOKEN` environment variable or Streamlit Secrets."
        return

    hf_token = raw_token.strip().strip("'\"").replace("“", "").replace("”", "").replace("‘", "").replace("’", "")
    hf_token = "".join(c for c in hf_token if ord(c) < 128)

    api_urls = [
        "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell",
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
                        image = Image.open(io.BytesIO(response.content))
                        image.load()
                        st.session_state.generated_image = image
                        st.session_state.error_message = None
                        return
                    except Exception as img_err:
                        st.session_state.error_message = f"🖼️ Image loading error: Received bytes could not be decoded. Details: {str(img_err)}"
                        return

                if response.status_code == 503:
                    try:
                        error_json = response.json()
                        wait_time = float(error_json.get("estimated_time", retry_delay))
                    except Exception:
                        wait_time = retry_delay

                    if attempt < max_retries - 1:
                        with st.spinner(f"⏳ AI system is initializing (attempt {attempt+1}/{max_retries}). Waiting {int(wait_time)}s..."):
                            time.sleep(wait_time)
                        continue
                    break

                if response.status_code == 429:
                    st.session_state.error_message = "⚠️ FLUX 額度已耗盡，請改用「快速圖片生成」模式，或等待下個月額度重置。"
                    return

                if response.status_code == 401:
                    st.session_state.error_message = "🔒 Authentication Failed: The provided `HF_TOKEN` is invalid or does not have permissions. Please check your credentials."
                    return

                try:
                    error_json = response.json()
                    error_msg = error_json.get("error", "")
                except Exception:
                    error_msg = ""

                if "rate limit" in error_msg.lower() or "limit" in error_msg.lower() or "quota" in error_msg.lower():
                    st.session_state.error_message = "⚠️ FLUX 額度已耗盡，請改用「快速圖片生成」模式，或等待下個月額度重置。"
                    return

                st.session_state.error_message = f"🚨 API Error: {error_msg if error_msg else f'HTTP status {response.status_code}'}"
                break

            except requests.exceptions.RequestException as e:
                if isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.Timeout)) and attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                st.session_state.error_message = f"🔌 Network connection failure: Details: {str(e)}"
                return

        if st.session_state.generated_image:
            return

    if not st.session_state.error_message:
        st.session_state.error_message = "❌ Failed to connect to the generation server. Please verify your internet connection."


def run_image_generation(prompt: str):
    generation_mode = st.session_state.get("generation_mode", "快速圖片生成")

    if generation_mode == "快速圖片生成":
        run_flux_generation(prompt)
    elif generation_mode in ("精準深層生成", "商業 Logo 生成"):
        run_flux_generation(prompt)
    else:
        st.session_state.error_message = f"⚠️ Unknown generation mode: {generation_mode}"

# --- PAGE LAYOUT SETUP ---

# Background三層結構與浮動線稿插畫 SVG 注入
background_html = """
<div class="bg-layer-1"></div>
<div class="bg-layer-2">
    <div class="halo-1"></div>
    <div class="halo-2"></div>
    <div class="champagne-particles"></div>
    <div class="background-bubble bb-1"></div>
    <div class="background-bubble bb-2"></div>
    <div class="background-bubble bb-3"></div>
    <div class="background-bubble bb-4"></div>
    <div class="background-bubble bb-5"></div>
    <div class="background-bubble bb-6"></div>
    <div class="background-bubble bb-7"></div>
    <div class="bubble-label">Bubble<br>to<br>Art</div>
    <div class="flow-rail">
        <span>Prompt</span>
        <span>↓</span>
        <span>AI</span>
        <span>↓</span>
        <span>Art</span>
        <span>↓</span>
        <span>Gallery</span>
    </div>
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
            <div class="photo-scene scene-castle"><div class="photo-mark"></div></div>
        </div>
        <div class="art-caption">Fantasy Castle</div>
    </div>
    <!-- Polaroid 2: Cute Animal -->
    <div class="polaroid-card pc-2">
        <div class="art-placeholder">
            <div class="photo-scene scene-corgi"><div class="photo-mark"></div></div>
        </div>
        <div class="art-caption">Cute Animal</div>
    </div>
    <!-- Polaroid 3: Cyber City -->
    <div class="polaroid-card pc-3">
        <div class="art-placeholder">
            <div class="photo-scene scene-city"><div class="photo-mark"></div></div>
        </div>
        <div class="art-caption">Cyber City</div>
    </div>
    <!-- Polaroid 4: AI Portrait -->
    <div class="polaroid-card pc-4">
        <div class="art-placeholder">
            <div class="photo-scene scene-portrait"><div class="photo-mark"></div></div>
        </div>
        <div class="art-caption">AI Portrait</div>
    </div>
    <!-- Polaroid 5: Logo Design -->
    <div class="polaroid-card pc-5">
        <div class="art-placeholder">
            <div class="photo-scene scene-logo"><div class="photo-mark"></div></div>
        </div>
        <div class="art-caption">Logo Design</div>
    </div>
    <!-- Polaroid 6: Watercolor Art -->
    <div class="polaroid-card pc-6">
        <div class="art-placeholder">
            <div class="photo-scene scene-water"><div class="photo-mark"></div></div>
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
            <div class="bubble-art-thumb thumb-1"></div>
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
            <div class="bubble-art-thumb thumb-2"></div>
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
            <div class="bubble-art-thumb thumb-3"></div>
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
            <div class="bubble-art-thumb thumb-4"></div>
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
            <div class="bubble-art-thumb thumb-5"></div>
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
            <div class="bubble-art-thumb thumb-6"></div>
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

# Centered hero section; decorative background remains behind the content
col_top_left_pad, col_top_left, col_top_right = st.columns([1, 8, 1])

with col_top_left:
    st.markdown('<div class="hero-panel"><div class="main-title">AI IMAGE<br>GENERATOR</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Creative AI Studio  •  Prompt to Art  •  AI Gallery</div>', unsafe_allow_html=True)
    
    # Generation Mode Selector
    st.markdown('<div class="mode-label">選擇生成模式</div>', unsafe_allow_html=True)
    
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
    st.markdown(
        f'''
        <div class="prompt-heading">
            <div class="prompt-heading-title">{input_label}</div>
            <div class="prompt-heading-subtitle">越詳細的描述，越能生成符合想像的圖片</div>
        </div>
        ''',
        unsafe_allow_html=True
    )
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
