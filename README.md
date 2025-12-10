# Analyzing Trump Tariff Impacts on Equity Portfolio

A data-driven dashboard built with **Streamlit** to analyze and simulate the potential impacts of trade tariffs and policy changes under the Trump administration on equity portfolios.

## 📊 Project Overview

This tool allows users to:
- Monitor portfolio performance in real-time.
- Analyze the correlation between tariff news/policies and specific stock sectors.
- Visualize potential risks and opportunities based on historical and projected data.

## 📋 Prerequisites

- **Python** (version 3.10 or higher)
- **uv** (An extremely fast Python package installer and resolver)
  - Installation: `pip install uv`

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KorNxHaidar/Analyzing-Trump-Tariff-Impacts-on-Equity-Portfolio.git
   cd Analyzing-Trump-Tariff-Impacts-on-Equity-Portfolio
    ```

2.  **Install Dependencies**

    This project uses `uv` for dependency management. Run the following command to sync the environment:
    ```bash
    uv sync
    ```

## 📂 Data Setup (Important)

Due to file size and security reasons, data files are not included in the git repository. Please download and place them manually as described below:

### 1\. Configuration File (Data\_Sources.csv)

  * **Download Link:** [Google Sheets - Data Sources](https://docs.google.com/spreadsheets/d/1OHFSwLoM3LqsP4xV8lekxjq_90lc_Su_rs45J0AT1_g/edit?usp=sharing)

  * **Instructions:**

    1.  Open the link above.
    2.  Go to **File** \> **Download** \> **Comma Separated Values (.csv)**.
    3.  Rename the downloaded file to `Data_Sources.csv`.
    4.  Move the file into the `src/` folder.

    **Required Structure:**

    ```text
    stock_analysis/
    └── src/
        └── Data_Sources.csv
    ```

### 2\. Data Folder

  * **Download Link:** [Google Drive - Data Folder](https://drive.google.com/drive/folders/1fGn-gGTraldVv9bmtlcculPsdwBq30-r?usp=sharing)

  * **Instructions:**

    1.  Download all files from the link.
    2.  Place all downloaded files inside the `data/` folder at the project root.

    **Required Structure:**

    ```text
    stock_analysis/
    └── data/
        ├── (downloaded files)
        └── ...
    ```

## ⚙️ Environment Variables (.env)

If the project requires API keys, create a `.env` file in the root directory and add your configurations there.
```bash
GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'
```
## ▶️ Run Application

Run the application using the following command:

```bash
# cd .\src\
streamlit run app.py
```
