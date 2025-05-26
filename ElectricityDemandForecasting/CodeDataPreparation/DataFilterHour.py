##
# @file DataFilterHour.py
# @brief Filters electricity demand and price data to hourly resolution.
#
# This script takes a DataFrame with timestamped electricity data,
# resamples it to an hourly frequency, and exports it to a CSV file
# for further forecasting or analysis.
#
# Includes structured error handling and informative console output.
#
# @author Fedor
# @date 2025-04-20
##

import pandas as pd
import matplotlib.pyplot as plt
import traceback
import os

##
# @brief Resamples electricity data to an hourly frequency.
#
# This function takes a Pandas DataFrame with minute-level or irregular time intervals,
# sets the 'SETTLEMENTDATE' column as the index, and computes the hourly mean
# of 'TOTALDEMAND' and 'RRP' values. The resulting dataset is saved as a CSV file.
#
# @param df The input Pandas DataFrame containing electricity data with a 'SETTLEMENTDATE' column.
# @return A new DataFrame with hourly resampled data, or None if an error occurs.
##
def filter_data_by_hour(df):
    try:
        print("Step 1: Validating input data...")
        required_columns = {'SETTLEMENTDATE', 'TOTALDEMAND', 'RRP'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Missing required columns: {required_columns - set(df.columns)}")

        print("Step 2: Converting 'SETTLEMENTDATE' to datetime format...")
        df['SETTLEMENTDATE'] = pd.to_datetime(df['SETTLEMENTDATE'], errors='coerce')
        if df['SETTLEMENTDATE'].isnull().any():
            print("Warning: Null values detected in 'SETTLEMENTDATE' after conversion.")

        print("Step 3: Setting datetime index and resampling to hourly frequency...")
        df.set_index('SETTLEMENTDATE', inplace=True)
        hourly_df = df[['TOTALDEMAND', 'RRP']].resample('H').mean()

        print("Step 4: Saving resampled data to CSV file...")
        output_path = "FiltredDataset/PRICE_AND_DEMAND_2024_HOURLY_NSW1.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        hourly_df.to_csv(output_path)
        print(f"Resampled data successfully saved to: {output_path}")

        return hourly_df

    except Exception as e:
        print("Error occurred during hourly data resampling.")
        traceback.print_exc()
        return None