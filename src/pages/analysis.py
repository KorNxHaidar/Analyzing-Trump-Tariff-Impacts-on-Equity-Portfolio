# news.py
import streamlit as st
import os
import requests
import json
import re
import streamlit.components.v1 as components
from pathlib import Path
from google import genai
from dotenv import load_dotenv
from variables import prompt_template
from navbar import create_navbar

create_navbar()
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
st.set_page_config(page_title="Port Analysis", page_icon="📈")

st.markdown("""
<style>
    /* --- Import Font --- */
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
        overflow-x: hidden;
    }

    /* --- Background --- */
    .stApp {
        background-color: #000000;
        background-image: 
            radial-gradient(circle at 20% 60%, rgba(41, 98, 255, 0.25) 0%, transparent 50%),
            radial-gradient(circle at 80% 40%, rgba(255, 87, 34, 0.15) 0%, transparent 50%);
        background-attachment: fixed;
    }

    /* --- Glowing Ring --- */
    .glowing-ring {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        width: 55vh; height: 55vh;
        border-radius: 50%;
        box-shadow: 
            -20px 0 70px rgba(60, 120, 255, 0.5), 
            20px 0 70px rgba(255, 100, 50, 0.4);
        z-index: 0;
        pointer-events: none;
    }
    .glowing-ring::after {
        content: '';
        position: absolute;
        top: -2px; left: -2px; right: -2px; bottom: -2px;
        border-radius: 50%;
        border: 1px dashed rgba(255,255,255,0.15);
        animation: spin 25s linear infinite;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }

    /* --- Typography --- */
    h1 {
        font-weight: 300 !important;
        font-size: 4.5rem !important;
        line-height: 1.1 !important;
        color: #ffffff !important;
        margin-bottom: 20px !important;
    }
    .shield-icon {
        font-size: 3rem; 
        vertical-align: middle;
        margin-left: 10px;
    }
    .sub-text {
        color: #999;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* Hide Header */
    header {visibility: hidden;}
    .block-container {
        padding-top: 40px !important; 
    }
    /* Card Container */
    .news-card-box {
        background-color: #1E1E1E;
        border-radius: 12px;
        padding: 0px;
        margin-bottom: 15px;
        border: 1px solid #333;
        overflow: hidden;
        transition: transform 0.2s;
    }
    .news-card-box:hover {
        border-color: #00F2C4;
        transform: translateY(-3px);
    }
    
    /* Title Style */
    .card-title {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: #FFFFFF;
        margin: 10px 15px 5px 15px;
        
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        height: 40px; 
    }
    
    .card-meta {
        font-size: 12px;
        color: #AAAAAA;
        padding: 0 15px 15px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .badge {
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: bold;
        text-transform: uppercase;
    }
    .badge-youtube { background: #FF0000; color: white; }
    .badge-tiktok { background: #000000; color: white; }
    .badge-podcast { background: #8A2BE2; color: white; }
    .badge-general { background: #555; color: white; }

    div.stButton > button {
        width: 100%;
        border-radius: 0 0 12px 12px; 
        margin-top: -10px; /* ดึงปุ่มขึ้นไปติด Card */
        border: 1px solid #333;
        border-top: none;
    }

    /* --- Expander / Analysis Box Styling --- */
    
    /* 1. ปรับกล่อง Expander ให้ดูเป็น Card */
    div[data-testid="stExpander"] {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-radius: 12px;
        margin-bottom: 12px;
        overflow: hidden; /* เพื่อให้ขอบมนทำงานสมบูรณ์ */
    }

    div[data-testid="stExpander"] details summary,
    div[data-testid="stExpander"] details summary p,
    div[data-testid="stExpander"] details summary span,
    div[data-testid="stExpander"] details summary div {
        font-size: 24px !important; 
        font-weight: 800 !important;
        color: #FFFFFF !important;
        line-height: 1.5 !important;
    }

    div[data-testid="stExpander"] details summary svg {
        width: 24px !important;
        height: 24px !important;
        margin-right: 15px !important;
        color: #00F2C4 !important;
    }

    div[data-testid="stExpander"]:hover {
        border-color: #00F2C4;
        transform: scale(1.01);
        transition: all 0.2s ease-in-out;
    }

    /* Button Styling */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        font-size: 18px !important;
    }
</style>
""", unsafe_allow_html=True)


