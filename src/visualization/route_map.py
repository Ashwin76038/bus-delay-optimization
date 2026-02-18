import folium
import pandas as pd
import os
import random
import logging

def generate_route_map(input_path='data/processed/cleaned_bus_delay.csv', output_path='reports/bus_route_map.html'):
    """
    Generates an interactive map of bus routes colored by inefficiency.
    Simulates route coordinates for Coimbatore area.
    """
    logging.info("Generating geospatial map...")
    
    if not os.path.exists(input_path):
        logging.error(f"Input file {input_path} not found.")
        return

    df = pd.read_csv(input_path)
    
    # Calculate average inefficiency per route for color coding
    # We use 'first' for route_name since it's constant per route_no
    route_stats = df.groupby('route_no').agg({
        'inefficiency_score': 'mean',
        'delay_min': 'mean',
        'route_name': 'first'
    }).reset_index()

    # Coimbatore Center
    coimbatore_lat, coimbatore_lon = 11.0168, 76.9558
    m = folium.Map(location=[coimbatore_lat, coimbatore_lon], zoom_start=12)

    # Simulated Route Coordinates for Coimbatore (Specific)
    # NOTE: These are approximate straight lines for visualization
    route_coords = {
        '33A': [(11.0168, 76.9558), (11.3006, 76.9366)], # Gandhipuram - Mettupalayam
        '32': [(11.0168, 76.9558), (11.0822, 76.9427)],  # Gandhipuram - Thudiyalur
        '111': [(11.0822, 76.9427), (11.0168, 76.9558)], # Thudiyalur - Gandhipuram (Reverse of 32)
        '70': [(11.0168, 76.9558), (11.0422, 76.8770)],  # Gandhipuram - Maruthamalai
        '4A': [(11.0822, 76.9427), (10.9634, 76.9804)],  # Thudiyalur - Podanur
        '2A': [(10.9850, 76.9180), (11.0287, 77.0305)]   # Perur - Polytechnic
    }

    # Color scale based on inefficiency
    def get_color(score):
        if score < 0.1: return 'green'
        elif score < 0.2: return 'orange'
        else: return 'red'

    for index, row in route_stats.iterrows():
        route = row['route_no']
        coords = route_coords.get(route, [(coimbatore_lat, coimbatore_lon)])
        
        color = get_color(row['inefficiency_score'])
        
        # Draw Route Line
        folium.PolyLine(
            locations=coords,
            color=color,
            weight=5,
            opacity=0.8,
            tooltip=f"Route {route} ({row['route_name']}): Avg Inefficiency {row['inefficiency_score']:.2f}"
        ).add_to(m)

        # Add Markers
        folium.Marker(
            location=coords[0],
            popup=f"Start Route {route} ({row['route_name']})",
            icon=folium.Icon(color='blue', icon='play')
        ).add_to(m)
        
        folium.Marker(
            location=coords[-1],
            popup=f"End Route {route} ({row['route_name']})",
            icon=folium.Icon(color='red', icon='stop')
        ).add_to(m)

    # Add Legend (HTML overlay)
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity:0.8">
     &nbsp;<b>Inefficiency Score</b> <br>
     &nbsp;<i class="fa fa-circle" style="color:green"></i>&nbsp;Low (< 0.1)<br>
     &nbsp;<i class="fa fa-circle" style="color:orange"></i>&nbsp;Moderate (< 0.2)<br>
     &nbsp;<i class="fa fa-circle" style="color:red"></i>&nbsp;High (>= 0.2)<br>
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save Map
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    m.save(output_path)
    logging.info(f"Map saved to {output_path}")

if __name__ == "__main__":
    generate_route_map()
