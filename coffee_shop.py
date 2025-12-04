"""
☕ BEAN & BREW COFFEE SHOP ASSISTANT
Professional Portfolio-Ready Bot
Save as: coffee_shop.py
"""

import streamlit as st
import requests
import time
from datetime import datetime
from collections import defaultdict

# ==================== CONFIGURATION ====================
GOOGLE_API_KEY = "AIzaSyCRoaWiiOGsslJ5VQwPXo-pfYRmOUMxu5Q"  # ⚠️ REPLACE THIS

RATE_LIMIT = 10
RATE_LIMIT_WINDOW = 60
CACHE_TTL = 300

# ==================== SESSION STATE ====================
if 'rate_limit_tracker' not in st.session_state:
    st.session_state.rate_limit_tracker = defaultdict(list)
if 'response_cache' not in st.session_state:
    st.session_state.response_cache = {}

# ==================== KNOWLEDGE BASE ====================
COFFEE_INFO = """
BEAN & BREW COFFEE SHOP

Location: 456 Main Street, Downtown
Phone: (555) 456-7890
Hours: Mon-Fri 6:30 AM - 8:00 PM, Weekends 7:00 AM - 9:00 PM

MENU:
Hot Drinks: Espresso $3.50, Americano $4, Cappuccino $4.50, Latte $5, Mocha $5.50
Cold Drinks: Iced Coffee $4.50, Iced Latte $5.50, Cold Brew $5, Frappuccino $6.50
Specialty: Caramel Macchiato $6, Vanilla Latte $5.50, Pumpkin Spice Latte $6.50
Food: Croissants $3.50, Muffins $3, Bagels $4.50, Avocado Toast $8, Panini $9

Milk options: Oat/Almond/Soy (+$0.75)
Loyalty: Buy 9, get 10th FREE!
"""

# ==================== FUNCTIONS ====================
def check_rate_limit():
    current_time = time.time()
    requests_list = st.session_state.rate_limit_tracker["user"]
    requests_list = [t for t in requests_list if current_time - t < RATE_LIMIT_WINDOW]
    st.session_state.rate_limit_tracker["user"] = requests_list
    if len(requests_list) >= RATE_LIMIT:
        return False
    requests_list.append(current_time)
    return True

def get_cached_response(question):
    cache_key = f"coffee:{question}"
    if cache_key in st.session_state.response_cache:
        cached = st.session_state.response_cache[cache_key]
        if time.time() - cached['timestamp'] < CACHE_TTL:
            return cached['response']
    return None

def cache_response(question, response):
    st.session_state.response_cache[f"coffee:{question}"] = {
        'response': response, 'timestamp': time.time()
    }

def ask_barista(question):
    try:
        if not check_rate_limit():
            return "⏱️ Please wait a moment before asking another question!"
        
        cached = get_cached_response(question)
        if cached:
            return cached
        
        if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_API_KEY_HERE":
            return "❌ System not configured. Please contact administrator."
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GOOGLE_API_KEY}"
        
        prompt = f"""You are Maya, a friendly barista at Bean & Brew Coffee Shop.

Answer using ONLY this information:
{COFFEE_INFO}

Customer: {question}

Your response:"""
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.8, "maxOutputTokens": 600}
        }
        
        response = requests.post(url, headers={'Content-Type': 'application/json'}, 
                               json=payload, timeout=20)
        
        if response.status_code == 429:
            return """😅 Oops! Too many questions right now.

**What to do:**
• Wait 60 seconds and try again
• The system has rate limits to prevent overload

Sorry for the inconvenience! ☕"""
        
        if response.status_code != 200:
            return "❌ Sorry, something went wrong. Please try again in a moment."
        
        answer = response.json()['candidates'][0]['content']['parts'][0]['text']
        cache_response(question, answer)
        return answer
        
    except requests.exceptions.Timeout:
        return "⏰ Request timed out. Please try again!"
    except Exception as e:
        return "❌ Sorry, I'm having trouble right now. Please try again!"

# ==================== PAGE SETUP ====================
st.set_page_config(
    page_title="Bean & Brew Coffee Shop",
    page_icon="☕",
    layout="wide"
)

# ==================== STYLING ====================
st.markdown("""
<style>
    /* Remove default padding */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Full gradient background - NO WHITE */
    .main, .stApp {
        background: linear-gradient(135deg, #6B4423 0%, #3E2723 50%, #1B0F0A 100%) !important;
    }
    
    /* Center all content */
    .main .block-container {
        max-width: 900px;
        padding: 2rem 1rem;
    }
    
    /* Title - CENTERED */
    .main h1 {
        color: #FFE4C4 !important;
        text-align: center !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.7);
        margin: 0 auto 0.5rem auto !important;
        padding: 0 !important;
    }
    
    /* Subtitle - CENTERED */
    .subtitle {
        color: #D4A574;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 300;
        letter-spacing: 3px;
        margin-bottom: 2rem;
    }
    
    /* Status box */
    .status-box {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 1.5rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.4);
    }
    
    /* Info card */
    .info-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.8rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    }
    
    .info-card h3 {
        color: #6B4423 !important;
        margin-bottom: 1rem !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 18px !important;
        padding: 1.2rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3) !important;
    }
    
    /* Chat input */
    .stChatInput > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 30px !important;
        border: 3px solid rgba(139, 69, 19, 0.5) !important;
    }
    
    /* Hide sidebar completely for users */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #D4A574;
        padding: 2rem 0 1rem 0;
        margin-top: 3rem;
        border-top: 2px solid rgba(212, 165, 116, 0.3);
    }
    
    .footer h3 {
        color: #FFE4C4 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== CONTENT ====================
st.title("☕ Bean & Brew")
st.markdown('<p class="subtitle">Coffee Shop Assistant</p>', unsafe_allow_html=True)

# Status
if GOOGLE_API_KEY and GOOGLE_API_KEY != "YOUR_API_KEY_HERE":
    st.markdown('<div class="status-box">✅ Online - Ready to Help!</div>', unsafe_allow_html=True)
else:
    st.error("⚠️ System Offline")
    st.stop()

# Info
st.markdown("""
<div class="info-card">
    <h3>🌟 Welcome to Bean & Brew!</h3>
    <p><strong>Hours:</strong> Mon-Fri 6:30 AM - 8:00 PM | Weekends 7:00 AM - 9:00 PM<br>
    <strong>Location:</strong> 456 Main Street, Downtown<br>
    <strong>Special:</strong> Buy 9 drinks, get 10th FREE!<br>
    <strong>Rating:</strong> ⭐⭐⭐⭐⭐ 4.9/5</p>
</div>
""", unsafe_allow_html=True)

# Chat
if 'messages' not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": """Hey there! ☕ I'm Maya, your friendly barista!

I can help with:
✅ Menu and prices
✅ Customizations
✅ Loyalty program
✅ Store info

What can I get for you today? 😊"""
    }]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask Maya anything!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("☕ Brewing your answer..."):
            answer = ask_barista(prompt)
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# Footer
st.markdown("""
<div class="footer">
    <h3>☕ Bean & Brew Coffee Shop</h3>
    <p>456 Main Street, Downtown<br>
    📞 (555) 456-7890 | ✉️ hello@beanandbrew.com<br><br>
    🤖 AI-Powered Assistant | Portfolio Project</p>
</div>

""", unsafe_allow_html=True)
