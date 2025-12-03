import os
import re
import requests
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from pathlib import Path  
from google import genai
from variables import stock_database
from dotenv import load_dotenv
from navbar import create_navbar

load_dotenv()

create_navbar()

st.set_page_config(layout="wide", page_title="Market Overviews", page_icon="📈")

st.markdown("""
<style>
/* --- Import Font --- */
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;800&display=swap');

/* --- Background --- */
.stApp {
    background-color: #000000;
    background-image: 
    radial-gradient(circle at 20% 60%, rgba(41, 98, 255, 0.25) 0%, transparent 50%),
    radial-gradient(circle at 80% 40%, rgba(255, 87, 34, 0.15) 0%, transparent 50%);
    background-attachment: fixed;
}
html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
    overflow-x: hidden;
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
    padding-top: 50px !important; 
    max-width: 100%;
}

.custom-asset-btn {
    border: 1px solid #444;
    padding: 10px;
    border-radius: 8px;
    text-align: center;
    background: #1E1E1E;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_stock_data(sym, per):
    ticker = yf.Ticker(sym)
    data = ticker.history(period=per)
    return data, ticker.info

@st.cache_data
def load_news_data():
    try:
        df = pd.read_csv("Data_Sources.csv")
        df['Date_Obj'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', dayfirst=True)
        
        if 'Name' not in df.columns:
            df['Name'] = "No Title"
        if 'Sources' in df.columns:
            df['Sources'] = df['Sources'].astype(str).str.strip()
            
        return df
    except Exception as e:
        return pd.DataFrame(columns=['Date', 'Sources', 'Link', 'Name', 'Date_Obj'])

BASE_DIR = Path(__file__).resolve().parent

def get_gemini_summary(api_key, news_df):
    """
    Reads text files from: BASE_DIR.parent.parent / 'data' / {filename}.txt
    and summarizes using the new Google Gen AI SDK.
    """
    if not api_key:
        return "⚠️ Please provide a Google Gemini API Key in the sidebar."

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        return f"Error initializing Gemini Client: {e}"

    combined_text = ""
    found_files_count = 0

    sorted_news = news_df.sort_values(by="Date_Obj")

    if len(sorted_news) > 10:
        target_news = sorted_news.tail(20) 
    else:
        target_news = sorted_news

    for index, row in target_news.iterrows():
        target_filename = str(row['Name']).strip()
        
        try:
            data_path = BASE_DIR.parent.parent / 'data' / f'{target_filename}.txt'
            
            if data_path.exists():
                with open(data_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    content = content[:4000]
                    combined_text += f"\n---\nDate: {row['Date']}\nSource: {row['Sources']}\nTitle: {row.get('Title', row['Name'])}\nTranscript Content:\n{content}\n"
                    found_files_count += 1
            else:
                # Fallback: Log that file is missing but include metadata
                combined_text += f"\n---\nDate: {row['Date']}\nSource: {row['Sources']}\nTitle: {row.get('Title', row['Name'])}\n(Transcript file not found at {data_path})\n"
        except Exception as e:
            continue

    if not combined_text:
        return "No transcript data found in the specified directory."

    # Construct Prompt
    prompt = f"""
    You are a Chief Market Strategist providing a high-level intelligence report.
    Analyze the provided transcripts to generate a structured **Executive Market Report**.

    **Format Requirements:**

    **PART 1: 📊 Executive Summary (At the very top)**
    - Provide 3-4 bullet points summarizing the *overall trend* across all dates.
    - Identify the single biggest "Key Risk" and "Key Opportunity".

    **PART 2: 📅 Strategic Timeline (Day-by-Day)**
    For each key date, use this exact structure:

    ### 📅 [Date] : [Impactful Headline]
    **Sentiment:** [🔴 Negative / 🟢 Positive / 🟡 Neutral] | **Focus Sector:** [e.g. Export/Energy/Tech]
    
    [Insert 1-2 paragraphs of narrative storytelling here. Explain the event, cause-and-effect, and market reaction.]

    > **Key Stats:**
    > * [List specific numbers here, e.g., "Tax Rate: **19%**"]
    > * [Another number, e.g., "GDP Impact: **-0.77%**"]

    ---
    
    **Instructions:**
    1. **Language:** Thai (Professional & Insightful).
    2. **Data:** Be extremely precise with numbers in the "Key Stats" section.
    3. **Tone:** Concise, direct, and actionable.

    **Raw Data:**
    {combined_text}
    """

    try:
        with st.spinner(f'Analysing {found_files_count} transcript files with Gemini AI...'):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"
    
# ---------------------------------------------------------
# 3. SIDEBAR (TRADINGVIEW STYLE MODAL)
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

if "selected_symbol" not in st.session_state:
    st.session_state.selected_symbol = "^GSPC" # ค่า Default

stock_database = stock_database

@st.dialog("Search Symbol", width="large")
def search_modal():
    
    if "search_filter" not in st.session_state:
        st.session_state.search_filter = "All"

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
            }
            div.stButton > button:hover {
                background-color: #2A2A2A;
                color: #00F2C4;
                border-color: #00F2C4;
                padding-left: 10px;
                transition: all 0.2s;
            }

            div[role="radiogroup"] > label > div:first-child {
                display: none; 
            }
            div[role="radiogroup"] {
                gap: 20px;
            }

            div[role="radiogroup"] label p {
                font-size: 14px;
                color: #888888; /* สีเทา */
                font-weight: 500;
            }
               
            div[data-testid="stImage"] {
                display: flex; align-items: center; justify-content: center; margin-top: 5px; 
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Search Box ---
    search_query = st.text_input("", placeholder="🔍 Search symbol, company (e.g. BTC, NVDA)", label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    filter_options = ["All", "Stock", "Crypto", "Index"]
    
    selected_filter = st.radio(
        "Filter",
        options=filter_options,
        index=filter_options.index(st.session_state.search_filter),
        horizontal=True,
        label_visibility="collapsed",
        key="filter_radio" 
    )
    
    st.session_state.search_filter = selected_filter

    st.markdown("---")
    
    with st.container(height=400, border=False):
        
        count = 0
        
        for stock in stock_database:
            # 1. Search Query Filter
            query_match = (search_query.lower() in stock['symbol'].lower()) or (search_query.lower() in stock['name'].lower())
            
            # 2. Category Filter Logic 
            category_match = (selected_filter == "All") or (stock['type'] == selected_filter)
            
            if query_match and category_match:
                count += 1
                row_c1, row_c2, row_c3 = st.columns([0.8, 5, 2], vertical_alignment="center")
                
                with row_c1:
                    logo_url = f"https://logo.clearbit.com/{stock['domain']}"
                    st.image(logo_url, width=32)
                
                with row_c2:
                    btn_text = f"{stock['symbol']}  |  {stock['name']}"
                    if st.button(btn_text, key=f"btn_{stock['symbol']}"):
                        st.session_state.selected_symbol = stock['symbol']
                        st.rerun()
                
                with row_c3:
                    st.markdown(f"""
                        <div style='text-align: right; font-size: 12px; color: #666;'>
                            {stock['type']}<br>NASDAQ
                        </div>
                    """, unsafe_allow_html=True)
        
        if count == 0:
            st.caption("No results found matching your criteria.")

current_name = next((item['name'] for item in stock_database if item["symbol"] == st.session_state.selected_symbol), "")

with st.container():
    c1, c2, c3 = st.columns([2, 2, 1], gap="medium", vertical_alignment="center")

    with c1:
        st.caption("🔍 SELECT ASSET")
        if st.button(f"{current_name}", use_container_width=True, help="Click to search asset"):
            search_modal()
        symbol = st.session_state.selected_symbol

    with c2:
        st.caption("⏱️ TIMEFRAME")
        period = st.select_slider(
            "Timeframe", 
            options=["1mo", "3mo", "6mo", "1y", "5y"], 
            value="1y", 
            label_visibility="collapsed"
        )

    with c3:
        st.caption("📰 NEW OPTIONS")
        show_news_markers = st.toggle("Show News", value=True)
# ---------------------------------------------------------
# 4. MAIN DASHBOARD LOGIC
# ---------------------------------------------------------

st.title(f"⚡ Market Intelligence: {current_name}")

with st.spinner('Loading market data...'):
    stock_df, stock_info = load_stock_data(symbol, period)
    news_df = load_news_data()

if not stock_df.empty:
    
    stock_df.index = stock_df.index.tz_localize(None)
    min_date = stock_df.index.min()
    max_date = stock_df.index.max()
    
    # --- Metrics ---
    current_price = stock_df['Close'].iloc[-1]
    prev_price = stock_df['Close'].iloc[-2]
    change = current_price - prev_price
    pct_change = (change / prev_price) * 100
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current Price", f"${current_price:,.2f}", f"{pct_change:.2f}%")
    c2.metric("High", f"${stock_df['High'].max():,.2f}")
    c3.metric("Low", f"${stock_df['Low'].min():,.2f}")
    c4.metric("Avg Volume", f"{stock_df['Volume'].mean()/1e6:.2f}M")
    st.markdown("---")

    # --- Data Processing for News ---
    merged_news = pd.DataFrame()
    if not news_df.empty:
        mask = (news_df['Date_Obj'] >= min_date) & (news_df['Date_Obj'] <= max_date)
        filtered_news = news_df.loc[mask].copy().sort_values('Date_Obj')
        
        if not filtered_news.empty:
            stock_reset = stock_df.reset_index().rename(columns={'Date': 'Stock_Date'})
            merged_news = pd.merge_asof(
                filtered_news, 
                stock_reset[['Stock_Date', 'Close', 'Volume']], 
                left_on='Date_Obj', 
                right_on='Stock_Date', 
                direction='nearest',
                tolerance=pd.Timedelta('3d')
            )

    # --- Create Chart ---
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 1. Volume Bars
    colors = ['#26a69a' if row['Close'] >= row['Open'] else '#ef5350' for index, row in stock_df.iterrows()]
    fig.add_trace(go.Bar(
        x=stock_df.index,
        y=stock_df['Volume'],
        name='Volume',
        marker_color=colors,
        marker_line_width=0,
        opacity=0.3
    ), secondary_y=True)

    # 2. Main Price Line
    fig.add_trace(go.Scatter(
        x=stock_df.index, 
        y=stock_df['Close'],
        mode='lines',
        name='Price',
        line=dict(color='#00F2C4', width=2),
        fill='tozeroy', 
        fillcolor='rgba(0, 242, 196, 0.05)'
    ), secondary_y=False)

    # 3. News Markers (Conditional Display)
    if show_news_markers and not merged_news.empty:
        custom_hovers = []

        for _, row in merged_news.iterrows():
            source = str(row.get('Sources', 'News')).upper()
            date_str = row['Date_Obj'].strftime('%d %b %Y')
            
            raw_headline = str(row.get('Title', 'No Title'))
            headline = raw_headline[:50] + "..." if len(raw_headline) > 50 else raw_headline
            
            price_str = f"${row.get('Close', 0):,.2f}"
            vol_str = f"{row.get('Volume', 0)/1e6:.1f}M"

            tooltip_txt = (
                f"<b>{source}</b>  <span style='color:#888; font-size:12px;'>({date_str})</span><br>"
                f"<span style='color:#333;'>━━━━━━━━━━━━━━━━━━</span><br>"  
                f"<span style='font-size:15px; font-weight:bold; color:#FFF;'>{headline}</span><br>"
                f"<br>"
                f"💰 Price: <b>{price_str}</b><br>"
                f"📊 Vol: <b>{vol_str}</b><br>"
                f"<span style='color:#333;'>━━━━━━━━━━━━━━━━━━</span><br>"
                f"<span style='color:#FF4B4B; font-size:11px;'>▶ CLICK TO SHOW SOURCE</span>"
            )
            custom_hovers.append(tooltip_txt)

        fig.add_trace(go.Scatter(
            x=merged_news['Date_Obj'], 
            y=merged_news['Close'], 
            mode='markers',
            name='News',
            marker=dict(
                color='#FF4B4B', 
                size=10,          # ขนาดจุด
                line=dict(width=2, color='white'),
                symbol='circle'
            ),
            text=custom_hovers, 
            hoverinfo='text',     
            
            hoverlabel=dict(
                bgcolor="#0F0F0F",     
                bordercolor="#333333",   
                font_size=14,            
                font_family="'Manrope', sans-serif",
                font_color="#E0E0E0",     
                align="left"              
            )
        ), secondary_y=False)

    # --- Layout Settings ---
    dt_all = pd.date_range(start=stock_df.index[0], end=stock_df.index[-1])
    dt_obs = [d.strftime("%Y-%m-%d") for d in stock_df.index]
    dt_breaks = [d.strftime("%Y-%m-%d") for d in dt_all if d.strftime("%Y-%m-%d") not in dt_obs]

    max_vol = stock_df['Volume'].max()
    fig.update_layout(
        height=500,
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        margin=dict(l=20, r=20, t=20, b=20),
        hoverlabel=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", align="left"),
        showlegend=False,
        yaxis=dict(title="Price", showgrid=True, gridcolor='#1f2937', tickprefix="$", side="right"),
        yaxis2=dict(title="", showgrid=False, showticklabels=False, range=[0, max_vol * 4], overlaying="y", side="left"),
        xaxis=dict(rangebreaks=[dict(values=dt_breaks)])
    )

    # --- Chart Display with Interaction ---
    chart_selection = st.plotly_chart(
        fig, 
        use_container_width=True,
        on_select="rerun",  
        selection_mode="points"
    )

    # ---------------------------------------------------------
    # 5. MEDIA PLAYER SECTION
    # ---------------------------------------------------------
    
    st.markdown("---")
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    selected_news_item = None
    
    if show_news_markers and chart_selection and chart_selection.selection["points"]:
        point_idx = chart_selection.selection["points"][0]["point_index"]
        if not merged_news.empty and len(merged_news) > point_idx: 
             selected_news_item = merged_news.iloc[point_idx]
    
    with col_center:
        if selected_news_item is not None:
            st.markdown(f"### 🍿 Media Player")
            with st.container():
                source = str(selected_news_item['Sources']).lower()
                link = str(selected_news_item['Link'])
                name = selected_news_item['Name']
                date = selected_news_item['Date']
                
                st.info(f"**{name}**\n\n📅 {date} | Source: {selected_news_item['Sources']}")

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

    # ---------------------------------------------------------
    # [NEW] 6. AI MARKET SUMMARY SECTION
    # ---------------------------------------------------------
    
    st.subheader("🤖 AI Market Summary & Timeline")
    st.caption("Generate a timeline analysis based on transcripts using Gemini 2.5 Flash")

    col_sum_btn, col_sum_status = st.columns([1, 4])
    
    with col_sum_btn:
        generate_btn = st.button("✨ Generate Summary", type="primary", use_container_width=True)

    if generate_btn:
        if not news_df.empty:
            summary_result = get_gemini_summary(gemini_api_key, filtered_news)
            
            with st.container(border=True):
                st.markdown("### 📝 Timeline & Impact Analysis")
                st.markdown(summary_result)
        else:
            st.warning("No news data available to summarize.")
    