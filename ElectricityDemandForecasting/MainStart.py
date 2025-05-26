##
# @file main.py
# @brief Main pipeline script for time series energy demand forecasting.
#
# This script performs a complete pipeline:
# - Combines raw data files
# - Filters data to hourly resolution
# - Applies SARIMA model to forecast future demand
#
# It uses modular components from:
# - CodeDataPreparation: DataCombine and DataFilterHour
# - CodeTimeForecast: Sarimamodel2
#
# @author Fedor, Sudhanshu
# @date 2025-04-20
##
from General.requirements import install_requirements
# === Data Acquisition ===

## @brief Downloads electricity demand data via AEMO API.
from CodeDataPreparation.DataDownload import download_energy_data  # ← NEW LINE

# === Data Merging ===

## @brief Combines multiple raw CSV files into a unified DataFrame.
from CodeDataPreparation.DataCombine import combine_data

# === Data Cleaning ===

## @brief Filters combined data to include valid hourly entries only.
from CodeDataPreparation.DataFilterHour import filter_data_by_hour

# === Forecasting ===

## @brief Runs SARIMA-based forecasting on filtered data.
from CodeTimeForecast.Sarimamodel5 import run_sarima_forecast

# === Visualization ===

## @brief Plots historical electricity demand for December as a reference.
from CodeDataVisualisation.demand_dec import plot_december_demand
## \file MainStart.py
#  \brief Main entry point for the Power Demand Forecasting pipeline.
#
#  This script executes the full forecasting process including data
#  acquisition, preprocessing, visualization, and prediction using SARIMA.

def main():
    """
    @brief Executes the forecasting pipeline in sequential steps.

    This function coordinates the entire process:
    - Downloading data from the AEMO portal
    - Merging raw CSV datasets
    - Visualizing historical demand
    - Filtering the time series
    - Running SARIMA forecasting
    """

    print(" Libraries updates...Wait till complete")
    # @step Downloads the last 12 months of demand data from the AEMO API.
    install_requirements()

    print("Step 0: Downloading data...")
    # @step Downloads the last 12 months of demand data from the AEMO API.
    download_energy_data()

    print("Step 1: Combining data...")
    # @step Merges all downloaded datasets into a single DataFrame.
    combined_data = combine_data()

    print("Step 2: Previous month data ...")
    # @step Displays a graph of electricity demand for the previous month (December).
    plot_december_demand()

    print("Step 3: Filtering data...")
    # @step Filters out zero or irrelevant hourly entries from the combined dataset.
    filtered_data = filter_data_by_hour(combined_data)

    print("Step 4: Running SARIMA model...")
    # @step Applies a seasonal SARIMA model to generate a forecast based on user-defined horizon.
    run_sarima_forecast(filtered_data)

    print("Pipeline complete.")

if __name__ == "__main__":
    main()