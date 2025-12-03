# filename: navbar.py
import streamlit as st

def create_navbar():
    # ---------------------------------------------------------
    # 1. CSS
    # ---------------------------------------------------------
    st.markdown("""
    <style>
        .block-container {
            padding-top: 20px !important;
        }
        header {visibility: hidden;}

        /* Navbar Container */
        .nav-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 70px; /* ความสูง Navbar */
            background-color: rgba(0, 0, 0, 0.5); /* พื้นหลังดำโปร่งแสง */
            backdrop-filter: blur(10px);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        /* ปรับแต่ง Link ของ Streamlit (st.page_link) */
        div[data-testid="stPageLink-NavLink"] {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 15px !important;
        }

        /* Text ข้างใน Link */
        div[data-testid="stPageLink-NavLink"] p {
            font-family: 'Manrope', sans-serif !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            transition: color 0.3s ease !important;
        }

        /* Hover Effect (สีขาวเรืองแสง) */
        div[data-testid="stPageLink-NavLink"]:hover p {
            color: #D34528 !important; /* สีส้ม */
            text-shadow: 0 0 8px rgba(211, 69, 40, 0.5);
        }
        
        div[data-testid="stPageLink-NavLink"] svg {
            display: none !important;
        }

        .btn-contact {
            background-color: #D34528;
            color: white !important;
            padding: 8px 24px;
            border-radius: 4px;
            text-decoration: none !important;
            font-weight: 700;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: all 0.3s;
        }
        .btn-contact:hover {
            background-color: transparent;
            border: 1px solid #D34528;
            color: #D34528 !important;
            box-shadow: 0 0 10px rgba(211, 69, 40, 0.5);
        }
        
        /* LOGO Style */
        .nav-logo {
            font-size: 20px;
            font-weight: 800;
            color: white;
            display: flex;
            align-items: center;
            gap: 10px;
            letter-spacing: 1px;
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 2. LAYOUT: สร้าง Navbar ด้วย Columns
    # ---------------------------------------------------------
    
    with st.container():
        c1, c2, c3, c4, c5, c6 = st.columns([3.0, 0.8, 1, 1, 0.8, 1.5], vertical_alignment="center")
        
        # --- LOGO ---
        with c1:
            st.markdown('<div class="nav-logo"><span>&#9679;</span> FIN FIN</div>', unsafe_allow_html=True)
            
        # --- MENU LINKS (ใช้ st.page_link เพื่อกันข้อมูลหาย) ---
        with c2:
            st.page_link("app.py", label="Home")
        with c3:
            st.page_link("pages/overview.py", label="Overview")
        with c4:
            st.page_link("pages/portfolio.py", label="Portfolio")
        with c5:
            st.page_link("pages/feed.py", label="News")
            
        # --- CONTACT BUTTON ---
        with c6:
            st.markdown('<div style="text-align: right;"><a href="#" class="btn-contact">CONTACT US</a></div>', unsafe_allow_html=True)