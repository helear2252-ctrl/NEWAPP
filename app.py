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

/* Custom styling for Streamlit Radio Buttons to look like premium segmented tabs */
div[data-testid="stRadio"] > div {{
    gap: 12px;
}}
div[data-testid="stRadio"] label {{
    background: rgba(234, 231, 218, 0.5) !important;
    border: 1px solid rgba(164, 137, 119, 0.15) !important;
    padding: 8px 16px !important;
    border-radius: 10px !important;
    color: #3F352E !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}}
div[data-testid="stRadio"] label:hover {{
    border-color: rgba(164, 137, 119, 0.4) !important;
    background: rgba(234, 231, 218, 0.8) !important;
}}
div[data-testid="stRadio"] label[data-checked="true"] {{
    background: #A48977 !important;
    border-color: #A48977 !important;
    color: #F7F4ED !important;
}}
div[data-testid="stRadio"] label span[data-baseweb="radio"],
div[data-testid="stRadio"] label div[role="radio"] {{
    display: none !important;
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
"""
st.markdown(background_html, unsafe_allow_html=True)

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
    st.markdown('<p style="color:#A48977; font-size:14px; font-weight:500; margin-bottom: 8px;">Generation Mode</p>', unsafe_allow_html=True)
    generation_mode = st.radio(
        label="Generation Mode Selector",
        options=["快速圖片生成", "精準深層生成", "商業 Logo 生成"],
        index=["快速圖片生成", "精準深層生成", "商業 Logo 生成"].index(st.session_state.generation_mode),
        horizontal=True,
        label_visibility="collapsed"
    )
    if generation_mode != st.session_state.generation_mode:
        st.session_state.generation_mode = generation_mode
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
