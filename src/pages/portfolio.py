import streamlit as st
import pandas as pd
from variables import stock_database
from navbar import create_navbar

st.set_page_config(page_title="My Portfolio", page_icon="💼", layout="wide")

create_navbar()

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

/* --- Stock Card Styling --- */
.stock-row {
    background-color: #1E1E1E;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
    border: 1px solid #333;
    transition: all 0.2s;
}
.stock-row:hover {
    border-color: #00F2C4;
    background-color: #252525;
    transform: translateX(5px);
}

/* --- Buttons --- */
div.stButton > button {
    border-radius: 20px;
    font-weight: bold;
    border: none;
    padding: 5px 20px;
}

/* --- Radio Button Styling (Shared) --- */
div[role="radiogroup"] > label > div:first-child { display: none; }
div[role="radiogroup"] { gap: 20px; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
div[role="radiogroup"] label p { font-size: 16px; color: #888; font-weight: 500; cursor: pointer; }
        
/* Hide Header */
header {visibility: hidden;}
.block-container {padding-top: 2rem; max-width: 100%;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# STATE MANAGEMENT
# ---------------------------------------------------------
if "my_portfolio" not in st.session_state:
    st.session_state.my_portfolio = []

if "portfolio_filter" not in st.session_state:
    st.session_state.portfolio_filter = "All"

if "search_filter" not in st.session_state:
    st.session_state.search_filter = "All"

# Function สำหรับ Add/Remove หุ้น
def toggle_stock(sym):
    if sym in st.session_state.my_portfolio:
        st.session_state.my_portfolio.remove(sym)
    else:
        st.session_state.my_portfolio.append(sym)

# ---------------------------------------------------------
# SEARCH MODAL FUNCTION 
# ---------------------------------------------------------
@st.dialog("Search Asset to Add", width="large")
def search_modal():
    st.markdown("""
        <style>
            div.stButton > button {
                width: 100%;
                text-align: left !important;
                background-color: transparent;
                border: none;
                border-bottom: 1px solid #333;
                color: #e0e0e0;
                padding: 12px 0px;
                font-size: 16px;
                border-radius: 0px;
                margin: 0px;
                display: flex;
                align-items: center;
                justify-content: flex-start;
            }
            div.stButton > button:hover {
                background-color: #2A2A2A;
                color: #00F2C4;
                border-color: #00F2C4;
                padding-left: 10px;
                transition: all 0.2s;
            }
            div[data-testid="stImage"] {
                display: flex; align-items: center; justify-content: center; margin-top: 5px; 
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Search Box inside Modal ---
    search_query = st.text_input("", placeholder="🔍 Search symbol, company (e.g. BTC, NVDA)", label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filter Tab inside Modal
    filter_options = ["All", "Stock", "Crypto", "Index"]
    selected_filter = st.radio(
        "Filter_Modal",
        options=filter_options,
        index=filter_options.index(st.session_state.search_filter) if st.session_state.search_filter in filter_options else 0,
        horizontal=True,
        label_visibility="collapsed",
        key="filter_radio_modal" 
    )
    st.session_state.search_filter = selected_filter

    # st.markdown("---")
    
    # List Result inside Modal
    with st.container(height=400, border=False):
        count = 0
        for stock in stock_database:
            # Logic Filter
            query_match = (search_query.lower() in stock['symbol'].lower()) or (search_query.lower() in stock['name'].lower())
            category_match = (selected_filter == "All") or (stock['type'] == selected_filter)
            
            if query_match and category_match:
                count += 1
                row_c1, row_c2, row_c3 = st.columns([0.8, 5, 1.0], vertical_alignment="center")
                
                # Logo
                with row_c1:
                    logo_url = f"https://logo.clearbit.com/{stock.get('domain', '')}"
                    st.image(logo_url, width=32)
                
                # Check status
                is_selected = stock['symbol'] in st.session_state.my_portfolio
                status_icon = "✅ Added" if is_selected else ""
                
                # Button (Click to Toggle)
                with row_c2:
                    btn_text = f"{stock['symbol']}  |  {stock['name']}"
                    if st.button(btn_text, key=f"modal_btn_{stock['symbol']}"):
                        toggle_stock(stock['symbol'])
                        st.rerun()
                
                # Type / Status Label
                with row_c3:
                    if is_selected:
                        st.markdown(f"<span style='color:#00F2C4; font-weight:bold; font-size:12px;'>{status_icon}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span style='color:#666; font-size:12px;'>{stock['type']}</span>", unsafe_allow_html=True)
        
        if count == 0:
            st.caption("No results found matching your criteria.")

# ---------------------------------------------------------
# HEADER & CONTROLS
# ---------------------------------------------------------
c_head, c_port = st.columns([3, 1])
with c_head:
    st.title("💼 Build Your Portfolio")
    st.caption("Select assets to track in your personalized dashboard.")

# --- CONTROL BAR (Updated with Search Modal Trigger) ---
col_search_btn, col_filter = st.columns([2, 2], vertical_alignment="center")

with col_search_btn:
    if st.button("🔍 Click here to Search & Add Assets", use_container_width=True):
        search_modal()

with col_filter:
    main_filter_options = ["All", "Stock", "Crypto"]
    main_selected = st.radio(
        "Main_Filter",
        options=main_filter_options,
        index=0,
        horizontal=True,
        label_visibility="collapsed",
        key="main_filter_radio"
    )

st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN CONTENT 
# ---------------------------------------------------------

col_list, col_sidebar = st.columns([2.5, 1.2])

with col_list:
    filtered_stocks = []
    for s in stock_database:
        if s.get('type') in ['Index', 'FX']: continue
        
        match_type = (main_selected == "All") or (s['type'] == main_selected)
        if match_type:
            filtered_stocks.append(s)

    # --- RENDER LIST ---
    if not filtered_stocks:
        st.info("No assets found.")
    else:
        with st.container(height=600, border=False):
            for stock in filtered_stocks:
                symbol = stock['symbol']
                name = stock['name']
                st_type = stock.get('type', 'Asset')
                domain = stock.get('domain', '')
                
                is_selected = symbol in st.session_state.my_portfolio
                
                # --- LAYOUT ROW ---
                with st.container():
                    c1, c2, c3 = st.columns([0.15, 0.65, 0.2], vertical_alignment="center")
                    
                    with c1:
                        if domain:
                            st.image(f"https://logo.clearbit.com/{domain}", width=40)
                        else:
                            st.markdown("⚪")

                    with c2:
                        st.markdown(f"""
                            <div style="line-height: 1.2;">
                                <span style="font-weight: bold; font-size: 18px; color: #FFF;">{symbol}</span>
                                <span style="font-size: 12px; color: #888; background: #333; padding: 2px 6px; border-radius: 4px; margin-left: 8px;">{st_type}</span>
                                <br>
                                <span style="font-size: 14px; color: #BBB;">{name}</span>
                            </div>
                        """, unsafe_allow_html=True)

                    with c3:
                        if is_selected:
                            st.button("Remove ❌", key=f"btn_rem_{symbol}", on_click=toggle_stock, args=(symbol,), type="primary")
                        else:
                            st.button("Add ➕", key=f"btn_add_{symbol}", on_click=toggle_stock, args=(symbol,))
                    
                    st.markdown("<hr style='margin: 5px 0; border-color: #333; opacity: 0.3;'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# RIGHT SIDEBAR 
# ---------------------------------------------------------
with col_sidebar:
    st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; border: 1px solid #00F2C4;">
            <h3 style="margin-top:0;">🌟 Your Selection</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") 

    if len(st.session_state.my_portfolio) > 0:
        st.write(f"Selected: **{len(st.session_state.my_portfolio)}** assets")
        
        for item in st.session_state.my_portfolio:
            st.markdown(f"""
                <div style="
                    display: flex; justify-content: space-between; 
                    background: #262626; padding: 10px; 
                    margin-bottom: 5px; border-radius: 5px; border-left: 3px solid #00F2C4;
                ">
                    <span style="font-weight: bold;">{item}</span>
                    <span style="color: #00F2C4;">✔</span>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("🚀 Analyze Portfolio", use_container_width=True, type="primary"):
             st.switch_page("pages/feed.py")
             
        if st.button("Clear All", use_container_width=True):
            st.session_state.my_portfolio = []
            st.rerun()
            
    else:
        st.info("Your portfolio is empty.")
        st.caption("Use the 'Search' button above or browse the list to add assets.")