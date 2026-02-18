import pandas as pd
import numpy as np
import os
import logging

def clean_data(input_path='data/raw/bus_delay_dataset.csv', output_path='data/processed/cleaned_bus_delay.csv'):
    """
    Cleans raw bus delay data and adds calculated fields.
    """
    logging.info("Starting data cleaning process...")
    
    if not os.path.exists(input_path):
        logging.error(f"Input file {input_path} not found.")
        return None

    df = pd.read_csv(input_path)

    # 1. Convert Date to Datetime
    df['date'] = pd.to_datetime(df['date'])

    # 2. Remove Negative Delays (Already handled in generation, but good practice)
    df = df[df['delay_min'] >= 0]

    # 3. Calculate Inefficiency Score
    # Formula: (Actual / Scheduled) - 1
    df['inefficiency_score'] = (df['actual_time_min'] / df['scheduled_time_min']) - 1
    
    # 4. Create Delay Categories
    def category_delay(delay):
        if delay <= 5:
            return 'Low'
        elif delay <= 15:
            return 'Moderate'
        else:
            return 'High'

    df['delay_category'] = df['delay_min'].apply(category_delay)

    # Save Cleaned Data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    logging.info(f"Data cleaned and saved to {output_path}")
    logging.info(f"Cleaned records: {len(df)}")
    return df

if __name__ == "__main__":
    clean_data()
