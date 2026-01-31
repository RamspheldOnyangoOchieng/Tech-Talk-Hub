import folium                          # To create an interactive map showing the optimized route between towns
import openrouteservice                # To call the OpenRouteService API and get real driving distances between locations
from itertools import permutations    # To generate every possible order of visiting towns for route evaluation
import matplotlib.pyplot as plt       # Optional: To visualize the route and directions on a static 2D plot if needed
import numpy as np                    # To help with numerical calculations, like distances or coordinate handling
import pandas as pd                   # To store and organize town data and route distances in structured tables
import random                        # Optional: Can be used if you want to create random test data or shuffle routes
import time                          # Optional: To measure how long route calculations take for performance checks
from folium.plugins import AntPath, PolyLineTextPath
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
ORS_API_KEY = os.getenv('ORS_API_KEY')

# connecting the openrouteservice API

def connect_openrouteservice(api_key):
    """
    Connect to the OpenRouteService API using the provided API key.
    
    :param api_key: Your OpenRouteService API key.
    :return: An instance of the OpenRouteService client.
    """
    try:
        client = openrouteservice.Client(key=api_key)
        return client
    except Exception as e:
        print(f"Error connecting to OpenRouteService: {e}")
        return None

ors_client = connect_openrouteservice(ORS_API_KEY)
if ors_client is None:
    print("Failed to connect to OpenRouteService. Please check your API key.")

def get_route_distance(client, locations):
    """
    Get the driving distance between a list of locations using OpenRouteService.
    
    :param client: An instance of the OpenRouteService client.
    :param locations: A list of tuples containing latitude and longitude of each location.
    :return: The total driving distance in meters.
    """
    try:
        # Create a route request
        route = client.directions(
            profile='driving-car',
            coordinates=locations,
            format='geojson'
        )
        
        # Extract the distance from the route response
        distance = route['features'][0]['properties']['segments'][0]['distance']
        return distance
    except Exception as e:
        print(f"Error getting route distance: {e}")
        return None
def calculate_route_distance(client, route):
    """
    Calculate total driving distance for a route with fixed start and end (Nairobi).
    :param client: OpenRouteService client
    :param route: List of town dicts in visit order (including start/end)
    :return: total distance in meters
    """
    coords = [(town['longitude'], town['latitude']) for town in route]
    return get_route_distance(client, coords)

def visualize_routes_distances(all_routes):
    """
    Create a bar chart visualization of all routes and their distances using matplotlib.
    :param all_routes: List of tuples containing (route, distance, route_str)
    """
    # Extract route strings and distances
    routes = [route[2] for route in all_routes]
    distances = [route[1]/1000 for route in all_routes]  # Convert to kilometers
    
    # Create figure and axis
    plt.figure(figsize=(15, 8))
    
    # Create bar chart
    bars = plt.bar(range(len(routes)), distances)
    
    # Customize the chart
    plt.title('Route Distances Comparison', fontsize=14, pad=20)
    plt.xlabel('Routes', fontsize=12)
    plt.ylabel('Distance (km)', fontsize=12)
    
    # Rotate x-axis labels for better readability
    plt.xticks(range(len(routes)), routes, rotation=45, ha='right')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f} km',
                ha='center', va='bottom')
    
    # Highlight the shortest route
    shortest_idx = distances.index(min(distances))
    bars[shortest_idx].set_color('green')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('route_distances.png')
    print("\nRoute distances visualization saved as 'route_distances.png'")
    
    # Show the plot
    plt.show()

def optimize_route(client, towns):
    """
    Optimize the route visiting all towns starting and ending in Nairobi.
    :param client: ORS client
    :param towns: Full list of towns, including Nairobi
    :return: optimized town order including Nairobi at start/end
    """
    start = towns[0]  # Nairobi
    others = towns[1:]
    best_distance = float('inf')
    best_route = None
    all_routes = []
    
    print("\nCalculating all possible routes...")
    print("-" * 50)
    
    for perm in permutations(others):
        route = [start] + list(perm) + [start]  # Start and end at Nairobi
        dist = calculate_route_distance(client, route)
        if dist is not None:
            route_names = [town['name'] for town in route]
            route_str = " → ".join(route_names)
            all_routes.append((route, dist, route_str))
            print(f"Route: {route_str}")
            print(f"Distance: {dist/1000:.2f} km")
            print("-" * 50)
            
            if dist < best_distance:
                best_distance = dist
                best_route = route
    
    # Sort routes by distance
    all_routes.sort(key=lambda x: x[1])
    
    # Print the shortest route
    if all_routes:
        shortest_route, shortest_dist, shortest_str = all_routes[0]
        print("\nShortest Route Found:")
        print("=" * 50)
        print(f"Route: {shortest_str}")
        print(f"Total Distance: {shortest_dist/1000:.2f} km")
        print("=" * 50)
        
        # Create visualization of all routes
        visualize_routes_distances(all_routes)
    
    return best_route

