import gpxpy
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import numpy as np
import os
import csv

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

    # Prompt user for output folder and file name
    output_folder_name = input("Enter the output folder and file base name: ")
    os.makedirs(output_folder_name, exist_ok=True)

    # Calculate velocity (first derivative of displacement) and acceleration (second derivative)
    velocities_ns = np.gradient(north_south_displacements, elapsed_times)
    velocities_ew = np.gradient(east_west_displacements, elapsed_times)
    accelerations_ns = np.gradient(velocities_ns, elapsed_times)
    accelerations_ew = np.gradient(velocities_ew, elapsed_times)

    # Plot and save North-South and East-West Displacement vs. Time graphs
    plt.figure(figsize=(12, 6))
    plt.plot(elapsed_times, north_south_displacements, label='North-South Displacement', color='green')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Displacement (km)')
    plt.title('North-South Displacement vs. Time')
    plt.grid(True)
    displacement_ns_graph_path = os.path.join(output_folder_name, f"{output_folder_name}_NS_displacement.png")
    plt.savefig(displacement_ns_graph_path)
    plt.close()
    print(f"North-South displacement graph saved as '{displacement_ns_graph_path}'.")

    plt.figure(figsize=(12, 6))
    plt.plot(elapsed_times, east_west_displacements, label='East-West Displacement', color='purple')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Displacement (km)')
    plt.title('East-West Displacement vs. Time')
    plt.grid(True)
    displacement_ew_graph_path = os.path.join(output_folder_name, f"{output_folder_name}_EW_displacement.png")
    plt.savefig(displacement_ew_graph_path)
    plt.close()
    print(f"East-West displacement graph saved as '{displacement_ew_graph_path}'.")

    # Plot and save North-South and East-West Velocity vs. Time graphs
    plt.figure(figsize=(12, 6))
    plt.plot(elapsed_times, velocities_ns, label='North-South Velocity', color='blue')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Velocity (km/s)')
    plt.title('North-South Velocity vs. Time')
    plt.grid(True)
    velocity_ns_graph_path = os.path.join(output_folder_name, f"{output_folder_name}_NS_velocity.png")
    plt.savefig(velocity_ns_graph_path)
    plt.close()
    print(f"North-South velocity graph saved as '{velocity_ns_graph_path}'.")

    plt.figure(figsize=(12, 6))
    plt.plot(elapsed_times, velocities_ew, label='East-West Velocity', color='orange')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Velocity (km/s)')
    plt.title('East-West Velocity vs. Time')
    plt.grid(True)
    velocity_ew_graph_path = os.path.join(output_folder_name, f"{output_folder_name}_EW_velocity.png")
    plt.savefig(velocity_ew_graph_path)
    plt.close()
    print(f"East-West velocity graph saved as '{velocity_ew_graph_path}'.")

    # Plot and save North-South and East-West Acceleration vs. Time graphs
    plt.figure(figsize=(12, 6))
    plt.plot(elapsed_times, accelerations_ns, label='North-South Acceleration', color='red')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Acceleration (km/s²)')
    plt.title('North-South Acceleration vs. Time')
    plt.grid(True)
    acceleration_ns_graph_path = os.path.join(output_folder_name, f"{output_folder_name}_NS_acceleration.png")
    plt.savefig(acceleration_ns_graph_path)
    plt.close()
    print(f"North-South acceleration graph saved as '{acceleration_ns_graph_path}'.")

    plt.figure(figsize=(12, 6))
    plt.plot(elapsed_times, accelerations_ew, label='East-West Acceleration', color='purple')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Acceleration (km/s²)')
    plt.title('East-West Acceleration vs. Time')
    plt.grid(True)
    acceleration_ew_graph_path = os.path.join(output_folder_name, f"{output_folder_name}_EW_acceleration.png")
    plt.savefig(acceleration_ew_graph_path)
    plt.close()
    print(f"East-West acceleration graph saved as '{acceleration_ew_graph_path}'.")

    # Save data to CSV
    csv_path = os.path.join(output_folder_name, f"{output_folder_name}.csv")
    try:
        with open(csv_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                "Elapsed Time (s)", "North-South Displacement (km)", "East-West Displacement (km)",
                "North-South Velocity (km/s)", "East-West Velocity (km/s)",
                "North-South Acceleration (km/s²)", "East-West Acceleration (km/s²)"
            ])
            for i in range(len(elapsed_times)):
                csv_writer.writerow([
                    elapsed_times[i],
                    north_south_displacements[i],
                    east_west_displacements[i],
                    velocities_ns[i],
                    velocities_ew[i],
                    accelerations_ns[i],
                    accelerations_ew[i]
                ])
        print(f"Data has been saved as '{csv_path}'.")
    except Exception as e:
        print(f"An error occurred while saving the CSV file: {e}")

if __name__ == "__main__":
    main()
