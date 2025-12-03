import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
data_path = BASE_DIR.parent / 'data' / 'YT03042025_CH3.txt'

try:
    with open(data_path, 'r', encoding='utf-8') as f:
        news_text = f.read()
    print(f"Successfully loaded file from: {data_path}")
except FileNotFoundError:
    print(f"Error: The file was not found at expected path: {data_path}")
    print(f"Current working directory when script ran was: {Path.cwd()}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


my_portfolio = "NVDA, TSM, AVGO, PANW, KO, V"

def prompt_template(my_portfolio, news_text):
    prompt = f'''
            # Role & Persona
            You are a Senior Investment Strategist specializing in Thai and Global markets. You are analyzing raw news transcriptions (ASR) which may contain errors.

            # Input Data
            1. **Transcribed News (Thai ASR):**
            """
            {news_text}
            """

            2. **User Portfolio:**
            """
            {my_portfolio}
            """ 

            # Task
            Analyze the news context and determine the impact on the user's portfolio.

            # Instructions
            1.  **Process the Input:** Read the Thai news text. Correct any obvious ASR errors based on financial context (e.g., if it hears "ชีพ", context implies "Chip/Semiconductor").
            2.  **Analyze Impact:** Determine how this specific news affects the stocks in the list (Positive, Negative, Neutral).
            3.  **Output Language:** **WRITE THE RESPONSE IN THAI (ภาษาไทย)** using professional investment terminology.

            # Output Structure

            ### **บทวิเคราะห์: [ตั้งชื่อหัวข้อให้ดึงดูด]**

            #### **1. สรุปสถานการณ์ (The Situation)**
            - Summarize what happened based on the ASR text.
            - Explain the context (Trade war, Policy change, etc.).

            #### **2. สถานะปัจจุบัน (Current Status)**
            - Tone of the news (Aggressive vs. Negotiating).
            - Status (Official vs. Rumor).

            #### **3. ผลกระทบต่อหุ้นในพอร์ต (Portfolio Impact Analysis)**
            - Analyze specific stocks from `{my_portfolio}`.
            - Group them with emojis:
            - 🔴 **กลุ่มผลกระทบเชิงลบ (Negative):** ...
            - 🟢 **กลุ่มได้ประโยชน์/หลุมหลบภัย (Positive/Defensive):** ...
            - ⚪ **กลุ่มผลกระทบจำกัด (Neutral):** ...

            #### **4. ตีความแบบนักลงทุน (Investor Takeaway)**
            - Actionable advice for this portfolio.
            - Key risks or next events to watch.

            ---
            Begin Analysis in Thai:
    '''
    return prompt


# print(prompt_template(my_portfolio=my_portfolio, news_text=news_text))


stock_database = [
    # --- Major U.S. Indices & Other Instruments ---
    {"symbol": "^GSPC",  "name": "S&P 500 Index",                     "type": "Index",  "domain": "spglobal.com",      "market": "Index"},
    {"symbol": "^DJI",   "name": "Dow Jones Industrial Average",      "type": "Index",  "domain": "dowjones.com",       "market": "Index"},
    {"symbol": "^IXIC",  "name": "Nasdaq Composite",                  "type": "Index",  "domain": "nasdaq.com",        "market": "Index"},
    {"symbol": "^NDX",   "name": "Nasdaq-100 Index",                  "type": "Index",  "domain": "nasdaq.com",        "market": "Index"},
    {"symbol": "^VIX",   "name": "CBOE Volatility Index (VIX)",       "type": "Index",  "domain": "cboe.com",           "market": "CBOE"},
    {"symbol": "THB=X",  "name": "USD/THB Exchange Rate",             "type": "FX",     "domain": "finance.yahoo.com", "market": "FX"},
    {"symbol": "BTC-USD","name": "Bitcoin USD",                       "type": "Crypto", "domain": "bitcoin.org",      "market": "Crypto"},

    # --- Top ~100 S&P 500 companies ---
    {"symbol": "NVDA",   "name": "NVIDIA Corporation",                 "type": "Stock",  "domain": "nvidia.com",        "market": "NASDAQ"},
    {"symbol": "AAPL",   "name": "Apple Inc.",                         "type": "Stock",  "domain": "apple.com",         "market": "NASDAQ"},
    {"symbol": "TSLA",   "name": "Tesla, Inc.",                        "type": "Stock",  "domain": "tesla.com",         "market": "NASDAQ"},
    {"symbol": "MSFT",   "name": "Microsoft Corporation",             "type": "Stock",  "domain": "microsoft.com",    "market": "NASDAQ"},
    {"symbol": "META",   "name": "Meta Platforms, Inc.",              "type": "Stock",  "domain": "meta.com",          "market": "NASDAQ"},
    {"symbol": "AMD",    "name": "Advanced Micro Devices, Inc.",      "type": "Stock",  "domain": "amd.com",           "market": "NASDAQ"},
    {"symbol": "AMZN",   "name": "Amazon.com, Inc.",                  "type": "Stock",  "domain": "amazon.com",        "market": "NASDAQ"},
    {"symbol": "NFLX",   "name": "Netflix, Inc.",                     "type": "Stock",  "domain": "netflix.com",      "market": "NASDAQ"},
    {"symbol": "INTC",   "name": "Intel Corporation",                 "type": "Stock",  "domain": "intel.com",         "market": "NASDAQ"},
    {"symbol": "AVGO",  "name": "Broadcom Inc.",                        "type": "Stock", "domain": "broadcom.com",          "market": "NASDAQ"},
    {"symbol": "GOOG",  "name": "Alphabet Inc. Class C",               "type": "Stock", "domain": "abc.xyz",               "market": "NASDAQ"},
    {"symbol": "BRK.B", "name": "Berkshire Hathaway Inc. Class B",     "type": "Stock", "domain": "berkshirehathaway.com",  "market": "NYSE"},
    {"symbol": "LLY",   "name": "Eli Lilly and Company",               "type": "Stock", "domain": "lilly.com",             "market": "NYSE"},
    {"symbol": "WMT",   "name": "Walmart Inc.",                        "type": "Stock", "domain": "walmart.com",           "market": "NYSE"},
    {"symbol": "JPM",   "name": "JPMorgan Chase & Co.",                "type": "Stock", "domain": "jpmorganchase.com",      "market": "NYSE"},
    {"symbol": "V",     "name": "Visa Inc.",                           "type": "Stock", "domain": "visa.com",              "market": "NYSE"},
    {"symbol": "ORCL",  "name": "Oracle Corporation",                  "type": "Stock", "domain": "oracle.com",           "market": "NYSE"},
    {"symbol": "JNJ",   "name": "Johnson & Johnson",                   "type": "Stock", "domain": "jnj.com",               "market": "NYSE"},
    {"symbol": "MA",    "name": "Mastercard Incorporated",             "type": "Stock", "domain": "mastercard.com",       "market": "NYSE"},
    {"symbol": "XOM",   "name": "Exxon Mobil Corporation",             "type": "Stock", "domain": "exxonmobil.com",        "market": "NYSE"},
    {"symbol": "COST",  "name": "Costco Wholesale Corporation",        "type": "Stock", "domain": "costco.com",            "market": "NASDAQ"},
    {"symbol": "ABBV",  "name": "AbbVie Inc.",                         "type": "Stock", "domain": "abbvie.com",            "market": "NYSE"},
    {"symbol": "HD",    "name": "The Home Depot, Inc.",                "type": "Stock", "domain": "homedepot.com",         "market": "NYSE"},
    {"symbol": "BAC",   "name": "Bank of America Corporation",         "type": "Stock", "domain": "bankofamerica.com",     "market": "NYSE"},
    {"symbol": "PG",    "name": "Procter & Gamble Company",            "type": "Stock", "domain": "pg.com",                "market": "NYSE"},
    {"symbol": "GE",    "name": "General Electric Company",            "type": "Stock", "domain": "ge.com",                "market": "NYSE"},
    {"symbol": "KO",    "name": "The Coca-Cola Company",               "type": "Stock", "domain": "coca-cola.com",         "market": "NYSE"},
    {"symbol": "CSCO",  "name": "Cisco Systems, Inc.",                 "type": "Stock", "domain": "cisco.com",             "market": "NASDAQ"},
    {"symbol": "CVX",   "name": "Chevron Corporation",                 "type": "Stock", "domain": "chevron.com",           "market": "NYSE"},
    {"symbol": "UNH",   "name": "UnitedHealth Group Incorporated",     "type": "Stock", "domain": "unitedhealthgroup.com",  "market": "NYSE"},
    {"symbol": "IBM",   "name": "International Business Machines Corp.","type": "Stock", "domain": "ibm.com",                "market": "NYSE"},
    {"symbol": "MS",    "name": "Morgan Stanley",                      "type": "Stock", "domain": "morganstanley.com",     "market": "NYSE"},
    {"symbol": "WFC",   "name": "Wells Fargo & Company",               "type": "Stock", "domain": "wellsfargo.com",        "market": "NYSE"},
    {"symbol": "CAT",   "name": "Caterpillar Inc.",                    "type": "Stock", "domain": "caterpillar.com",       "market": "NYSE"},
    {"symbol": "MU",    "name": "Micron Technology, Inc.",             "type": "Stock", "domain": "micron.com",            "market": "NASDAQ"},
    {"symbol": "MRK",   "name": "Merck & Co., Inc.",                   "type": "Stock", "domain": "merck.com",             "market": "NYSE"},
    {"symbol": "AXP",   "name": "American Express Company",            "type": "Stock", "domain": "americanexpress.com",   "market": "NYSE"},
    {"symbol": "GS",    "name": "The Goldman Sachs Group, Inc.",       "type": "Stock", "domain": "goldmansachs.com",      "market": "NYSE"},
    {"symbol": "PM",    "name": "Philip Morris International Inc.",    "type": "Stock", "domain": "pmi.com",                "market": "NYSE"},
    {"symbol": "RTX",   "name": "RTX Corporation",                     "type": "Stock", "domain": "rtx.com",                "market": "NYSE"},
    {"symbol": "TMUS",  "name": "T-Mobile US, Inc.",                   "type": "Stock", "domain": "t-mobile.com",          "market": "NASDAQ"},
    {"symbol": "ABT",   "name": "Abbott Laboratories",                 "type": "Stock", "domain": "abbott.com",            "market": "NYSE"},
    {"symbol": "MCD",   "name": "McDonald's Corporation",              "type": "Stock", "domain": "mcdonalds.com",         "market": "NYSE"},
    {"symbol": "TMO",   "name": "Thermo Fisher Scientific Inc.",       "type": "Stock", "domain": "thermofisher.com",      "market": "NYSE"},
    {"symbol": "CRM",   "name": "Salesforce, Inc.",                    "type": "Stock", "domain": "salesforce.com",        "market": "NYSE"},
    {"symbol": "PEP",   "name": "PepsiCo, Inc.",                       "type": "Stock", "domain": "pepsico.com",           "market": "NASDAQ"},
    {"symbol": "ISRG",  "name": "Intuitive Surgical, Inc.",            "type": "Stock", "domain": "intuitive.com",         "market": "NASDAQ"},
    {"symbol": "AMAT",  "name": "Applied Materials, Inc.",             "type": "Stock", "domain": "appliedmaterials.com",  "market": "NASDAQ"},
    {"symbol": "LRCX",  "name": "Lam Research Corporation",            "type": "Stock", "domain": "lamresearch.com",       "market": "NASDAQ"},
    {"symbol": "LIN",   "name": "Linde plc",                          "type": "Stock", "domain": "linde.com",             "market": "NYSE"},
    {"symbol": "DIS",   "name": "The Walt Disney Company",            "type": "Stock", "domain": "thewaltdisneycompany.com","market": "NYSE"},
    {"symbol": "AMGN",  "name": "Amgen Inc.",                          "type": "Stock", "domain": "amgen.com",             "market": "NASDAQ"},
    {"symbol": "C",     "name": "Citigroup Inc.",                     "type": "Stock", "domain": "citigroup.com",         "market": "NYSE"},
    {"symbol": "T",     "name": "AT&T Inc.",                          "type": "Stock", "domain": "att.com",               "market": "NYSE"},
    {"symbol": "UBER",  "name": "Uber Technologies, Inc.",            "type": "Stock", "domain": "uber.com",              "market": "NYSE"},
    {"symbol": "QCOM",  "name": "QUALCOMM Incorporated",              "type": "Stock", "domain": "qualcomm.com",          "market": "NASDAQ"},
    {"symbol": "NEE",   "name": "NextEra Energy, Inc.",               "type": "Stock", "domain": "nexteraenergy.com",      "market": "NYSE"},
    {"symbol": "INTU",  "name": "Intuit Inc.",                        "type": "Stock", "domain": "intuit.com",            "market": "NASDAQ"},
    {"symbol": "VZ",    "name": "Verizon Communications Inc.",        "type": "Stock", "domain": "verizon.com",           "market": "NYSE"},
    {"symbol": "APH",   "name": "Amphenol Corporation",               "type": "Stock", "domain": "amphenol.com",          "market": "NYSE"},
    {"symbol": "TJX",   "name": "The TJX Companies, Inc.",            "type": "Stock", "domain": "tjx.com",               "market": "NYSE"},
    {"symbol": "NOW",   "name": "ServiceNow, Inc.",                   "type": "Stock", "domain": "servicenow.com",        "market": "NYSE"},
    {"symbol": "SCHW",  "name": "The Charles Schwab Corporation",     "type": "Stock", "domain": "schwab.com",            "market": "NYSE"},
    {"symbol": "ANET",  "name": "Arista Networks, Inc.",              "type": "Stock", "domain": "arista.com",            "market": "NYSE"},
    {"symbol": "GEV",   "name": "GE Vernova Inc.",                    "type": "Stock", "domain": "gevernova.com",         "market": "NYSE"},
    {"symbol": "BLK",   "name": "BlackRock, Inc.",                    "type": "Stock", "domain": "blackrock.com",         "market": "NYSE"},
    {"symbol": "DHR",   "name": "Danaher Corporation",               "type": "Stock", "domain": "danaher.com",          "market": "NYSE"},
    {"symbol": "BKNG",  "name": "Booking Holdings Inc.",              "type": "Stock", "domain": "bookingholdings.com",   "market": "NASDAQ"},
    {"symbol": "GILD",  "name": "Gilead Sciences, Inc.",              "type": "Stock", "domain": "gilead.com",            "market": "NASDAQ"},
    {"symbol": "ACN",   "name": "Accenture plc",                      "type": "Stock", "domain": "accenture.com",         "market": "NYSE"},
    {"symbol": "KLAC",  "name": "KLA Corporation",                    "type": "Stock", "domain": "kla.com",               "market": "NASDAQ"},
    {"symbol": "TXN",   "name": "Texas Instruments Incorporated",     "type": "Stock", "domain": "ti.com",                "market": "NASDAQ"},
    {"symbol": "SPGI",  "name": "S&P Global Inc.",                    "type": "Stock", "domain": "spglobal.com",          "market": "NYSE"},
    {"symbol": "BSX",   "name": "Boston Scientific Corporation",      "type": "Stock", "domain": "bostonscientific.com",   "market": "NYSE"},
    {"symbol": "PFE",   "name": "Pfizer Inc.",                        "type": "Stock", "domain": "pfizer.com",            "market": "NYSE"},
    {"symbol": "BA",    "name": "The Boeing Company",                 "type": "Stock", "domain": "boeing.com",            "market": "NYSE"},
    {"symbol": "WELL",  "name": "Welltower Inc.",                     "type": "Stock", "domain": "welltower.com",         "market": "NYSE"},
    {"symbol": "SYK",   "name": "Stryker Corporation",               "type": "Stock", "domain": "stryker.com",           "market": "NYSE"},
    {"symbol": "COF",   "name": "Capital One Financial Corporation",  "type": "Stock", "domain": "capitalone.com",        "market": "NYSE"},
    {"symbol": "UNP",   "name": "Union Pacific Corporation",          "type": "Stock", "domain": "up.com",                "market": "NYSE"},
    {"symbol": "LOW",   "name": "Lowe's Companies, Inc.",             "type": "Stock", "domain": "lowes.com",             "market": "NYSE"},
    {"symbol": "MDT",   "name": "Medtronic plc",                      "type": "Stock", "domain": "medtronic.com",         "market": "NYSE"},
    {"symbol": "ETN",   "name": "Eaton Corporation plc",             "type": "Stock", "domain": "eaton.com",             "market": "NYSE"},
    {"symbol": "PGR",   "name": "The Progressive Corporation",        "type": "Stock", "domain": "progressive.com",       "market": "NYSE"},
    {"symbol": "ADBE",  "name": "Adobe Inc.",                         "type": "Stock", "domain": "adobe.com",             "market": "NASDAQ"},
    {"symbol": "PANW",  "name": "Palo Alto Networks, Inc.",           "type": "Stock", "domain": "paloaltonetworks.com",  "market": "NASDAQ"},
    {"symbol": "ADI",   "name": "Analog Devices, Inc.",               "type": "Stock", "domain": "analog.com",            "market": "NASDAQ"},
    {"symbol": "CRWD",  "name": "CrowdStrike Holdings, Inc.",         "type": "Stock", "domain": "crowdstrike.com",       "market": "NASDAQ"},
    {"symbol": "DE",    "name": "Deere & Company",                    "type": "Stock", "domain": "deere.com",             "market": "NYSE"},
    {"symbol": "HON",   "name": "Honeywell International Inc.",       "type": "Stock", "domain": "honeywell.com",         "market": "NYSE"},
    {"symbol": "PLD",   "name": "Prologis, Inc.",                     "type": "Stock", "domain": "prologis.com",          "market": "NYSE"},
    {"symbol": "CB",    "name": "Chubb Limited",                      "type": "Stock", "domain": "chubb.com",             "market": "NYSE"},
    {"symbol": "HCA",   "name": "HCA Healthcare, Inc.",               "type": "Stock", "domain": "hcahospitals.com",      "market": "NYSE"},
    {"symbol": "HOOD",  "name": "Robinhood Markets, Inc.",            "type": "Stock", "domain": "robinhood.com",         "market": "NASDAQ"},
    {"symbol": "CEG",   "name": "Constellation Energy Corporation",   "type": "Stock", "domain": "constellation.com",      "market": "NYSE"},
    {"symbol": "BX",    "name": "Blackstone Inc.",                    "type": "Stock", "domain": "blackstone.com",        "market": "NYSE"},
    {"symbol": "VRTX",  "name": "Vertex Pharmaceuticals Incorporated","type": "Stock", "domain": "vertex.com",            "market": "NASDAQ"},
]