def create_map(towns, route):
    """
    Create a folium map with markers, optimized route, and animated car movement.
    :param towns: full towns list
    :param route: optimized route including start/end
    """
    # Create the base map centered on the first town
    m = folium.Map(location=[route[0]['latitude'], route[0]['longitude']], zoom_start=7)
    
    # Add markers with popups and custom icons
    for i, town in enumerate(towns):
        # Customize marker color based on whether it's the start/end point
        if town['name'] == 'Nairobi':
            icon_color = 'red'
            icon = 'home'
        else:
            icon_color = 'blue'
            icon = 'info-sign'
            
        folium.Marker(
            location=[town['latitude'], town['longitude']],
            popup=f"{town['name']} (Stop {i+1})",
            icon=folium.Icon(color=icon_color, icon=icon, prefix='glyphicon')
        ).add_to(m)
    
    # Create route coordinates
    route_coords = [(town['latitude'], town['longitude']) for town in route]
    
    # Add the base route line
    folium.PolyLine(
        route_coords,
        color='blue',
        weight=3,
        opacity=0.5
    ).add_to(m)
    
    # Add the animated ant path
    ant_path = AntPath(
        route_coords,
        color='blue',
        weight=5,
        delay=1000,
        dash_array=[10, 20],
        pulse_color='red'
    ).add_to(m)
    
    # Create car icon HTML with rotation
    car_html = """
    <div style="position: absolute; transform: translate(-50%, -50%);">
        <div style="font-size: 24px; transform: rotate({rotation}deg);">🚗</div>
    </div>
    """
    
    # Add the car marker
    car_marker = folium.Marker(
        location=route_coords[0],
        icon=folium.DivIcon(
            html=car_html.format(rotation=0),
            icon_size=(24, 24),
            icon_anchor=(12, 12)
        ),
        popup='Traveling Car'
    ).add_to(m)
    
    # Add JavaScript for car animation
    js_code = """
    var car = document.querySelector('div[style="font-size: 24px;"]').parentElement;
    var route = %s;
    var currentIndex = 0;
    var animationSpeed = 2000; // 2 seconds between each point
    
    function calculateRotation(start, end) {
        var dx = end[1] - start[1];
        var dy = end[0] - start[0];
        return Math.atan2(dy, dx) * 180 / Math.PI;
    }
    
    function moveCar() {
        if (currentIndex < route.length - 1) {
            var current = route[currentIndex];
            var next = route[currentIndex + 1];
            var rotation = calculateRotation(current, next);
            
            car.style.transform = 'translate(' + next[1] + 'px, ' + next[0] + 'px) rotate(' + rotation + 'deg)';
            currentIndex++;
            setTimeout(moveCar, animationSpeed);
        }
    }
    
    moveCar();
    """ % route_coords
    
    # Add the JavaScript to the map
    m.get_root().html.add_child(folium.Element(f'<script>{js_code}</script>'))
    
    # Add a layer control
    folium.LayerControl().add_to(m)
    
    # Save the map
    m.save('optimized_route_map.html')
    print("Interactive animated map with car movement created and saved as 'optimized_route_map.html'.")

def calculate_all_routes(client, towns):
    """
    Calculate and display all possible routes with their distances.
    :param client: ORS client
    :param towns: List of towns
    :return: List of tuples containing (route, distance)
    """
    start = towns[0]  # Nairobi
    others = towns[1:]
    all_routes = []
    
    print("\nCalculating all possible routes...")
    print("-" * 50)
    
    for perm in permutations(others):
        route = [start] + list(perm) + [start]  # Start and end at Nairobi
        dist = calculate_route_distance(client, route)
        if dist is not None:
            route_names = [town['name'] for town in route]
            route_str = " → ".join(route_names)
            all_routes.append((route, dist, route_str))
            print(f"Route: {route_str}")
            print(f"Distance: {dist/1000:.2f} km")
            print("-" * 50)
    
    # Sort routes by distance
    all_routes.sort(key=lambda x: x[1])
    
    # Print the shortest route
    if all_routes:
        shortest_route, shortest_dist, shortest_str = all_routes[0]
        print("\nShortest Route Found:")
        print("=" * 50)
        print(f"Route: {shortest_str}")
        print(f"Total Distance: {shortest_dist/1000:.2f} km")
        print("=" * 50)
        
    return all_routes

def main():
    towns = [
        {'name': 'Nairobi', 'latitude': -1.2921, 'longitude': 36.8219},
        {'name': 'Meru', 'latitude': 0.0460, 'longitude': 37.6493},
        {'name': 'Nyeri', 'latitude': -0.4167, 'longitude': 36.9500},
        {'name': 'Nandi', 'latitude': 0.1000, 'longitude': 35.1833},
        {'name': 'Kericho', 'latitude': -0.3673, 'longitude': 35.2830}
    ]
    
    # Connect to OpenRouteService
    ors_client = connect_openrouteservice(ORS_API_KEY)
    if ors_client is None:
        print("Could not connect to OpenRouteService. Exiting.")
        return
    
    # Optimize the route
    optimized_route = optimize_route(ors_client, towns)
    if optimized_route is None:
        print("No valid route found. Please check your internet connection or OpenRouteService API availability.")
        return
    
    # Create a map showing the optimized route
    create_map(towns, optimized_route)
    print("\nMap has been created and saved as 'optimized_route_map.html'")
    print("Please open the HTML file in your web browser to view the route visualization.")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"\nRoute optimization completed in {end_time - start_time:.2f} seconds.")

