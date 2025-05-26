##
# @file Sarimamodel4.py
# @brief SARIMA model implementation for electricity demand forecasting.
#
# This script loads hourly energy demand data, checks for stationarity,
# fits a SARIMA model, forecasts future demand, visualizes the forecast,
# and saves forecast data to CSV for further analysis or visualization.
#
# @details
# Steps performed:
# - Load and process demand data
# - Check stationarity with ADF test
# - Fit SARIMA model
# - Forecast future demand
# - Simulate realistic fluctuations
# - Plot observed vs forecasted demand
# - Save forecast results
#
# About ADF Test (Augmented Dickey-Fuller):
# - The ADF test checks if a time series is stationary (constant mean and variance over time).
# - Test Output:
#     - ADF Statistic: A negative value; the more negative, the stronger the evidence of stationarity.
#     - p-value: If p-value < 0.05, we reject the null hypothesis and conclude that the series is stationary.
# - Example:
#     - ADF Statistic: -7.54
#     - p-value: 3.39e-11
#     - Interpretation: Very strong evidence that the demand series is stationary (good for modeling).
#
# @author Fedor
# @date 2025-04-20
##

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import os

##
# @brief Runs the SARIMA forecasting pipeline on hourly electricity demand data.
#
# This function performs:
# - Load dataset
# - Test stationarity
# - Fit SARIMA model
# - Forecast and simulate future demand
# - Visualize and save results
#
# @param df A Pandas DataFrame (placeholder), the function internally reloads the dataset.
# @return None
##
def run_sarima_forecast(df):
    # Load the dataset
    print("Loading dataset...")
    df = pd.read_csv("FiltredDataset/PRICE_AND_DEMAND_2024_HOURLY_NSW1.csv", parse_dates=True,
                     index_col='SETTLEMENTDATE')

    # Extract the demand series with hourly frequency
    demand_series = df['TOTALDEMAND'].asfreq('h')

    # Step 1: Check stationarity
    print("Performing ADF test...")
    adf_result = adfuller(demand_series.dropna())
    adf_statistic = adf_result[0]
    p_value = adf_result[1]
    print(f"ADF Statistic: {adf_statistic}")
    print(f"p-value: {p_value}")

    # Automatic interpretation of ADF result
    if p_value < 0.05:
        print("✅ The series is stationary. SARIMA model can be safely applied.")
    else:
        print("⚠️ Warning: The series is likely non-stationary. Differencing may be needed.")

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

    # Simulate realistic fluctuations
    forecast_simulated = results.simulate(nsimulations=forecast_steps, anchor='end')

    # Step 4: Visualization
    print("Plotting forecast results...")
    plt.figure(figsize=(15, 5))
    plt.plot(demand_series[-24 * 7:], label='Observed (last 7 days)', color='blue')
    plt.plot(forecast_mean, label='Forecast (smooth)', color='orange')
    plt.plot(forecast_simulated, label='Forecast (simulated)', color='green', alpha=0.7)
    plt.title('SARIMA Forecast of Hourly Electricity Demand (Next Month)')
    plt.xlabel('Date')
    plt.ylabel('Demand (MW)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Step 5: Save forecast to CSV
    print("Saving forecast data to CSV...")
    forecast_df = pd.DataFrame({
        'datetime': forecast_mean.index,
        'forecast_demand_smooth': forecast_mean.values,
        'forecast_demand_simulated': forecast_simulated.values
    })

    output_path = "CodeDataVisualisation/CVSs/FORECAST_DEMAND_2025_MONTH1.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    forecast_df.to_csv(output_path, index=False)
    print(f"✅ Forecast saved to: {output_path}")