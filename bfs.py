import heapq

class EvacuationRoute:
    def __init__(self):
        self.graph = {}  # Graph representation {location: [(neighbor, risk), ...]}

    def add_road(self, location, neighbor, flood_risk, traffic_delay):
        """ Adds a road between two locations with flood risk and traffic weight """
        weight = flood_risk + traffic_delay  # Higher weight means riskier route
        if location not in self.graph:
            self.graph[location] = []
        if neighbor not in self.graph:
            self.graph[neighbor] = []
        self.graph[location].append((neighbor, weight))
        self.graph[neighbor].append((location, weight))  # Undirected graph

    def bfs_safest_route(self, start, destination):
        """ Finds the safest and shortest route using BFS with a priority queue """
        priority_queue = [(0, start, [])]  # (Total risk, current location, path)
        visited = set()

        while priority_queue:
            total_risk, current, path = heapq.heappop(priority_queue)
            
            if current in visited:
                continue
            visited.add(current)
            path = path + [current]

            if current == destination:
                return path, total_risk  # Return the safest path and its risk level

            for neighbor, risk in self.graph.get(current, []):
                if neighbor not in visited:
                    heapq.heappush(priority_queue, (total_risk + risk, neighbor, path))

        return None, float("inf")  # No path found

# Initialize the evacuation route system
evacuation = EvacuationRoute()

# Fully connected locations
evacuation.add_road("UP Dorm", "New Science Building", 1, 2)
evacuation.add_road("UP Dorm", "Canteen", 2, 3)
evacuation.add_road("UP Dorm", "Library", 4, 2)
evacuation.add_road("UP Dorm", "Kiosks", 3, 2)

evacuation.add_road("Canteen", "Library", 1, 2)
evacuation.add_road("Canteen", "New Science Building", 2, 2)
evacuation.add_road("Canteen", "Kiosks", 2, 1)

evacuation.add_road("New Science Building", "Kiosks", 3, 3)
evacuation.add_road("New Science Building", "Library", 2, 3)

evacuation.add_road("Kiosks", "Library", 1, 2)

# Connecting locations to all evacuation sites
evacuation.add_road("UP Dorm", "Parking Lot near UP Dorm", 1, 1)
evacuation.add_road("New Science Building", "Parking Lot near UP Dorm", 2, 1)
evacuation.add_road("Canteen", "Open Field near Library & Canteen", 1, 1)
evacuation.add_road("Kiosks", "Open Field near Library & Canteen", 2, 1)
evacuation.add_road("Library", "Open Field near Library & Canteen", 1, 1)

# Extra connections for full connectivity
evacuation.add_road("Parking Lot near UP Dorm", "Open Field near Library & Canteen", 3, 2)
evacuation.add_road("Basketball Court near SOM", "Open Field near Library & Canteen", 2, 1)
evacuation.add_road("Basketball Court near SOM", "Parking Lot near UP Dorm", 2, 2)
evacuation.add_road("Library", "Basketball Court near SOM", 2, 1)

# Mapping user choices
locations = {
    "A": "UP Dorm",
    "B": "Canteen",
    "C": "New Science Building",
    "D": "Kiosks",
    "E": "Library"
}

# Nearest evacuation sites (Now fully connected)
evacuation_sites = {
    "UP Dorm": "Parking Lot near UP Dorm",
    "New Science Building": "Parking Lot near UP Dorm",
    "Canteen": "Open Field near Library & Canteen",
    "Kiosks": "Open Field near Library & Canteen",
    "Library": "Open Field near Library & Canteen"
}

# User input validation
while True:
    user_choice = input("Choose your starting point (A-UP Dorm, B-Canteen, C-New Science Building, D-Kiosks, E-Library): ").strip().upper()
    
    if user_choice in locations:
        start_location = locations[user_choice]
        break
    else:
        print("Invalid input! Please enter A, B, C, D, or E.")

# Determine evacuation route
destination = evacuation_sites[start_location]
path, risk = evacuation.bfs_safest_route(start_location, destination)

# Display result
print(f"\n🚨 Evacuation Route from {start_location} to {destination}:")
print(f"➡️ {' → '.join(path)}")
print(f"⚠️ Total Risk Level: {risk}")
