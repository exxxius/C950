import csv
import datetime
import heapq
from datetime import timedelta


# Rev1
# This function returns the index of an address in the addresses dictionary.
# Time complexity: O(V) where V is the number of vertices in the graph.
# Space complexity: O(1)
def find_location_index_by_address(address, addresses_dict):
    for index, (_, location_address) in addresses_dict.items():
        if location_address == address:
            return index
    return None


# Dijkstra algorithm for finding the shortest path from a start node to all other nodes in a graph.
# Overall time complexity of the Dijkstra's algorithm is O((V + E) log(V)).
# Overall space complexity is O(V).
def dijkstra(graph, start):
    shortest_paths = {start: 0}
    unvisited_nodes = [(0, start)]
    visited_nodes = set()

    while unvisited_nodes:
        current_min_distance, current_node = heapq.heappop(unvisited_nodes)
        if current_node not in visited_nodes:
            visited_nodes.add(current_node)
            for neighbor, distance in graph[current_node].items():
                new_distance = current_min_distance + distance
                if neighbor not in shortest_paths or new_distance < shortest_paths[neighbor]:
                    shortest_paths[neighbor] = new_distance
                    heapq.heappush(unvisited_nodes, (new_distance, neighbor))
    return shortest_paths


# Updates the address of package 9 to the correct address.
# Time complexity: O(1)
# Space complexity: O(1)
def update_package9_info(package_info, corrected_package9_address):
    if package_info[0] == "9":
        package_info[2] = corrected_package9_address[0]
        package_info[5] = corrected_package9_address[3]
    return package_info


# Finds the shortest path for each truck and returns a list of addresses for each truck, a list of distances for each
# truck, and a list of arrival times (delivery times) for each truck. It also updates the address of package 9 to the
# correct address when the current_time is 10:20 AM. The path of each truck starts from the hub and ends at the hub.
# So, the distance from the last package of each truck is included in calculation of total distances of all trucks.
# Time complexity: O(TP + V^2 + TP(V^2 log V)) T is the number of trucks, P is the number of packages, and V is the
# number of vertices in the graph.
# Space complexity: O(V^2 + TP) where T is the number of trucks, P is the number of packages, and V is the number of
# vertices in the graph.
def find_shortest_path(allocated_trucks, addresses_dict, distances_dict):
    hub_address = "4001 South 700 East"
    hub_index = find_location_index_by_address(hub_address, addresses_dict)

    corrected_package9_address = ["410 S State St", "Salt Lake City", "UT", "84111"]

    packages_dict = {}
    deadlines_dict = {}
    trucks_with_paths = []

    # Average speed of trucks is 18 miles per hour.
    SPEED_LIMIT = 18

    for truck in allocated_trucks:
        for package_info in truck:
            package_info = update_package9_info(package_info, corrected_package9_address)
            package_id = package_info[0]
            package_address = package_info[2]
            deadline = package_info[6]
            index = find_location_index_by_address(package_address, addresses_dict)
            packages_dict[package_id] = package_address
            deadlines_dict[index] = datetime.datetime.strptime(deadline, "%H:%M:%S")

    graph = {}
    for (index1, index2), distance in distances_dict.items():
        if index1 not in graph:
            graph[index1] = {}
        if index2 not in graph:
            graph[index2] = {}
        graph[index1][index2] = distance
        graph[index2][index1] = distance

    departure_times = [datetime.datetime.strptime("08:00:00", "%H:%M:%S")] * 2

    for truck_index, truck in enumerate(allocated_trucks):
        if truck_index == 2:
            earliest_arrival_time = min(trucks_with_paths[0]['times'][-1], trucks_with_paths[1]['times'][-1])
            departure_times.append(earliest_arrival_time)

        current_time = departure_times[truck_index]

        path = [hub_index]
        path_distances = []
        path_times = [current_time]
        remaining_packages = [package_info[0] for package_info in truck]

        while remaining_packages:
            last_location_index = path[-1]
            shortest_paths = dijkstra(graph, last_location_index)

            min_distance = float("inf")
            next_location_index = None
            next_package_id = None
            for package_id in remaining_packages:
                package_index = find_location_index_by_address(packages_dict[package_id], addresses_dict)
                if package_index is not None and shortest_paths[package_index] < min_distance:
                    new_time = current_time + timedelta(hours=shortest_paths[package_index] / SPEED_LIMIT)
                    if new_time <= deadlines_dict[package_index]:
                        min_distance = shortest_paths[package_index]
                        next_location_index = package_index
                        next_package_id = package_id

            if next_location_index is not None:
                path.append(next_location_index)
                remaining_packages.remove(next_package_id)
                current_time = current_time + timedelta(hours=min_distance / SPEED_LIMIT)

                key = (last_location_index, next_location_index)
                reversed_key = (next_location_index, last_location_index)
                if key in distances_dict:
                    path_distances.append(distances_dict[key])
                elif reversed_key in distances_dict:
                    path_distances.append(distances_dict[reversed_key])
                elif key == reversed_key:
                    path_distances.append(0)
                else:
                    raise KeyError(f"Both key {key} and {reversed_key} not found in distances_dict")

                path_times.append(current_time)
            else:
                print("No next location found. Remaining packages:", remaining_packages)
                break

        path.append(hub_index)
        path_distances.append(distances_dict[(path[-2], hub_index)])
        trucks_with_paths.append({"path": path, "distances": path_distances, "times": path_times})
    return trucks_with_paths


# Rev 4/6/2023 gets distances for each truck and total distance for all trucks from trucks_with_paths
# Time complexity: O(T) where T is the number of trucks.
# Space complexity: O(T) where T is the number of trucks.
def get_distances(trucks):
    truck_distances = []
    total_distance = 0

    for truck in trucks:
        distance_sum = sum(truck['distances'])
        truck_distances.append(distance_sum)
        total_distance += distance_sum

    return truck_distances, total_distance
