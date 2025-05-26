##
# @file Sarimamodel2.py
# @brief SARIMA model implementation for electricity demand forecasting.
#
# This script defines a function to load hourly demand data, check for stationarity,
# fit a SARIMA model, forecast future demand, and save the forecast results to a CSV.
#
# The forecast horizon is set to one month (approximately 730 hours).
# Visual output and statistical summaries are also generated.
#
# @author Fedor
# @date 2025-04-20
##

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import os


##
# @brief Runs the SARIMA forecasting pipeline on hourly electricity demand data.
#
# This function performs the following steps:
# - Loads and processes demand data
# - Tests for stationarity using the Augmented Dickey-Fuller (ADF) test
# - Fits a SARIMA model to the time series
# - Forecasts demand for the next month (~730 hours)
# - Visualizes and saves the forecast results
#
# @param df A Pandas DataFrame, expected to contain the 'TOTALDEMAND' column.
#           Although provided, the function re-loads data from a fixed CSV path.
#
# @return None
##
def run_sarima_forecast(df):
    # Re-load data from the filtered dataset to ensure consistency
    print("Loading dataset...")
    df = pd.read_csv("FiltredDataset/PRICE_AND_DEMAND_2024_HOURLY_NSW1.csv", parse_dates=True,
                     index_col='SETTLEMENTDATE')

    # Extract and re-sample demand series to ensure hourly frequency
    demand_series = df['TOTALDEMAND'].asfreq('h')

    # Step 1: Check stationarity
    print("Performing ADF test...")
    adf_result = adfuller(demand_series.dropna())
    print("ADF Statistic:", adf_result[0])
    print("p-value:", adf_result[1])

    # Step 2: Fit SARIMA model
    print("Fitting SARIMA model...")
    model = SARIMAX(demand_series,
                    order=(2, 0, 2),
                    seasonal_order=(2, 0, 2, 24),
                    enforce_stationarity=False,
                    enforce_invertibility=False)

    results = model.fit(disp=False)
    print(results.summary())

    # Step 3: Forecast
    forecast_steps = 730  # Approx. one month of hourly data
    forecast = results.get_forecast(steps=forecast_steps)
    forecast_mean = forecast.predicted_mean
    forecast_ci = forecast.conf_int()

    # Step 4: Visualization
    plt.figure(figsize=(15, 5))
    plt.plot(demand_series[-24 * 7:], label='Observed (last 7 days)', color='blue')
    plt.plot(forecast_mean, label='Forecast (next month)', color='orange')
    plt.fill_between(forecast_ci.index,
                     forecast_ci.iloc[:, 0],
                     forecast_ci.iloc[:, 1], color='orange', alpha=0.2)
    plt.ylim(0, demand_series.max() * 2)
    plt.title('SARIMA Forecast of Hourly Electricity Demand (Next Month)')
    plt.xlabel('Date')
    plt.ylabel('Demand (MW)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Step 5: Save forecast to CSV
    forecast_df = pd.DataFrame({
        'datetime': forecast_mean.index,
        'forecast_demand': forecast_mean,
        'lower_ci': forecast_ci.iloc[:, 0],
        'upper_ci': forecast_ci.iloc[:, 1]
    })

    output_path = "FiltredDataset/FORECAST_DEMAND_2025_MONTH1.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    forecast_df.to_csv(output_path, index=False)
    print(f"✅ Forecast saved to: {output_path}")