import pandas as pd
import numpy as np
import os
import logging

def analyze_delays(input_path='data/processed/cleaned_bus_delay.csv', output_dir='reports/tables'):
    """
    Performs statistical analysis, computes advanced metrics, and generates recommendations.
    """
    logging.info("Starting delay analysis...")
    
    if not os.path.exists(input_path):
        logging.error(f"Input file {input_path} not found.")
        return

    df = pd.read_csv(input_path, parse_dates=['date'])
    os.makedirs(output_dir, exist_ok=True)

    # --- Basic Stats ---
    avg_delay = df['delay_min'].mean()
    logging.info(f"Overall Average Delay: {avg_delay:.2f} minutes")

    route_avg_delay = df.groupby('route_no')['delay_min'].mean().sort_values(ascending=False)
    
    # --- Advanced Metrics ---
    # 1. Standard Deviation
    std_dev_delay = df['delay_min'].std()
    logging.info(f"Delay Standard Deviation: {std_dev_delay:.2f} minutes")

    # 2. 95th Percentile
    p95_delay = df['delay_min'].quantile(0.95)
    logging.info(f"95th Percentile Delay: {p95_delay:.2f} minutes")

    # 3. Peak vs Non-Peak Percentage Diff
    peak_delay = df[df['peak_hour'] == True]['delay_min'].mean()
    non_peak_delay = df[df['peak_hour'] == False]['delay_min'].mean()
    pct_diff = ((peak_delay - non_peak_delay) / non_peak_delay) * 100 if non_peak_delay > 0 else 0
    logging.info(f"Peak vs Non-Peak Difference: {pct_diff:.2f}%")

    # --- Exports ---
    # 4. Route Efficiency Ranking
    route_ranking = df.groupby(["route_no", "route_name"])["inefficiency_score"].mean().sort_values(ascending=False).rename("Average Inefficiency")
    ranking_path = os.path.join(output_dir, "route_ranking.csv")
    route_ranking.to_csv(ranking_path)
    logging.info(f"Route ranking exported to {ranking_path}")

    # --- Recommendations Engine ---
    logging.info("Generating business recommendations...")
    recommendations = []

    # Rule 1: High Inefficiency
    # route_ranking index is now (route_no, route_name)
    inefficient_routes = route_ranking[route_ranking > 0.25].index.tolist()
    for route_no, route_name in inefficient_routes:
        recommendations.append({
            "Route": f"{route_no} ({route_name})",
            "Issue": "High Inefficiency (> 0.25)",
            "Action": "Increase frequency during peak hours & review schedule"
        })

    # Rule 2: Peak Hour Congestion (General)
    if pct_diff > 30:
        recommendations.append({
            "Route": "ALL",
            "Issue": f"Significant Peak Congestion (+{pct_diff:.0f}%)",
            "Action": "Reschedule departure times to buffer peak delays"
        })

    # Rule 3: High Variability
    route_std = df.groupby(['route_no', 'route_name'])['delay_min'].std()
    unstable_routes = route_std[route_std > 10].index.tolist() # Threshold: 10 mins std dev
    for route_no, route_name in unstable_routes:
        recommendations.append({
            "Route": f"{route_no} ({route_name})",
            "Issue": "High Delay Variability (Std Dev > 10m)",
            "Action": "Investigate inconsistent traffic patterns or driver performance"
        })

    # Save Recommendations
    rec_df = pd.DataFrame(recommendations)
    if not rec_df.empty:
        rec_path = os.path.join(output_dir, "recommendations.csv")
        rec_df.to_csv(rec_path, index=False)
        logging.info(f"Recommendations exported to {rec_path}")
    else:
        logging.info("No critical recommendations generated based on current thresholds.")

    logging.info("Analysis phase completed.")

if __name__ == "__main__":
    analyze_delays()
