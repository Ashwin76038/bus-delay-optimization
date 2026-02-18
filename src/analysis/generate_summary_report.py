import pandas as pd
import os
import logging

def generate_summary(input_data='data/processed/cleaned_bus_delay.csv', 
                     rec_path='reports/tables/recommendations.csv',
                     output_report='reports/summary_report.txt'):
    """
    Generates a readable summary report of the bus delay analysis.
    """
    logging.info("Generating summary report...")

    if not os.path.exists(input_data):
        logging.error(f"Input file {input_data} not found.")
        return

    df = pd.read_csv(input_data, parse_dates=['date'])
    
    # Compute Key Metrics
    avg_delay = df['delay_min'].mean()
    p95_delay = df['delay_min'].quantile(0.95)
    
    route_avg = df.groupby(['route_no', 'route_name'])['delay_min'].mean()
    worst_route_idx = route_avg.idxmax()
    worst_route = f"{worst_route_idx[0]} ({worst_route_idx[1]})"
    worst_route_delay = route_avg.max()

    hour_avg = df.groupby('hour')['delay_min'].mean()
    congested_hour = hour_avg.idxmax()
    congested_hour_delay = hour_avg.max()
    
    inefficiency = df.groupby(['route_no', 'route_name'])['inefficiency_score'].mean()
    top_inefficient_idx = inefficiency.idxmax()
    top_inefficient = f"{top_inefficient_idx[0]} ({top_inefficient_idx[1]})"
    
    # Read Recommendations
    recommendations_text = ""
    if os.path.exists(rec_path):
        try:
            rec_df = pd.read_csv(rec_path)
            for idx, row in rec_df.iterrows():
                recommendations_text += f"{idx+1}. Route {row['Route']}: {row['Issue']} -> {row['Action']}\n"
        except Exception as e:
            recommendations_text = f"Could not load recommendations: {str(e)}"
    else:
        recommendations_text = "No critical recommendations found."

    # Report Template
    report_content = f"""----------------------------------------
BUS DELAY ANALYTICS SUMMARY REPORT
----------------------------------------
Date Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

KEY METRICS:
- Overall Average Delay: {avg_delay:.2f} min
- 95th Percentile Delay: {p95_delay:.2f} min
- Worst Performing Route: {worst_route} (Avg {worst_route_delay:.2f} min)
- Most Congested Hour:    {congested_hour}:00 (Avg {congested_hour_delay:.2f} min)
- Top Inefficient Route:  {top_inefficient} (Score {inefficiency.max():.2f})

----------------------------------------
AUTOMATED RECOMMENDATIONS:
{recommendations_text}
----------------------------------------
"""

    # Save to File
    os.makedirs(os.path.dirname(output_report), exist_ok=True)
    with open(output_report, 'w') as f:
        f.write(report_content)
    
    logging.info(f"Summary report generated at {output_report}")

if __name__ == "__main__":
    generate_summary()
