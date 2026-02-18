# Bus Delay Optimization & Route Analytics - Coimbatore Edition

**Version**: 2.0  
**Last Updated**: 2026-02-18

## Project Overview
This data analytics project optimizes public transport efficiency by analyzing bus delay patterns for **Coimbatore, Tamil Nadu**. It simulates realistic trip data for specific high-traffic routes (e.g., Gandhipuram, Thudiyalur, Mettupalayam) to identify bottlenecks, quantify inefficiency, and generate actionable recommendations for transport authorities.

## Key Features
-   **Realistic Data Simulation**: Generates 30-day trip data for 6 specific Coimbatore routes, incorporating peak-hour traffic logic and weekend variations.
-   **Advanced Metrics**: Calculates "Inefficiency Scores", "Delay Variability" (Std Dev), and "Peak vs. Non-Peak Congestion" percentages.
-   **Automated Reporting**: Produces a comprehensive text summary (`summary_report.txt`) and CSV exports for route rankings and business recommendations.
-   **Interactive Visualization**: Generates a dynamic geospatial map (`bus_route_map.html`) using Folium, visualizing route paths and inefficiency levels on a map of Coimbatore.
-   **Named Route Identification**: All outputs explicitly name routes (e.g., *Route 33A (Gandhipuram - Mettupalayam)*) for clarity.

## Routes Analyzed
The project currently simulates the following popular routes:
1.  **33A**: Gandhipuram ↔ Mettupalayam
2.  **32**: Gandhipuram ↔ Thudiyalur
3.  **111**: Thudiyalur ↔ Gandhipuram
4.  **70**: Gandhipuram ↔ Maruthamalai
5.  **4A**: Thudiyalur ↔ Podanur
6.  **2A**: Perur ↔ Polytechnic

## Folder Structure
```
bus-delay-optimization/
│── data/
│   ├── raw/                 # Generated raw datasets (bus_delay_dataset.csv)
│   ├── processed/           # Cleaned datasets with calculated fields
│── logs/                    # Execution logs (project.log)
│── src/                     # Source Code
│   ├── data_collection/     # Data generation logic (Coimbatore specific)
│   ├── data_processing/     # Data cleaning & transformation
│   ├── analysis/            # Statistical analysis & recommendation engine
│   ├── visualization/       # Plotting & Map generation (Folium, Seaborn)
│── reports/                 # Output Artifacts
│   ├── plots/               # Distribution charts, Heatmaps (PNG)
│   ├── tables/              # Route Rankings, Recommendations (CSV)
│   ├── bus_route_map.html   # Interactive Route Map
│   └── summary_report.txt   # Executive Summary
│── main.py                  # Pipeline Orchestrator
│── requirements.txt         # Python Dependencies
│── README.md                # Documentation
```

## How to Run
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Execute the Pipeline**:
    ```bash
    python main.py
    ```
3.  **Explore the Results**:
    -   **Executive Summary**: Open `reports/summary_report.txt`.
    -   **Interactive Map**: Open `reports/bus_route_map.html` in your web browser.
    -   **Data Tables**: Check `reports/tables/` for detailed CSV analysis.

## Tech Stack
-   **Python 3.x**
-   **Pandas & NumPy**: Data manipulation and analysis.
-   **Folium**: Geospatial data visualization.
-   **Matplotlib & Seaborn**: Statistical plotting.
-   **Logging**: Built-in Python logging for pipeline tracking.
