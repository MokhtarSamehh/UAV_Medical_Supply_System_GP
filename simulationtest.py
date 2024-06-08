import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

class Flight:
    def __init__(self, flight_number, departure_airport, destination_airport, departure_time, arrival_time):
        self.flight_number = flight_number
        self.departure_airport = departure_airport
        self.destination_airport = destination_airport
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.current_position = None

class FlightSchedule:
    def __init__(self):
        self.flights = []

    def add_flight(self, flight):
        self.flights.append(flight)

    def generate_flight(self, flight_number, departure_airport, destination_airport, start_time, end_time):
        departure_time = start_time + timedelta(minutes=random.randint(0, (end_time - start_time).total_seconds() // 60))
        flight_duration = random.randint(60, 600)  # Random duration in minutes
        arrival_time = departure_time + timedelta(minutes=flight_duration)
        flight = Flight(flight_number, departure_airport, destination_airport, departure_time, arrival_time)
        self.add_flight(flight)

    def plot_flight_progression(self, start_time, end_time):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

        ax.set_extent([-130, -65, 20, 55])  # Adjust map extent to focus on the continental US
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.STATES.with_scale('50m'))

        for flight in self.flights:
            dep_lat, dep_lon = airports[flight.departure_airport]
            dest_lat, dest_lon = airports[flight.destination_airport]
            flight.current_position = (dep_lat, dep_lon)
            ax.plot([dep_lon, dest_lon], [dep_lat, dest_lat], transform=ccrs.PlateCarree(), linewidth=1, color='b')

        for current_time in range((end_time - start_time).seconds // 60):
            for flight in self.flights:
                if flight.departure_time <= start_time + timedelta(minutes=current_time) <= flight.arrival_time:
                    dep_lat, dep_lon = airports[flight.departure_airport]
                    dest_lat, dest_lon = airports[flight.destination_airport]
                    interp_lat = dep_lat + (dest_lat - dep_lat) * (current_time / (flight.arrival_time - flight.departure_time).total_seconds() // 60)
                    interp_lon = dep_lon + (dest_lon - dep_lon) * (current_time / (flight.arrival_time - flight.departure_time).total_seconds() // 60)
                    flight.current_position = (interp_lat, interp_lon)
            
            for flight in self.flights:
                if flight.current_position:
                    ax.plot(flight.current_position[1], flight.current_position[0], marker='o', markersize=5, color='r', transform=ccrs.PlateCarree())

            plt.title('Flight Progression')
            plt.pause(0.1)
            plt.clf()

# Define airport coordinates
airports = {
    "JFK": (40.6413, -73.7781),  # JFK International Airport
    "LAX": (33.9416, -118.4085)  # Los Angeles International Airport
}

# Example usage
flight_schedule = FlightSchedule()
start_time = datetime(2024, 4, 20, 8, 0)  # Start time for random departure time calculation
end_time = datetime(2024, 4, 20, 20, 0)    # End time for random departure time calculation

for i in range(10):  # Generate 10 flights
    flight_schedule.generate_flight(
        flight_number=f"ABC{i}",
        departure_airport="JFK",
        destination_airport="LAX",
        start_time=start_time,
        end_time=end_time
    )

flight_schedule.plot_flight_progression(start_time, end_time)