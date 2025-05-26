## @file Sarimamodel5.py
#  @brief SARIMA forecasting pipeline for electricity demand.
#
#  This script loads hourly electricity demand data, fits a SARIMA model,
#  and forecasts future values using user-specified forecast windows.
#  It includes GUI input, visualization, and Excel export with error handling.
#
#  @author Fedor
#  @date 2025-04-20

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import os
import sys
import tkinter as tk
import traceback

##
# @brief Launches a Tkinter GUI to request forecast duration from the user.
#
# Allows the user to select a duration in weeks or months via an interactive slider.
# Falls back to a default of 1 week if the GUI fails.
#
# @return int Number of hours to forecast (e.g., 168 for 1 week)
def get_forecast_steps():
    def update_scale(*args):
        unit = unit_var.get()
        if unit == "Weeks":
            scale.config(from_=1, to=4, label='Weeks (1–4)')
        elif unit == "Months":
            scale.config(from_=1, to=12, label='Months (1–12)')

    def on_select():
        unit = unit_var.get()
        value = scale.get()
        if unit == "Weeks":
            steps = value * 7 * 24
        elif unit == "Months":
            steps = value * 30 * 24
        else:
            steps = 7 * 24
        root.steps = steps
        root.destroy()

    try:
        root = tk.Tk()
        root.title("Forecast Duration")
        root.geometry("320x220")
        root.resizable(False, False)

        tk.Label(root, text="Select Forecast Period").pack(pady=10)

        unit_var = tk.StringVar(value="Weeks")
        unit_menu = tk.OptionMenu(root, unit_var, "Weeks", "Months")
        unit_menu.pack()

        scale = tk.Scale(root, from_=1, to=4, orient='horizontal', label='Weeks (1–4)')
        scale.pack(pady=10)

        unit_var.trace_add("write", update_scale)
        tk.Button(root, text="Confirm", command=on_select).pack(pady=10)

        root.mainloop()
        return getattr(root, 'steps', 7 * 24)
    except Exception as e:
        print("Error during GUI forecast configuration.")
        traceback.print_exc()
        return 7 * 24

##
# @brief Executes SARIMA-based forecasting on electricity demand data.
#
# Performs the following steps:
# - Loads the preprocessed dataset
# - Checks for stationarity using the Augmented Dickey-Fuller test
# - Fits a SARIMA model with pre-selected parameters
# - Gets forecast length via GUI
# - Simulates forecasts and plots results
# - Saves output to both Excel and PNG
#
# @param df Unused placeholder to maintain compatibility (can be extended)
# @return None
def run_sarima_forecast(df):
    try:
        print("Step 1: Loading dataset...")
        df = pd.read_csv("FiltredDataset/PRICE_AND_DEMAND_2024_HOURLY_NSW1.csv", parse_dates=True, index_col='SETTLEMENTDATE')
        demand_series = df['TOTALDEMAND'].asfreq('h')

        print("Step 2: Running ADF stationarity test...")
        adf_result = adfuller(demand_series.dropna())
        print(f"ADF Statistic: {adf_result[0]}")
        print(f"p-value: {adf_result[1]}")
        if adf_result[1] >= 0.05:
            print("Note: The series may be non-stationary. Differencing may be needed.")

        print("Step 3: Fitting SARIMA model...")
        model = SARIMAX(demand_series,
                        order=(2, 0, 2),
                        seasonal_order=(2, 0, 2, 24),
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        results = model.fit(disp=False)
        print("Model fitting complete.")
        print(results.summary())

        print("Step 4: Getting forecast range from user...")
        forecast_steps = get_forecast_steps()
        print(f"Forecasting {forecast_steps} hours ahead ({forecast_steps // 24} days).")

        forecast_mean = results.get_forecast(steps=forecast_steps).predicted_mean
        forecast_simulated = results.simulate(nsimulations=forecast_steps, anchor='end')

        print("Step 5: Plotting forecast results...")
        plt.figure(figsize=(15, 5))
        plt.plot(demand_series[-24 * 7:], label='Observed (last 7 days)', color='blue')
        plt.plot(forecast_mean, label='Forecast Trend', color='orange')
        plt.plot(forecast_simulated, label='Forecast Fluctuations', color='green', alpha=0.7)
        plt.title('SARIMA Forecast of Electricity Demand')
        plt.xlabel('Date')
        plt.ylabel('Demand (MW)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        plot_path = "CodeDataVisualisation/FORECAST_PLOT_2025_DYNAMIC.png"
        os.makedirs(os.path.dirname(plot_path), exist_ok=True)
        plt.savefig(plot_path)
        print(f"Plot saved to: {plot_path}")
        plt.show()

        print("Step 6: Saving forecast data to Excel...")
        forecast_df = pd.DataFrame({
            'datetime': forecast_mean.index,
            'forecast_demand_trend': forecast_mean.values,
            'forecast_demand_fluctuations': forecast_simulated.values
        })

        excel_path = "CodeDataVisualisation/FORECAST_DEMAND_2025_DYNAMIC.xlsx"
        os.makedirs(os.path.dirname(excel_path), exist_ok=True)

        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            forecast_df.to_excel(writer, index=False, sheet_name='Forecast')
            worksheet = writer.sheets['Forecast']
            for column_cells in worksheet.columns:
                max_length = max(len(str(cell.value)) for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = max_length + 2

        print(f"Forecast data saved to: {excel_path}")

    except FileNotFoundError:
        print("ERROR: Dataset file not found. Check the input path.")
        traceback.print_exc()
    except Exception:
        print("ERROR: An unexpected error occurred during the SARIMA forecast process.")
        traceback.print_exc()

##
# @brief Entry point when running the script directly.
if __name__ == "__main__":
    run_sarima_forecast(None)