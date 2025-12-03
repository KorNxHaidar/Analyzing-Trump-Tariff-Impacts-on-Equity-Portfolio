import streamlit as st
from navbar import create_navbar 
create_navbar()

# --- 1. ตั้งค่าหน้าเพจ ---
st.set_page_config(layout="wide", page_title="Home")

# --- 2. Custom CSS ---
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
    margin-bottom: 40px;
}

/* Hide Header */
header {visibility: hidden;}
.block-container {padding-top: 0; max-width: 100%;}

/* =========================================
   STYLING STREAMLIT PAGE LINKS
   ========================================= */

div[data-testid="stPageLink"] a {
    display: inline-flex;
    justify-content: center;
    align-items: center;
    text-decoration: none !important;
    padding: 12px 32px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease-in-out;
    width: 100%; 
}


div[data-testid="stPageLink"] a::after {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# --- 4. Glowing Ring ---
st.markdown('<div class="glowing-ring"></div>', unsafe_allow_html=True)

# --- 5. Spacer ---
for _ in range(8): st.write("")

# --- 6. Main Content ---
c1, c2 = st.columns([1.2, 1])

with c1:
    st.markdown("""
    <div style="padding-left: 60px; position: relative; z-index: 1;">
        <h1>
            Make Investing <br>
            Smarter <span class="shield-icon">📈</span><br>
            Today
        </h1>
        <p class="sub-text">
            Effortlessly track your stocks and analyze market news <br>
            with our intelligent portfolio insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- BUTTONS SECTION  ---
    st.markdown('<div style="padding-left: 60px; position: relative; z-index: 2;">', unsafe_allow_html=True)
    
    btn_col1, btn_col2, btn_spacer = st.columns([0.25, 0.4, 0.5]) 
    
    with btn_col1:
        st.page_link("pages/feed.py", label="Read News ↗")
        
    with btn_col2:
        st.page_link("pages/portfolio.py", label="Set Your Portfolio", icon="⚡")
        
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    pass