if "selected_news" not in st.session_state:
    st.warning("⚠️ กรุณาเลือกข่าวจากหน้า News Feed ก่อน")
    if st.button("Back to Feed"):
        st.switch_page("pages/feed.py")
    st.stop()

selected_news_item = st.session_state['selected_news']
st.subheader(f"📑 News: {selected_news_item.get('Title', 'Unknown Title')}")

# ตั้งค่า Path
BASE_DIR = Path(__file__).resolve().parent
target_filename = selected_news_item.get('Name', '') 

if not target_filename:
    st.error("❌ ไม่พบข้อมูลชื่อไฟล์ใน CSV (กรุณาเช็ค column 'File_Name')")

data_path = BASE_DIR.parent.parent / 'data' / f'{target_filename}.txt'

news_text = ""
try:
    with open(data_path, 'r', encoding='utf-8') as f:
        news_text = f.read()
    
    # --- MEDIA PLAYER SECTION ---
    st.divider()
    col1, col_center, col2 = st.columns([1, 8, 1]) 

    with col_center:
        if selected_news_item is not None:
            st.write("#### ลงล่าสุดเมื่อ")
            with st.container():
                source = str(selected_news_item.get('Sources', '')).lower()
                link = str(selected_news_item.get('Link', ''))
                title = selected_news_item.get('Title', selected_news_item.get('Name', 'No Title')) 
                date = selected_news_item.get('Date', '-')
                
                st.info(f"📅 {date} | Source: {selected_news_item.get('Sources', '-')}")

                if "youtube" in source or "youtu" in link:
                    st.video(link)
                elif "podcast" in source or "apple" in link:
                    if "podcasts.apple.com" in link:
                        embed_link = link.replace("podcasts.apple.com", "embed.podcasts.apple.com")
                        components.iframe(embed_link, height=180, scrolling=False)
                        st.markdown(f"<div style='text-align: center;'><a href='{link}' target='_blank'>🔗 Open in Apple Podcasts</a></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"[Click to Listen External Link]({link})")
                elif "tiktok" in link or "tiktok" in source:
                    try:
                        clean_link = link.split('?')[0]
                        oembed_url = f"https://www.tiktok.com/oembed?url={clean_link}"
                        response = requests.get(oembed_url, timeout=2)
                        if response.status_code == 200:
                            data = response.json()
                            tiktok_html = data.get('html')
                            styled_html = f"""
                                <div style="display: flex; justify-content: center;">{tiktok_html}</div>
                                <script async src="https://www.tiktok.com/embed.js"></script>
                            """
                            components.html(styled_html, height=750, scrolling=True)
                        else:
                            raise Exception("OEmbed failed")
                    except:
                        st.markdown(f"<a href='{link}' target='_blank'>Watch on TikTok</a>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align: center; padding: 20px; background-color: #262730; border-radius: 10px;'><a href='{link}' target='_blank' style='color: #00F2C4; font-weight: bold;'>Open External Link</a></div>", unsafe_allow_html=True)
    
    st.divider()

except FileNotFoundError:
    st.error(f"❌ ไม่พบไฟล์ Text: {target_filename}")
    st.info(f"ระบบพยายามหาที่: {data_path}")
    st.warning("กรุณาตรวจสอบว่าชื่อไฟล์ใน CSV ตรงกับชื่อไฟล์ในโฟลเดอร์ data หรือไม่")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

# ---------------------------------------------------------
# 2. GET USER PORTFOLIO
# ---------------------------------------------------------
if "my_portfolio" not in st.session_state or not st.session_state.my_portfolio:
    st.warning("⚠️ ยังไม่ได้เลือกหุ้นจากหน้าแรก กรุณากลับไปเลือกก่อน")
    st.stop() 

selected_stocks_list = st.session_state.my_portfolio

st.write("### 💼 Stock in Portfolio")
st.info(f"Symbols: {', '.join(selected_stocks_list)}")

# ---------------------------------------------------------
# 3. SIDEBAR & API CONFIG
# ---------------------------------------------------------
with st.sidebar:
    st.write("Setting API KEY")
    env_api_key = os.getenv("GOOGLE_API_KEY")
    
    if "GOOGLE_API_KEY" not in os.environ and not env_api_key:
        default_api_key = ""
        with st.popover("🔐 GOOGLE API KEY"):
            gemini_api_key = st.text_input(
                "Introduce your GOOGLE API Key", 
                value=default_api_key, 
                type="password",
                key="google_api_key",
            )
            if gemini_api_key:
                try:
                    genai.Client(api_key=gemini_api_key)
                    st.session_state.api_key_configured = True
                    st.success("API Key Configured!")
                except Exception as e:
                    st.error(f"Error configuring API: {e}")
                    st.session_state.api_key_configured = False
            else:
                st.session_state.api_key_configured = False
                
    else:
        gemini_api_key = env_api_key if env_api_key else os.getenv("GOOGLE_API_KEY")
        try:
            genai.Client(api_key=gemini_api_key)
            st.session_state.api_key_configured = True
            st.success("API Key loaded from environment.", icon="✅")
        except Exception as e:
            st.error(f"Error configuring API from env: {e}")
            st.session_state.api_key_configured = False

# ---------------------------------------------------------
# 4. PREPARE PROMPT & ANALYZE
# ---------------------------------------------------------
st.write('### Analysis Your Portfolio')

json_instruction = """
IMPORTANT: 
Respond ONLY in valid JSON format. 
Do not wrap the response in markdown code blocks (like ```json ... ```).
Just return the raw JSON object starting with { and ending with }.
Structure:
{
    "situation": "Markdown text...",
    "current_status": "Markdown text...",
    "portfolio_impact": "Markdown text...",
    "investor_takeaway": "Markdown text..."
}
"""

prompt = f"{prompt_template(my_portfolio=selected_stocks_list, news_text=news_text)}\n\n{json_instruction}"

def clean_json_response(text):
    """ลบ Markdown Code Block (```json ... ```) ออกจากข้อความ"""
    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s*```$', '', text, flags=re.MULTILINE)
    return text.strip()

# Initialize Session State for Analysis Result
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if not GOOGLE_API_KEY and ('api_key_configured' not in st.session_state or not st.session_state.api_key_configured):
    st.error("กรุณาใส่ Google API Key ก่อนใช้งาน")
else:
    client = genai.Client(api_key=gemini_api_key)

    if st.session_state.analysis_result is None:
        if st.button("Generate Summary", type="primary"):
            
            with st.spinner('รอสักครู่ ระบบกำลังวิเคราะห์ผลกระทบสำหรับพอร์ตของคุณ...'):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=[prompt],
                        config={'response_mime_type': 'application/json'} 
                    )

                    if response.text:
                        # Clean & Parse JSON
                        cleaned_text = clean_json_response(response.text)
                        analysis_data = json.loads(cleaned_text)
                        
                        # บันทึกผลลัพธ์ลง Session State
                        st.session_state.analysis_result = analysis_data
                        
                        # Rerun เพื่อซ่อนปุ่มและแสดงผลลัพธ์
                        st.rerun()
                        
                    else:
                        st.warning("AI ไม่ตอบกลับข้อมูล กรุณาลองใหม่")
                        
                except json.JSONDecodeError as e:
                    st.error("เกิดข้อผิดพลาดในการแปลงข้อมูล JSON จาก AI")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาดของระบบ: {e}")

    else:
        st.write("### 📊 ผลการวิเคราะห์")
        st.divider()
        
        data = st.session_state.analysis_result
        
        # Dropdown
        with st.expander("1. 🚩 สรุปสถานการณ์ (The Situation)", expanded=True):
            st.markdown(data.get("situation", "-"))

        with st.expander("2. 🌎 สถานะปัจจุบัน (Current Status)", expanded=False):
            st.markdown(data.get("current_status", "-"))

        with st.expander("3. 🎯 ผลกระทบต่อหุ้นในพอร์ต (Portfolio Impact)", expanded=False):
            st.markdown(data.get("portfolio_impact", "-"))

        with st.expander("4. 🧠 ตีความแบบนักลงทุน (Investor Takeaway)", expanded=False):
            st.markdown(data.get("investor_takeaway", "-"))
            
        st.write("")
        if st.button("Clear Result"):
            st.session_state.analysis_result = None
            st.rerun()