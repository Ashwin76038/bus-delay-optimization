import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging

def plot_delays(input_path='data/processed/cleaned_bus_delay.csv', output_dir='reports/plots'):
    """
    Generates various visualizations for bus delay analysis.
    """
    logging.info("Generating visualizations...")
    
    if not os.path.exists(input_path):
        logging.error(f"Input file {input_path} not found.")
        return

    df = pd.read_csv(input_path)
    os.makedirs(output_dir, exist_ok=True)

    # Set style
    sns.set_style("whitegrid")
    
    # 1. Delay Distribution Histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(df['delay_min'], kde=True, bins=30, color='skyblue')
    plt.title('Distribution of Bus Delays')
    plt.xlabel('Delay (minutes)')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, 'delay_distribution.png'))
    plt.close()
    logging.info("Saved delay_distribution.png")

    # 2. Route-wise Average Delay Bar Chart
    plt.figure(figsize=(12, 6))
    avg_delay = df.groupby('route_no')['delay_min'].mean().sort_values()
    sns.barplot(x=avg_delay.index, y=avg_delay.values, hue=avg_delay.index, palette='viridis', legend=False)
    plt.title('Average Delay by Route')
    plt.xlabel('Route Number')
    plt.ylabel('Average Delay (minutes)')
    plt.savefig(os.path.join(output_dir, 'route_wise_delay.png'))
    plt.close()
    logging.info("Saved route_wise_delay.png")

    # 3. Hour vs Delay Line Plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='hour', y='delay_min', hue='route_no', marker='o')
    plt.title('Delay Trends by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Delay (minutes)')
    plt.xticks(sorted(df['hour'].unique()))
    plt.legend(title='Route', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'hour_vs_delay.png'))
    plt.close()
    logging.info("Saved hour_vs_delay.png")

    # 4. Heatmap (Hour vs Route Average Delay)
    pivot_table = df.pivot_table(index='route_no', columns='hour', values='delay_min', aggfunc='mean')
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_table, annot=True, cmap='coolwarm', fmt=".1f")
    plt.title('Heatmap of Average Delays (Route vs Hour)')
    plt.xlabel('Hour of Day')
    plt.ylabel('Route Number')
    plt.savefig(os.path.join(output_dir, 'delay_heatmap.png'))
    plt.close()
    logging.info("Saved delay_heatmap.png")
    
    # 5. Scatter Plot: Traffic Multiplier vs Delay
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='traffic_multiplier', y='delay_min', hue='peak_hour', alpha=0.7)
    plt.title('Impact of Traffic Multiplier on Delay')
    plt.xlabel('Traffic Multiplier')
    plt.ylabel('Delay (minutes)')
    plt.savefig(os.path.join(output_dir, 'traffic_vs_delay.png'))
    plt.close()
    logging.info("Saved traffic_vs_delay.png")

    logging.info(f"All plots saved to {output_dir}")

if __name__ == "__main__":
    plot_delays()
