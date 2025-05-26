
# Data Downloader

This Python script allows you to download price and demand data from the Australian Energy Market Operator (AEMO) website.

It supports two modes:

- **Historical Mode (H)**: Downloads a range of files for consecutive months.
- **Daily Mode (D)**: Downloads a single file for a specified month.

The script supports **environment variables** using a `.env` file to store configuration settings, which makes it portable and easy to use across different environments.

---

## Prerequisites

To run this script, you need the following:

1. **Python 3.x** installed on your system.
2. **Required Python packages**: `requests`, `python-dotenv`, and `python-dateutil`.

Create new python project in your favorite directory:

```bash
python -m venv data-download
```

Activate virtual environment
```bash
cd data-download
Scripts\activate
```

You can install the required packages using the following command:

```bash
pip install -r requirements.txt
```


---

## Setup

### 1. Create a `.env` File

Create a `.env` file in the root directory of the project. The `.env` file should contain the following configuration variables:

```env
# .env file

REGION=NSW1
START_MONTH=202501
END_MONTH=202502
MODE=H  # H = Historical, D = Daily
BASE_URL=https://aemo.com.au/aemo/data/nem/priceanddemand/

# Optional: specify log and download directories
LOG_FOLDER=C:/MyDownloads/logs/
DOWNLOAD_FOLDER=C:/MyDownloads/downloads/
```

- **REGION**: The region code for the data you want to download (e.g., `NSW1`).
- **START_MONTH**: The start month in `YYYYMM` format (e.g., `202501`).
- **END_MONTH**: The end month in `YYYYMM` format (only used in **Historical Mode**).
- **MODE**: Set to `H` for **Historical Mode** or `D` for **Daily Mode**.
- **BASE_URL**: The base URL for the AEMO price and demand data files.
- **LOG_FOLDER**: Directory where log files will be saved.
- **DOWNLOAD_FOLDER**: Directory where downloaded files will be stored.

### 2. Create the Required Directories

Ensure the directories specified in your `.env` file for logs and downloads exist, or the script will create them automatically.

---

## Usage

### Running the Script

There are two modes you can run the script in, depending on the value of `MODE` in the `.env` file:

### **1. Historical Mode (H)**

When `MODE` is set to `H`, the script will download data for a range of months, from `START_MONTH` to `END_MONTH`.

#### Example:

To download data from **January 2025** to **February 2025**, set the `.env` file as follows:

```env
MODE=H
START_MONTH=202501
END_MONTH=202502
```

To run the script, execute:

```bash
python app.py
```

The script will download files for each month in the range (`202501`, `202502`), saving them in the directory specified in `DOWNLOAD_FOLDER`.

### **2. Daily Mode (D)**

When `MODE` is set to `D`, the script will download a single file for the given month (specified by `START_MONTH`).

#### Example:

To download data for **January 2025**, set the `.env` file as follows:

```env
MODE=D
START_MONTH=202501
```

To run the script, execute:

```bash
python app.py
```

This will download the file for the specified month (`202501`), saving it in the directory specified in `DOWNLOAD_FOLDER`.

---

## Scheduling the Script with Task Scheduler

If you want to automate the script to run periodically (e.g., daily or weekly), you can use **Windows Task Scheduler** to schedule it.

### Steps to Set Up Task Scheduler:

1. **Create a batch file** (`run_download.bat`) that runs the Python script. Here's an example:

   ```batch
   @echo off
   REM Change to the folder where the script and .env file are located python app.py
   cd C:\Path\To\Your\Script
   python app.py
   ```

2. **Set up Task Scheduler**:
   - Open **Task Scheduler** and click **Create Task**.
   - Under the **Triggers** tab, set a trigger (e.g., daily at a specific time).
   - Under the **Actions** tab, select **Start a Program** and point it to the `.bat` file you created.

This will ensure that the script runs automatically at your specified time and downloads the data.

---

## Log Files

The script will generate a log file (`download.log`) that contains detailed information about the download process, including progress and any errors encountered.

Log files are saved in the directory specified by `LOG_FOLDER` in the `.env` file.

---

## Notes

- Ensure that your system has proper internet access to download data from the AEMO website.
- The script checks the response status (`requests.raise_for_status()`) and logs any errors encountered during the download process.
