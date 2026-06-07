import streamlit as st
import os
import io
import base64
import requests
import time
from PIL import Image
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI STUDIO - CREATE THE FUTURE",
    page_icon="🔮",
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
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Space+Grotesk:wght@400;500;700&display=swap');

/* Main background & page container */
.stApp {{
    background: linear-gradient(rgba(3, 10, 22, 0.7), rgba(3, 10, 22, 0.85)), url("data:image/jpeg;base64,{base64_bg}") no-repeat center center fixed;
    background-size: cover;
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #E2F1FF;
}}

/* Hide Streamlit elements */
header, footer, [data-testid="stHeader"] {{
    visibility: hidden !important;
    height: 0 !important;
}}

/* Custom Typography */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Space Grotesk', sans-serif !important;
    color: #FFFFFF !important;
}}

/* Glassmorphism card utility */
.glass-card {{
    background: rgba(10, 25, 50, 0.35);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(0, 191, 255, 0.12);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
    margin-bottom: 24px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}
.glass-card:hover {{
    border-color: rgba(0, 191, 255, 0.25);
    box-shadow: 0 12px 40px 0 rgba(0, 191, 255, 0.08);
}}

/* Logo and brand styles */
.logo-container {{
    display: flex;
    align-items: center;
    margin-bottom: 25px;
}}
.logo-icon {{
    background: linear-gradient(135deg, #0052D4, #4364F7, #6FB1FC);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    margin-right: 14px;
    box-shadow: 0 0 15px rgba(67, 100, 247, 0.7);
    display: inline-block;
}}
.logo-text-block {{
    display: flex;
    flex-direction: column;
}}
.logo-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 20px;
    letter-spacing: 1.5px;
    color: #FFFFFF;
    line-height: 1.1;
}}
.logo-subtitle {{
    font-size: 9px;
    color: #00BFFF;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    font-weight: 600;
}}

/* Main titles */
.main-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 52px;
    font-weight: 800;
    background: linear-gradient(90deg, #00BFFF, #8AE5FF, #FFFFFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
    letter-spacing: -1px;
}}
.main-subtitle {{
    font-size: 16px;
    color: #8A99AD;
    margin-bottom: 35px;
    font-weight: 300;
}}

/* Custom placeholder / box for generated image */
.generated-box {{
    border: 1px dashed rgba(0, 191, 255, 0.25);
    border-radius: 12px;
    background: rgba(5, 12, 28, 0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    color: #8A99AD;
    padding: 24px;
    text-align: center;
}}
.placeholder-icon {{
    font-size: 48px;
    margin-bottom: 15px;
    opacity: 0.6;
}}
.generated-title-text {{
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 20px;
    color: #FFFFFF;
    font-family: 'Space Grotesk', sans-serif;
}}

/* Custom styling for standard Streamlit Text Area */
div[data-testid="stTextArea"] textarea {{
    background: rgba(5, 12, 28, 0.65) !important;
    border: 1px solid rgba(0, 191, 255, 0.2) !important;
    border-radius: 12px !important;
    color: #E2F1FF !important;
    font-size: 15px !important;
    padding: 16px !important;
    font-family: 'Outfit', sans-serif !important;
    transition: all 0.3s ease !important;
}}
div[data-testid="stTextArea"] textarea:focus {{
    border-color: #00BFFF !important;
    box-shadow: 0 0 15px rgba(0, 191, 255, 0.25) !important;
}}
div[data-testid="stTextArea"] label p {{
    color: #8A99AD !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    margin-bottom: 6px !important;
}}

/* Custom styling for streamlit buttons */
div.stButton > button {{
    background: linear-gradient(135deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 14px 28px !important;
    width: 100% !important;
    box-shadow: 0 4px 18px rgba(67, 100, 247, 0.35) !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    cursor: pointer !important;
    letter-spacing: 0.8px !important;
}}
div.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 22px rgba(67, 100, 247, 0.55), 0 0 15px rgba(0, 191, 255, 0.4) !important;
    color: #FFFFFF !important;
}}
div.stButton > button:active {{
    transform: translateY(1px) !important;
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
    color: #8A99AD;
}}
.badge-tag {{
    background: rgba(10, 25, 50, 0.7);
    border: 1px solid rgba(0, 191, 255, 0.2);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 11px;
    font-family: 'Space Grotesk', sans-serif;
    color: #8AE5FF;
}}

/* Tip list items */
.tip-item {{
    display: flex;
    align-items: flex-start;
    margin-bottom: 12px;
    font-size: 13.5px;
    color: #C0D1EB;
    line-height: 1.4;
}}
.tip-bullet {{
    color: #00BFFF;
    margin-right: 10px;
    font-size: 14px;
}}

/* Styled header for section cards */
.section-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 16px;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(0, 191, 255, 0.15);
    padding-bottom: 8px;
}}

