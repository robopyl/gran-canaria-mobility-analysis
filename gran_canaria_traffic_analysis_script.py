import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Create output directory for exported datasets and figures
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_synthetic_mobility_data(num_records=12000):
    """
    Generates a realistic synthetic mobility dataset for Gran Canaria public transit & traffic.
    Corridors cover main urban and commuter routes across the island.
    """
    print("[1/4] Generating synthetic mobility dataset for Gran Canaria...")
    
    routes = [
        "Las Palmas GC - Telde (GC-1)",
        "Las Palmas GC - Maspalomas (GC-1)",
        "Las Palmas GC - Arucas (GC-2)",
        "Telde - Airport (GC-1)",
        "Las Palmas Urban (Mesa y Lopez - Triana)",
        "Galdar - Las Palmas GC (GC-2)",
        "Maspalomas - Mogan (GC-500)"
    ]
    
    start_date = datetime(2026, 10, 1)
    timestamps = [start_date + timedelta(minutes=random.randint(0, 30 * 24 * 60)) for _ in range(num_records)]
    
    data = []
    for ts in timestamps:
        route = random.choice(routes)
        hour = ts.hour
        
        # Base passenger load and delays dependent on peak hours
        is_morning_peak = 7 <= hour <= 9
        is_evening_peak = 17 <= hour <= 19
        
        if is_morning_peak or is_evening_peak:
            passenger_count = np.random.randint(40, 95)
            delay_minutes = np.random.exponential(scale=10.0) + 3
        else:
            passenger_count = np.random.randint(10, 50)
            delay_minutes = np.random.exponential(scale=3.0)
            
        # Introduce synthetic missing values (~2% missing data) for cleaning demo
        if random.random() < 0.02:
            delay_minutes = np.nan
            
        data.append({
            "timestamp": ts,
            "route": route,
            "passenger_count": passenger_count,
            "delay_minutes": round(delay_minutes, 2) if not np.isnan(delay_minutes) else np.nan,
            "bus_id": f"BUS-{random.randint(100, 150)}"
        })
        
    df = pd.DataFrame(data)
    csv_path = os.path.join(OUTPUT_DIR, "traffic_data.csv")
    df.to_csv(csv_path, index=False)
    print(f" -> Dataset saved with {len(df)} records at: {csv_path}")
    return df


def clean_and_prepare_data(df):
    """
    Cleans raw transit data, handles missing values, and creates derived temporal features.
    """
    print("[2/4] Cleaning and preparing dataset...")
    
    # 1. Fill missing delay values with route median
    df["delay_minutes"] = df.groupby("route")["delay_minutes"].transform(lambda x: x.fillna(x.median()))
    
    # 2. Extract temporal features
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.day_name()
    df["is_weekend"] = df["timestamp"].dt.dayofweek >= 5
    
    # 3. Categorize peak times
    def categorize_period(h):
        if 7 <= h <= 9:
            return "Morning Peak (07-09)"
        elif 17 <= h <= 19:
            return "Evening Peak (17-19)"
        else:
            return "Off-Peak"
            
    df["period"] = df["hour"].apply(categorize_period)
    print(" -> Data cleaning and feature engineering completed.")
    return df


def calculate_kpis(df):
    """
    Computes key performance indicators (KPIs) and congestion summaries.
    """
    print("[3/4] Calculating Key Performance Indicators (KPIs)...")
    
    total_passengers = df["passenger_count"].sum()
    avg_delay = df["delay_minutes"].mean()
    busiest_route = df.groupby("route")["passenger_count"].sum().idxmax()
    peak_delay = df[df["period"] != "Off-Peak"]["delay_minutes"].mean()
    
    print("\n" + "="*45)
    print("      GRAN CANARIA MOBILITY KPI REPORT     ")
    print("="*45)
    print(f"Total Passengers Analyzed : {total_passengers:,}")
    print(f"System Average Delay      : {avg_delay:.2f} minutes")
    print(f"Peak Hour Average Delay   : {peak_delay:.2f} minutes")
    print(f"Busiest Corridor          : {busiest_route}")
    print("="*45 + "\n")


def generate_visualizations(df):
    """
    Generates and exports analytical plots for GitHub documentation.
    """
    print("[4/4] Generating analytical visualizations...")
    sns.set_theme(style="whitegrid")

    # Chart 1: Hourly Passenger Volume
    plt.figure(figsize=(10, 5))
    hourly_df = df.groupby("hour")["passenger_count"].mean().reset_index()
    sns.lineplot(data=hourly_df, x="hour", y="passenger_count", marker="o", color="#1f77b4", linewidth=2.5)
    plt.title("Gran Canaria: Average Passenger Volume by Hour of Day", fontsize=12, fontweight="bold")
    plt.xlabel("Hour of Day (0-23)", fontsize=10)
    plt.ylabel("Avg Passenger Count per Bus", fontsize=10)
    plt.xticks(range(0, 24))
    plt.tight_layout()
    plot1_path = os.path.join(OUTPUT_DIR, "hourly_flow.png")
    plt.savefig(plot1_path, dpi=300)
    plt.close()
    print(f" -> Exported: {plot1_path}")

    # Chart 2: Average Delay by Route
    plt.figure(figsize=(11, 5))
    route_delay = df.groupby("route")["delay_minutes"].mean().sort_values().reset_index()
    sns.barplot(data=route_delay, x="delay_minutes", y="route", palette="Viridis")
    plt.title("Average Transit Delay by Corridor (Minutes)", fontsize=12, fontweight="bold")
    plt.xlabel("Average Delay (Minutes)", fontsize=10)
    plt.ylabel("Transit Corridor", fontsize=10)
    plt.tight_layout()
    plot2_path = os.path.join(OUTPUT_DIR, "route_delay.png")
    plt.savefig(plot2_path, dpi=300)
    plt.close()
    print(f" -> Exported: {plot2_path}")

    # Chart 3: Heatmap of Route vs Peak Period Congestion
    plt.figure(figsize=(10, 6))
    pivot_table = df.pivot_table(values="delay_minutes", index="route", columns="period", aggfunc="mean")
    sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label': 'Avg Delay (min)'})
    plt.title("Route Congestion Heatmap across Commute Periods", fontsize=12, fontweight="bold")
    plt.xlabel("Commute Period", fontsize=10)
    plt.ylabel("Corridor", fontsize=10)
    plt.tight_layout()
    plot3_path = os.path.join(OUTPUT_DIR, "heatmap.png")
    plt.savefig(plot3_path, dpi=300)
    plt.close()
    print(f" -> Exported: {plot3_path}")


if __name__ == "__main__":
    df_raw = generate_synthetic_mobility_data()
    df_clean = clean_and_prepare_data(df_raw)
    calculate_kpis(df_clean)
    generate_visualizations(df_clean)
    print("\n✅ Project execution complete! Check the 'output/' folder for outputs.")