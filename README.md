# ⚡ Electricity Demand Forecasting with SARIMA

## 📌 Project Overview

This project provides a **complete end-to-end pipeline for forecasting electricity demand** using the **SARIMA (Seasonal ARIMA) model**. Designed for real-world datasets, the solution automates **data acquisition, preprocessing, forecasting, and output export**, facilitating practical demand planning and analysis.

---

## 💡 Key Features

✅ **Automated Data Collection**  
- Downloads hourly electricity demand data directly from the **Australian Energy Market Operator (AEMO)** based on specified date ranges.

✅ **Data Processing & Harmonization**  
- Combines multiple CSV files chronologically.  
- Resamples to hourly data, interpolates missing values, and aligns time zones.

✅ **Advanced Forecasting**  
- Implements SARIMA with **hyperparameter tuning based on AIC** for optimal model selection.  
- Provides interactive Tkinter GUI for forecast horizon selection (e.g., 1 week, 1 month, 3 months).

✅ **Multi-format Output**  
- Exports forecast results to **Excel (.xlsx)**, **CSV**, and **PNG images** for analysis and reporting.

✅ **Full Pipeline Automation**  
- From data download to final forecast report generation.

---

## 📁 Directory Structure

project-root/
├── MainStart.py # Orchestrates the full pipeline
├── DataDownload.py # Downloads AEMO datasets based on date range
├── DataCombine.py # Combines and sorts CSV files chronologically
├── DataFilterHour.py # Resamples data to hourly and interpolates missing values
├── Sarimamodel5.py # Applies SARIMA, shows GUI, exports forecast
├── Contents/ # LaTeX chapters for documentation
├── Documents/ # Bibliography and references
├── Images/ # PNG and diagram assets
└── .env # Configuration file for region and time span

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

1. **Clone the repository and install dependencies:**

   ```bash
   pip install pandas numpy statsmodels matplotlib openpyxl python-dotenv pytz tk
# Create a .env file with the following content:
REGION=NSW1
START_DATE=2020-01-01
END_DATE=2024-12-31

# Run the project:
python MainStart.py
# 📈 Results
Forecast outputs are saved as:

forecast_output.xlsx – Excel file with forecast data

forecast_output.csv – CSV file with forecast data

forecast_plot.png – Forecast graph with confidence intervals

