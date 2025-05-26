# CodeDataPreparation/DataDownload.py
# author Sudhanshu
##
# @file DataDownload.py
# @brief Downloads electricity price and demand data from AEMO using configuration from a .env file.
#
# This module retrieves hourly or daily datasets for a given region and date range
# directly from the Australian Energy Market Operator (AEMO) and logs the results.
# Requires a configured .env file containing REGION, START_MONTH, BASE_URL, etc.
#
# @author Sudhanshu

import os
import requests
import logging
import sys
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

##
# @brief Downloads energy price and demand CSV files from a remote AEMO server.
#
# Uses environment variables to determine the region, date range, and URL path.
# Automatically logs download status and stores files locally in a defined folder.
#
# Expected environment variables in `.env`:
# - REGION: e.g., "NSW1"
# - START_MONTH: e.g., "202301"
# - END_MONTH: Optional; defaults to START_MONTH
# - MODE: "H" (hourly by month range) or "D" (daily by single file)
# - BASE_URL: Base URL for downloading AEMO CSV files
# - LOG_FOLDER: Optional log output directory
# - DOWNLOAD_FOLDER: Optional local folder to store downloads
def download_energy_data():
    # --- Load environment variables from .env file ---
    load_dotenv()

    region = os.getenv('REGION')
    start_month = os.getenv('START_MONTH')
    end_month = os.getenv('END_MONTH', start_month)
    mode = os.getenv('MODE', 'H').upper()
    base_url = os.getenv('BASE_URL')

    if not region or not start_month or not base_url:
        print("ERROR: Missing required environment variables.")
        return

    log_folder = os.getenv('LOG_FOLDER', './logs/')
    download_folder = os.getenv('DOWNLOAD_FOLDER', './DataSetOrigin')
    os.makedirs(log_folder, exist_ok=True)
    os.makedirs(download_folder, exist_ok=True)

    # Set up logging system to both file and console
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(os.path.join(log_folder, 'download.log'), mode='a')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    ##
    # @brief Downloads a specific month of CSV data.
    # @param year_month A string in YYYYMM format, e.g., "202401"
    def download_file(year_month):
        filename = f"PRICE_AND_DEMAND_{year_month}_{region}.csv"
        file_path = os.path.join(download_folder, filename)
        url = f"{base_url}{filename}"

        try:
            with requests.get(url, stream=True, headers={"User-Agent": "Mozilla/5.0"}) as r:
                r.raise_for_status()
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            logger.info(f"Downloaded: {filename}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download {year_month}: {e}")

    ##
    # @brief Generates a list of months between a start and end month.
    # @param start Start month as string in YYYYMM format
    # @param end End month as string in YYYYMM format
    # @return Yields each month in YYYYMM format
    def month_range(start, end):
        current = datetime.strptime(start, "%Y%m")
        end_date = datetime.strptime(end, "%Y%m")
        while current <= end_date:
            yield current.strftime("%Y%m")
            current += relativedelta(months=1)

    # Perform downloads based on mode
    if mode == "H":
        for ym in month_range(start_month, end_month):
            download_file(ym)
    elif mode == "D":
        download_file(start_month)
    else:
        logger.error("Invalid mode in config. Use 'H' or 'D'.")