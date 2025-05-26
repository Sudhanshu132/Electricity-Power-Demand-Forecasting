##
# @file DataCombine.py
# @brief Combines multiple CSV files into a single dataset for electricity price and demand.
#
# This script searches for CSV files that match a specific pattern, loads them,
# merges them into one DataFrame, converts timestamps, and saves the result to disk.
#
# The combined dataset is saved to the "FiltredDataset" folder for further analysis.
#
# @author Fedor
# @date 2025-04-20
##

import pandas as pd
import glob
import os
import traceback

##
# @brief Combines electricity demand and price data from multiple monthly CSV files.
#
# This function performs the following steps:
# - Searches for all CSV files matching a specific naming pattern.
# - Loads and concatenates them into a single Pandas DataFrame.
# - Converts the 'SETTLEMENTDATE' column to datetime format.
# - Saves the combined dataset to a new CSV file.
#
# @return Pandas DataFrame containing the combined dataset, or None if an error occurs.
##
def combine_data():
    try:
        print("Step 1: Locating input CSV files...")
        input_pattern = "DataSetOrigin/PRICE_AND_DEMAND_2024*_NSW1.csv"
        csv_files = sorted(glob.glob(input_pattern))

        if not csv_files:
            raise FileNotFoundError(f"No files matched pattern: {input_pattern}")

        print(f"Found {len(csv_files)} CSV files to combine.")

        df_list = []
        for file in csv_files:
            try:
                print(f"Loading file: {file}")
                df = pd.read_csv(file)
                df_list.append(df)
            except Exception as e:
                print(f"Warning: Failed to read {file}. Skipping.")
                traceback.print_exc()

        if not df_list:
            raise ValueError("No valid CSV files could be loaded.")

        print("Step 2: Concatenating data...")
        combined_df = pd.concat(df_list, ignore_index=True)

        if 'SETTLEMENTDATE' not in combined_df.columns:
            raise KeyError("Missing required column 'SETTLEMENTDATE' in combined data.")

        print("Step 3: Converting 'SETTLEMENTDATE' to datetime...")
        combined_df['SETTLEMENTDATE'] = pd.to_datetime(combined_df['SETTLEMENTDATE'], errors='coerce')

        if combined_df['SETTLEMENTDATE'].isnull().any():
            print("Warning: Null values detected in 'SETTLEMENTDATE' after conversion.")

        output_folder = "FiltredDataset"
        output_file = os.path.join(output_folder, "PRICE_AND_DEMAND_2024_ALL_NSW1.csv")

        print("Step 4: Saving combined dataset to output CSV...")
        os.makedirs(output_folder, exist_ok=True)
        combined_df.to_csv(output_file, index=False)
        print(f"Combined dataset successfully saved to: {output_file}")

        return combined_df

    except Exception as e:
        print("Error occurred during data combination.")
        traceback.print_exc()
        return None