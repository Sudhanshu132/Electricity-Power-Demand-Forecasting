import os
import requests
import logging
import sys
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

# --- Load environment variables from .env file ---
load_dotenv()  # This loads the .env file into environment variables

# Get values from environment variables
region = os.getenv('REGION')
start_month = os.getenv('START_MONTH')
end_month = os.getenv('END_MONTH', start_month)  # Default to start_month if end_month is not set
mode = os.getenv('MODE', 'H').upper()
base_url = os.getenv('BASE_URL')

log_folder = os.getenv('LOG_FOLDER', './logs/')  # Default to './logs/' if not set
download_folder = os.getenv('DOWNLOAD_FOLDER', '../DataSetOrigin')  # Default to './downloads/' if not set

# Ensure folders exist
os.makedirs(log_folder, exist_ok=True)
os.makedirs(download_folder, exist_ok=True)

# --- Set up logging ---
log_filename = os.path.join(log_folder, 'download.log')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_filename, mode='a')
file_handler.setFormatter(logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# --- Functions for downloading files ---
def download_file(year_month):
    filename = f"PRICE_AND_DEMAND_{year_month}_{region}.csv"
    file_path = os.path.join(download_folder, filename)
    url = f"{base_url}{filename}"

    try:
        with requests.get(url, stream=True, headers={"User-Agent": "Mozilla/5.0"}) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('Content-Length', 0))
            downloaded = 0
            chunk_size = 8192  # 8 KB

            logger.info(f"Starting download: {filename} ({total_size / (1024**2):.2f} MB)")

            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            percent = (downloaded / total_size) * 100
                            logger.info(f"Progress: {downloaded / (1024**2):.2f} MB ({percent:.2f}%)")

            logger.info(f"Download completed: {filename}")
            print(f"Downloaded successfully: {filename}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Download failed for {year_month}: {e}")
        print(f"Error downloading {year_month}: {e}")

# --- Main logic ---
def month_range(start, end):
    """Generate YYYYMM strings between start and end (inclusive)."""
    current = datetime.strptime(start, "%Y%m")
    end_date = datetime.strptime(end, "%Y%m")
    dates = []
    while current <= end_date:
        dates.append(current.strftime("%Y%m"))
        current += relativedelta(months=1)
    return dates

if mode == "H":
    for ym in month_range(start_month, end_month):
        download_file(ym)
elif mode == "D":
    download_file(start_month)
else:
    logger.error("Invalid mode in config. Use 'H' for historical or 'D' for daily.")