/* Styled Alert elements */
.alert-card {{
    background: rgba(220, 53, 69, 0.1);
    border: 1px solid rgba(220, 53, 69, 0.3);
    border-radius: 12px;
    padding: 16px;
    color: #F8D7DA;
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

# Example selection helper
def set_prompt(text):
    st.session_state.prompt_text = text
    st.session_state.error_message = None

# Core Inference API Call function
def run_image_generation(prompt: str):
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        st.session_state.error_message = "🔑 API Token is missing! Please configure the `HF_TOKEN` environment variable or Streamlit Secrets."
        return
    
    api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": prompt}
    
    max_retries = 3
    retry_delay = 6
    
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
                    with st.spinner(f"⏳ Hugging Face model is initializing (attempt {attempt+1}/{max_retries}). Waiting {int(wait_time)}s..."):
                        time.sleep(wait_time)
                    continue
                else:
                    st.session_state.error_message = f"⚡ Hugging Face model loading timed out. Please try again in a moment. (HTTP 503)"
                    return
                    
            elif response.status_code == 401:
                st.session_state.error_message = "🔒 Authentication Failed: The provided `HF_TOKEN` is invalid or does not have permissions. Please check your credentials."
                return
            else:
                try:
                    error_msg = response.json().get("error", f"HTTP status {response.status_code}")
                except Exception:
                    error_msg = f"HTTP {response.status_code} error response"
                st.session_state.error_message = f"🚨 API Error: {error_msg}"
                return
                
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            st.session_state.error_message = "🌐 Network Timeout: The request took too long. Please check your internet connection and try again."
            return
        except requests.exceptions.RequestException as e:
            st.session_state.error_message = f"🔌 Network connection failure: Could not reach Hugging Face API. Details: {str(e)}"
            return
            
    st.session_state.error_message = "❌ Failed to generate image after multiple attempts due to API unavailability."


# --- PAGE LAYOUT SETUP ---

# Brand Logo
logo_html = """
<div class="logo-container">
    <div class="logo-icon"></div>
    <div class="logo-text-block">
        <div class="logo-title">AI STUDIO</div>
        <div class="logo-subtitle">CREATE THE FUTURE</div>
    </div>
</div>
"""
st.markdown(logo_html, unsafe_allow_html=True)

# Main 2-Column top section to align title/input on the left and keep background globe visible
col_top_left, col_top_right = st.columns([6, 4])

with col_top_left:
    st.markdown('<div class="main-title">AI IMAGE GENERATOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Turn your imagination into reality with AI</div>', unsafe_allow_html=True)
    
    # Input Area
    st.markdown('<p style="color:#8A99AD; font-size:14px; font-weight:500; margin-bottom: 8px;">Describe the image you want to generate</p>', unsafe_allow_html=True)
    prompt = st.text_area(
        label="Prompt input label",
        value=st.session_state.prompt_text,
        placeholder="Describe the image you want to generate...",
        max_chars=500,
        label_visibility="collapsed"
    )
    
    # Synchronize state when user types manually
    st.session_state.prompt_text = prompt
    
    # Generate Button
    generate_clicked = st.button("✨ GENERATE IMAGE")
    
    # Powered by labels
    st.markdown(
        """
        <div class="badge-container">
            <span class="badge-label">Powered by</span>
            <span class="badge-tag">FLUX.1-schnell</span>
            <span class="badge-tag">🤗 Hugging Face</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_top_right:
    # Intentionally empty to showcase the beautiful digital earth background globe
    pass


# Horizontal spacing
st.write("---")

# Bottom layout containing output image container and right sidebar cards
col_bot_left, col_bot_right = st.columns([65, 35])

with col_bot_left:
    st.markdown('<div class="generated-title-text">Generated Image</div>', unsafe_allow_html=True)
    
    # Error rendering
    if st.session_state.error_message:
        st.markdown(f'<div class="alert-card">{st.session_state.error_message}</div>', unsafe_allow_html=True)
        
    # Trigger image generation
    if generate_clicked:
        if not prompt.strip():
            st.session_state.error_message = "⚠️ Please write a description before clicking Generate!"
            st.session_state.generated_image = None
        else:
            with st.spinner("🧠 Generating your masterpiece..."):
                run_image_generation(prompt)
                
    # Image Display Box
    if st.session_state.generated_image:
        st.image(st.session_state.generated_image, use_column_width=True)
        
        # Download button
        buf = io.BytesIO()
        st.session_state.generated_image.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="📥 DOWNLOAD IMAGE",
            data=byte_im,
            file_name="ai_studio_generated.jpg",
            mime="image/jpeg"
        )
    else:
        # Placeholder image card
        st.markdown(
            """
            <div class="generated-box">
                <div class="placeholder-icon">🎨</div>
                <div>Your generated image will appear here</div>
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
            <span class="tip-bullet">✦</span>
            <div><b>Be specific and descriptive:</b> Mention the main subject, environment, materials, color palette, and textures.</div>
        </div>
        <div class="tip-item">
            <span class="tip-bullet">✦</span>
            <div><b>Use artistic styles:</b> Add terms like <i>cinematic, anime, oil painting, 3D render, digital art, cyberpunk</i>.</div>
        </div>
        <div class="tip-item">
            <span class="tip-bullet">✦</span>
            <div><b>Include lighting details:</b> Specify mood lights e.g. <i>neon glow, golden hour, volumetric lighting, dramatic shadow</i>.</div>
        </div>
        <div class="tip-item">
            <span class="tip-bullet">✦</span>
            <div><b>Experiment and have fun:</b> Flux.1-schnell excels at text-rendering and complex composition. Try typing text in quotes!</div>
        </div>
    </div>
    """
    st.markdown(tips_card_content, unsafe_allow_html=True)
    
    # Examples Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Examples</div>', unsafe_allow_html=True)
    
    # Example buttons
    ex_list = [
        ("Futuristic City", "A futuristic cyber city night view, glowing skyscrapers, holographic billboards, flying cars, deep blue colors"),
        ("Astronaut On Mars", "An astronaut standing on the red dusty desert surface of Mars, dramatic lighting, futuristic spacesuit, 8k"),
        ("Cyberpunk Street", "A rainy cyberpunk alleyway, neon signs reflections, a mysterious figure under an umbrella, high detail"),
        ("Fantasy Castle", "A majestic fantasy castle floating on white clouds, golden sun rays piercing through, dreamlike atmosphere"),
        ("Digital Art", "Abstract vibrant digital art, swirling neural networks, glowing tech particles, high contrast design")
    ]
    
    for label, text in ex_list:
        if st.button(label, key=f"btn_{label.lower().replace(' ', '_')}"):
            set_prompt(text)
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
