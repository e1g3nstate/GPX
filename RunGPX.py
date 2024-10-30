import gpxpy
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import numpy as np

def main():
    # Prompt user for GPX file name
    gpx_file_name = input("Enter the GPX file name (with extension): ")

    # Open the GPX file
    try:
        with open(gpx_file_name, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
    except FileNotFoundError:
        print(f"Error: File '{gpx_file_name}' not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the GPX file: {e}")
        return

    # Lists to store data
    times = []
    latitudes = []
    longitudes = []

    # Extract data from GPX
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if point.time is not None:
                    times.append(point.time)
                    latitudes.append(point.latitude)
                    longitudes.append(point.longitude)
                else:
                    print("Warning: A point without time data was skipped.")

    if not times:
        print("Error: No time data found in the GPX file.")
        return

    # Convert times to elapsed seconds
    start_time = times[0]
    elapsed_times = [(t - start_time).total_seconds() for t in times]

    # Calculate displacements from starting position
    start_coords = (latitudes[0], longitudes[0])
    north_south_displacements = []  # Positive north, negative south
    east_west_displacements = []    # Positive east, negative west

    for lat, lon in zip(latitudes, longitudes):
        current_coords = (lat, lon)

        # Calculate north-south displacement
        north_point = (lat, longitudes[0])
        ns_distance = geodesic(start_coords, north_point).kilometers
        if lat < latitudes[0]:
            ns_distance = -ns_distance  # Moving south

        # Calculate east-west displacement
        east_point = (latitudes[0], lon)
        ew_distance = geodesic(start_coords, east_point).kilometers
        if lon < longitudes[0]:
            ew_distance = -ew_distance  # Moving west

        north_south_displacements.append(ns_distance)
        east_west_displacements.append(ew_distance)

    # Plot North-South and East-West Displacement over Time
    plt.figure(figsize=(12, 6))
    plt.plot(elapsed_times, north_south_displacements, label='North-South Displacement', color='green')
    plt.plot(elapsed_times, east_west_displacements, label='East-West Displacement', color='purple')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Displacement (km)')
    plt.title('Displacement vs. Time')
    plt.legend()
    plt.grid(True)

    # Prompt user for output image file name
    output_file_name = input("Enter the output image file name (with extension, e.g., output.png): ")

    # Save the plot to the specified file
    try:
        plt.savefig(output_file_name)
        print(f"Graph has been saved as '{output_file_name}'.")
    except Exception as e:
        print(f"An error occurred while saving the image: {e}")

if __name__ == "__main__":
    main()
