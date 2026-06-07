# AI STUDIO - AI Image Generator Web App

> **CREATE THE FUTURE**
> A premium, commercial-grade, glassmorphic AI Image Generator Web App styled with a futuristic dark-sci-fi theme, built using Python, Streamlit, and Hugging Face's `black-forest-labs/FLUX.1-schnell` Inference API.

![AI Studio Reference Style UI](assets/background.jpg)

## Features
- **SaaS Enterprise Aesthetic**: Stunning glassmorphism UI overlay, customized scrollbars, premium Outfit & Space Grotesk typography, glowing buttons, and dark blue cyber theme.
- **State Management**: Session-based prompt selection from curated template buttons (examples).
- **Production-grade API client**: Auto-retry logic for busy endpoints (HTTP 503), authentication verification, timeout recovery, and clean error alert modals.
- **Fast Generation**: Harnesses the cutting-edge FLUX.1-schnell model hosted on Hugging Face Serverless API.

## Requirements
- Python 3.11+
- Hugging Face Inference API Access Token (free or paid)

## Local Setup

1. **Clone this repository**:
   ```bash
   git clone https://github.com/helear2252-ctrl/NEWAPP.git
   cd ai-image-generator
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your Hugging Face Access Token:
   ```env
   HF_TOKEN=your_huggingface_access_token_here
   ```
   *Note: You can get your Hugging Face token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).*

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

---

## Deployment to Streamlit Cloud

1. Push your code to your GitHub Repository.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and create a new app.
3. Select your repository, branch (`main`), and set the Main file path to `app.py`.
4. Under **Advanced Settings**, add your Hugging Face API token inside the Secrets field:
   ```toml
   HF_TOKEN = "your_actual_token_here"
   ```
5. Deploy and watch your app come alive at your custom URL!
