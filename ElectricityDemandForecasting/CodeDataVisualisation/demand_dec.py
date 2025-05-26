
import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_december_demand():
    # Step 1: Load dataset
    print("Loading dataset...")
    df = pd.read_csv("FiltredDataSet/PRICE_AND_DEMAND_2024_ALL_NSW1.csv")

    # Step 2: Convert 'SETTLEMENTDATE' to datetime and set as index
    print("Processing datetime...")
    df['SETTLEMENTDATE'] = pd.to_datetime(df['SETTLEMENTDATE'])
    df.set_index('SETTLEMENTDATE', inplace=True)

    # Step 3: Filter data for December
    print("Filtering December data...")
    december_data = df[df.index.month == 12]

    # Step 4: Plotting
    print("Plotting December demand...")
    plt.figure(figsize=(15, 5))
    plt.plot(december_data.index, december_data['TOTALDEMAND'],
             marker='o', linestyle='-', color='lightgreen', linewidth=1)
    plt.title('Total Demand for December')
    plt.xlabel('Date and Time')
    plt.ylabel('Total Demand (MW)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Step 5: Save December data to CSV
    output_path = "CSVs/DECEMBER_DEMAND_2024.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    december_data.to_csv(output_path)
    print(f"✅ December data saved to: {output_path}")


# Call the function
if __name__ == "__main__":
    plot_december_demand()