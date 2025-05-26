import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import os

# === Step 1: Load hourly demand data ===
df = pd.read_csv("../FiltredDataset/PRICE_AND_DEMAND_2024_HOURLY_NSW1.csv", parse_dates=True, index_col='SETTLEMENTDATE')

# === Step 2: Keep TOTALDEMAND series and set frequency explicitly ===
demand_series = df['TOTALDEMAND']
demand_series = demand_series.asfreq('h')  # Set hourly frequency

# === Step 3: Stationarity Check (ADF Test) ===
adf_result = adfuller(demand_series.dropna())
print("ADF Statistic:", adf_result[0])
print("p-value:", adf_result[1])

# === Step 4: Define and Fit SARIMA Model ===
model = SARIMAX(demand_series,
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 24),
                enforce_stationarity=False,
                enforce_invertibility=False)

results = model.fit(disp=False)
print(results.summary())

# === Step 5: Forecast next 1 month (~730 hours) ===
forecast_steps = 730
forecast = results.get_forecast(steps=forecast_steps)
forecast_mean = forecast.predicted_mean
forecast_ci = forecast.conf_int()

# === Step 6: Plot Forecast ===
plt.figure(figsize=(15, 5))

# Plot last 7 days of actual demand
plt.plot(demand_series[-24*7:], label='Observed (last 7 days)', color='blue')

# Plot forecast with confidence intervals
plt.plot(forecast_mean, label='Forecast (next month)', color='orange')
plt.fill_between(forecast_ci.index,
                 forecast_ci.iloc[:, 0],
                 forecast_ci.iloc[:, 1], color='orange', alpha=0.2)

# Limit y-axis: realistic range from 0 to 2 × max observed demand
plt.ylim(0, demand_series.max() * 2)

plt.title('SARIMA Forecast of Hourly Electricity Demand (Next Month)')
plt.xlabel('Date')
plt.ylabel('Demand (MW)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === Step 7: Save Forecast to CSV ===
forecast_df = pd.DataFrame({
    'datetime': forecast_mean.index,
    'forecast_demand': forecast_mean,
    'lower_ci': forecast_ci.iloc[:, 0],
    'upper_ci': forecast_ci.iloc[:, 1]
})

output_path = "../FiltredDataset/FORECAST_DEMAND_2025_MONTH1.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
forecast_df.to_csv(output_path, index=False)
print(f"✅ Forecast saved to: {output_path}")