from src.data_collection.generate_dataset import generate_dataset
from src.data_processing.clean_data import clean_data
from src.analysis.delay_analysis import analyze_delays
from src.analysis.generate_summary_report import generate_summary
from src.visualization.plot_delay import plot_delays
from src.visualization.route_map import generate_route_map
import os
import logging

def configure_logging():
    """
    Configures the extraction logging system.
    """
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename="logs/project.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode='w' # Overwrite log on each run for clean session logs
    )
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def main():
    """
    Main entry point for the Bus Delay & Route Optimization project.
    Orchestrates the entire data pipeline (Version 1.0).
    """
    configure_logging()
    
    logging.info("==================================================")
    logging.info("   Bus Delay Optimization Pipeline Started (v1.0) ")
    logging.info("==================================================")
    
    # Define Paths
    raw_data_path = 'data/raw/bus_delay_dataset.csv'
    processed_data_path = 'data/processed/cleaned_bus_delay.csv'
    
    # Ensure all directories exist
    os.makedirs('reports/plots', exist_ok=True)
    os.makedirs('reports/tables', exist_ok=True)
    
    try:
        # Step 1: Data Collection
        logging.info(">>> Step [1/6]: Generating Dataset...")
        generate_dataset(output_path=raw_data_path)
        
        # Step 2: Data Processing
        logging.info(">>> Step [2/6]: Cleaning Data...")
        clean_data(input_path=raw_data_path, output_path=processed_data_path)
        
        # Step 3: Analysis
        logging.info(">>> Step [3/6]: Running Analysis & Recommendations...")
        analyze_delays(input_path=processed_data_path)
        
        # Step 4: Summary Report
        logging.info(">>> Step [4/6]: Generating Summary Report...")
        generate_summary(input_data=processed_data_path)
        
        # Step 5: Visualization
        logging.info(">>> Step [5/6]: Generating Plots...")
        plot_delays(input_path=processed_data_path)

        # Step 6: Geospatial Map
        logging.info(">>> Step [6/6]: Creating Route Map...")
        generate_route_map(input_path=processed_data_path)
        
        logging.info("==================================================")
        logging.info("   Pipeline Execution Completed Successfully      ")
        logging.info("==================================================")
        
    except Exception as e:
        logging.critical(f"Pipeline failed with error: {str(e)}", exc_info=True)
        print(f"CRITICAL ERROR: {str(e)}. Check logs/project.log for details.")

if __name__ == "__main__":
    main()
