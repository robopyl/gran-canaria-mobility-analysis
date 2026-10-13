[github_readme.md](https://github.com/user-attachments/files/33396163/github_readme.md)
# Gran Canaria Mobility & Traffic Flow Analysis

1. ## Executive Summary

This project presents an end-to-end data analytics workflow analyzing public transport and commuter traffic flow patterns across major transit corridors in **Gran Canaria, Spain** (e.g., Las Palmas de Gran Canaria, Telde, Airport, Maspalomas, Arucas).

Using realistic synthetic dataset generation based on public mobility indicators, the pipeline handles data cleaning, feature engineering, exploratory data analysis (EDA), congestion index calculations, and automated visualisation generation.

2. ## Key Features & Technical Scope

* **Data Simulation & Generation:** Programmatically simulates 10,000+ transit records representing daily commuter routes, timestamps, passenger loads, delay times, and transport lines (*Guaguas*).

* **Data Cleaning & Wrangling:** Handles missing values, standardises geographic route labels, filters anomalies, and parses temporal attributes using `pandas`.

* **Exploratory Data Analysis (EDA):** Identifies peak morning/evening commuting windows, high-density hubs, and bottleneck corridors across the island.

* **KPI & Congestion Metrics:** Computes key operational metrics including **Average Delay Per Route**, **Passenger Volume per Hour**, and **Route Congestion Index (RCI)**.

* **Data Visualisation:** Generates publication-ready visual charts using `matplotlib` and `seaborn`.

3. ## Key Findings & Metrics Summary

* **Peak Commute Hours:** The primary morning rush hour occurs between **07:00 – 09:00**, with an evening peak between **17:00 – 19:00**.

* **Highest Volume Corridor:** The **Las Palmas de Gran Canaria ↔ Telde / Airport (GC-1 corridor)** exhibits the highest passenger density and peak congestion levels.

* **Average Delay:** System-wide average delay averages **8.4 minutes** during peak hours, spiking up to **18.5 minutes** on bottleneck routes.

4. ## Repository Structure

```
├── main.py              # Main Python script (data generation, EDA, metrics, chart exporter)
├── requirements.txt     # Dependency list
├── README.md            # Project documentation
└── output/              # Generated datasets and exported charts
    ├── traffic_data.csv # Raw synthetic dataset
    ├── hourly_flow.png  # Hourly commuter traffic chart
    ├── route_delay.png  # Average delay by route bar chart
    └── heatmap.png      # Congestion matrix heatmap

```
5. ## Quick Start & Installation

### 5.1. Prerequisites

Ensure you have **Python 3.9+** installed on your machine.

### 5.2. Clone Repository & Setup Environment

```
git clone https://github.com/your-username/gran-canaria-mobility-analysis.git
cd gran-canaria-mobility-analysis

```
### 5.3. Install Dependencies

```
pip install pandas numpy matplotlib seaborn

```

### 5.4. Run the Pipeline

Execute the main script to generate the synthetic dataset, calculate KPIs, and save visualisation plots to the `output/` directory:

```
python main.py

```

6. ## Built With

* **Language:** Python

* **Data Manipulation:** `pandas`, `numpy`

* **Visualisation:** `matplotlib`, `seaborn`

7. ## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
