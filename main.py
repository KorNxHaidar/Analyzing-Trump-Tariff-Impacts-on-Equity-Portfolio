import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

script_dir = Path(__file__).resolve().parent
file_path = script_dir / "data" / "YT03042025_CH3.txt"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        news_text = f.read()
    print(f"Successfully loaded file from: {file_path}")
except FileNotFoundError:
    print(f"Error: The file was not found at expected path: {file_path}")
    print(f"Current working directory when script ran was: {Path.cwd()}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

my_portfolio = ["NVDA", "TSM", "AVGO", "PANW", "KO", "V"]

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

client = genai.Client(api_key=GOOGLE_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[prompt],
    config={
            "temperature": 0.7,
    }
)

print(response.text)
print(response.usage_metadata)