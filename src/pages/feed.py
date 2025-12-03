import streamlit as st
import pandas as pd
import math
import os
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from google import genai
from dotenv import load_dotenv
from navbar import create_navbar
create_navbar()

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="News Feed", page_icon="📰", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
source_path = BASE_DIR.parent / 'Data_Sources.csv' 

try:
    df = pd.read_csv(source_path, encoding='utf-8')
    df['Date_Obj'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df = df.sort_values(by='Date_Obj', ascending=False)
    df = df.reset_index(drop=True)

except FileNotFoundError:
    st.error("ไม่พบไฟล์ Data_Sources.csv กรุณาอัปโหลดไฟล์")
    st.stop()

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

    /* --- Navbar --- */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 50px;
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 999;
        background: rgba(0,0,0,0.2); 
        backdrop-filter: blur(8px);
    }
    .nav-logo {
        font-weight: 800;
        font-size: 1.3rem;
        color: #fff;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .nav-center {
        display: flex;
        gap: 40px;
    }
    .nav-link {
        color: #ffffff !important;
        text-decoration: none !important;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        position: relative;
    }
    .nav-link:hover {
        color: #ffffff !important;
        text-shadow: 0 0 8px rgba(255,255,255,0.8);
    }

    /* --- Contact Us Button --- */
    .nav-btn-contact {
        background-color: #D34528;
        color: #000000;
        padding: 10px 25px;
        border-radius: 4px;
        text-decoration: none !important;
        font-size: 0.8rem;
        font-weight: 700;
        transition: 0.3s;
        border: 1px solid #D34528;
    }
    .nav-btn-contact:hover {
        background-color: transparent;
        color: #D34528;
        box-shadow: 0 0 10px rgba(211, 69, 40, 0.5);
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
    .block-container {padding-top: 0; max-width: 100%;}
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
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        div[data-testid="stMetric"] {
            background-color: #1E1E1E;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #00F2C4;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        }
        h1, h2, h3, h4, h5 {
            color: #FFFFFF; 
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def fetch_metadata_image(url):
    try:
        if "tiktok.com" in url:
            oembed_url = f"https://www.tiktok.com/oembed?url={url}"
            response = requests.get(oembed_url, timeout=5)
            data = response.json()
            return data.get('thumbnail_url', None)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]
            
    except Exception as e:
        return None
    return None

def get_thumbnail(link, source_type):
    link = str(link).strip()
    source_type = str(source_type).lower()
    
    if "youtube" in link or "youtu.be" in link:
        video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', link)
        if video_id_match:
            return f"https://img.youtube.com/vi/{video_id_match.group(1)}/hqdefault.jpg"
        return "https://placehold.co/640x360/FF0000/FFFFFF/png?text=YouTube+Error"

    real_image = fetch_metadata_image(link)
    
    if real_image:
        return real_image
    if "tiktok" in source_type:
        return "https://placehold.co/640x360/000000/FFFFFF/png?text=TikTok"
    elif "podcast" in source_type:
        return "https://placehold.co/640x360/8A2BE2/FFFFFF/png?text=Podcast"
    else:
        return "https://placehold.co/640x360/333333/FFFFFF/png?text=News"

# ---------------------------------------------------------
# RENDER FEED
# ---------------------------------------------------------
st.title("📰 Latest News & Insights")
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

cols = st.columns(4)

for index, row in df.iterrows():
    col_idx = index % 4
    
    with cols[col_idx]:
        title = row.get('Title', 'No Title')
        source_type = str(row.get('Sources', 'General'))
        date_str = str(row.get('Date', '-'))
        link = row.get('Link', '')
        
        badge_class = f"badge-{source_type.lower()}" if source_type.lower() in ['youtube', 'tiktok', 'podcast'] else "badge-general"
        
        thumbnail = get_thumbnail(link, source_type)


        st.markdown(f"""
        <div class="news-card-box">
            <div style="width:100%; height:160px; overflow:hidden;">
                <img src="{thumbnail}" style="width:100%; height:100%; object-fit:cover;">
            </div>
            <div class="card-title">{title}</div>
            <div class="card-meta">
                <span class="badge {badge_class}">{source_type}</span>
                <span>📅 {date_str}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View Analysis ➔", key=f"btn_{index}", use_container_width=True):
            st.session_state['selected_news'] = row.to_dict()
            st.switch_page("pages/analysis.py")
        st.write("") 
        st.write("")