import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os
import logging

def generate_dataset(output_path='data/raw/bus_delay_dataset.csv', days=30):
    """
    Generates a realistic 30-day dataset for 6 bus routes in Coimbatore.
    Routes: 33A, 32, 111, 70, 4A, 2A
    """
    logging.info(f"Starting dataset generation for {days} days...")
    
    # 2. Reproducibility
    np.random.seed(42)
    random.seed(42)

    # Configuration
    # Configuration - COIMBATORE ROUTES (Specific)
    routes = {
        '33A': {'distance': 34.0, 'base_time': 75, 'route_name': 'Gandhipuram - Mettupalayam'},
        '32': {'distance': 10.0, 'base_time': 30, 'route_name': 'Gandhipuram - Thudiyalur'},
        '111': {'distance': 10.0, 'base_time': 30, 'route_name': 'Thudiyalur - Gandhipuram'},
        '70': {'distance': 15.0, 'base_time': 45, 'route_name': 'Gandhipuram - Maruthamalai'},
        '4A': {'distance': 18.0, 'base_time': 55, 'route_name': 'Thudiyalur - Podanur'},
        '2A': {'distance': 16.0, 'base_time': 50, 'route_name': 'Perur - Polytechnic'}
    }
    
    trip_hours = [7, 9, 12, 17, 19]
    start_date = datetime.now() - timedelta(days=days)
    
    data = []

    for day in range(days):
        current_date = start_date + timedelta(days=day)
        date_str = current_date.strftime('%Y-%m-%d')
        day_of_week = current_date.strftime('%A')
        is_weekend = current_date.weekday() >= 5

        for route, info in routes.items():
            for hour in trip_hours:
                # Determine Peak Hour
                is_peak = hour in [7, 9, 17, 19] and not is_weekend
                
                # Traffic Multiplier Calculation
                # Base traffic: 1.0
                # Peak hour add: 0.3 - 0.8
                # Non-peak add: 0.0 - 0.2
                # Weekend reduction: -0.1
                
                traffic_multiplier = 1.0
                if is_peak:
                    traffic_multiplier += np.random.uniform(0.3, 0.8)
                else:
                    traffic_multiplier += np.random.uniform(0.0, 0.2)
                
                if is_weekend:
                    traffic_multiplier -= 0.1
                
                # Ensure multiplier is never below 0.8
                traffic_multiplier = max(0.8, traffic_multiplier)

                # Calculate Times
                scheduled_time = info['base_time']
                
                # Actual time influenced by traffic and random noise
                # variance factor: different drivers, weather, signals etc.
                random_variation = np.random.normal(0, 5) # standard deviation of 5 mins
                
                actual_time = (scheduled_time * traffic_multiplier) + random_variation
                actual_time = max(scheduled_time - 5, actual_time) # Can't be impossibly fast, but can be slightly faster
                
                delay = actual_time - scheduled_time
                delay = max(0, delay) # No negative delays for this specific field requirement

                trip_record = {
                    'route_no': route,
                    'route_name': info['route_name'],
                    'distance_km': info['distance'],
                    'scheduled_time_min': int(scheduled_time),
                    'actual_time_min': int(actual_time),
                    'delay_min': int(delay),
                    'hour': hour,
                    'date': date_str,
                    'day_of_week': day_of_week,
                    'peak_hour': is_peak,
                    'traffic_multiplier': round(traffic_multiplier, 2)
                }
                data.append(trip_record)

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logging.info(f"Dataset generated successfully at: {output_path}")
    logging.info(f"Total records: {len(df)}")
    return df

if __name__ == "__main__":
    generate_dataset()
