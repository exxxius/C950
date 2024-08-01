import datetime
from Distance import find_shortest_path
from csvReader import (get_package_hash_table, package_list, read_csv_files)

address_file_path = 'CSV/Addresses.csv'
distance_file_path = 'CSV/Distances.csv'
address_dict, distance_dict = read_csv_files(address_file_path, distance_file_path)


# This function prints the package deadlines for each truck.
# The time complexity is O(T * P) where T is the number of trucks and P is the number of packages.
# The space complexity is O(1)
def print_truck_deadlines(trucks):
    for i, truck in enumerate(trucks, start=1):
        print(f"Truck {i} delivery deadlines:")
        for package in truck:
            print(f"Package ID: {package[0]}, Deadline: {package[6]}")
        print()


# The overall time complexity is O(n * log(n) + n^2). Since n^2 dominates the expression, the complexity can be O(n^2).
# The space complexity is O(n).
def allocate_packages_to_trucks(packages_list):
    print("Allocating packages to trucks function has started.")
    truck1 = []
    truck2 = []
    truck3 = []
    trucks = [truck1, truck2, truck3]
    # Sort packages based on their deadlines
    packages_list.sort(key=lambda x: x[6])

    # Helper function to check if the truck has space left
    def has_space_left(truck):
        return len(truck) < 16
    # Update EOD deadlines to 17:00 assuming that the official end of the day is 5:00 PM
    for package in packages_list:
        if package[6] == "EOD":
            package[6] = "17:00:00"
    # First, allocate packages with specific constraints
    for package in packages_list:
        if "Wrong address listed" in package[8]:
            truck3.append(package)
            print(f"Package {package[0]} has been allocated to truck 3 due to a wrong address listed.")
            print(truck3)

        elif "Can only be on truck 2" in package[8]:
            truck2.append(package)
            print(f"Package {package[0]} has been allocated to truck 2 due to 'Can only be on truck 2' constraint.")

        elif "Delayed" in package[8]:
            print(f"Package {package[0]} has been allocated to truck 3 due to a delay.")
            truck3.append(package)

    # Then, allocate packages with "Must be delivered with" constraint
    for package in packages_list:
        if package[8].startswith("Must be delivered with"):
            package_ids = package[8][21:].split(" & ")
            related_packages = [p for p in packages_list if p[0] in package_ids]
            all_packages = [package] + related_packages

            if all(p[0] not in [pkg[0] for pkg in truck1 + truck2 + truck3] for p in all_packages):
                if has_space_left(truck1) and len(truck1) + len(all_packages) <= 16:
                    truck1.extend(all_packages)
                elif has_space_left(truck2) and len(truck2) + len(all_packages) <= 16:
                    truck2.extend(all_packages)
                elif has_space_left(truck3) and len(truck3) + len(all_packages) <= 16:
                    truck3.extend(all_packages)

    # Allocate remaining packages, prioritizing those with a deadline
    for package in packages_list:
        if package[0] not in [pkg[0] for pkg in truck1 + truck2 + truck3]:
            if "17:00:00" not in package[6] and has_space_left(truck1):
                truck1.append(package)
            elif "17:00:00" not in package[6] and has_space_left(truck2):
                truck2.append(package)
            elif "17:00:00" not in package[6] and has_space_left(truck3):
                truck3.append(package)

    for package in packages_list:
        if package[0] not in [pkg[0] for pkg in truck1 + truck2 + truck3]:
            if has_space_left(truck1):
                truck1.append(package)
            elif has_space_left(truck2):
                truck2.append(package)
            elif has_space_left(truck3):
                truck3.append(package)

    # Sort packages based on delivery deadlines
    truck1.sort(key=lambda x: x[6])
    truck2.sort(key=lambda x: x[6])
    truck3.sort(key=lambda x: x[6])

    print_truck_deadlines([truck1, truck2, truck3])
    print("Allocating packages to trucks function has finished.")
    return [truck1, truck2, truck3]


# lists of packages allocated to each truck.
allocated_trucks_packages = allocate_packages_to_trucks(package_list)

print("distance_dict: ", distance_dict)
trucks_with_paths = find_shortest_path(allocated_trucks_packages, address_dict, distance_dict)
print("Trucks with paths: ", trucks_with_paths)
print("address_dict: ", address_dict)


# Rev 4/6/2023 - Prints allocated package info for each truck
for i, truck in enumerate(allocated_trucks_packages):
    print(f"Truck {i+1} Packages:")
    print("Package ID, Address Index, Address, City, State, Zip, Deadline, Weight, Notes, Departure Time, Delivery Status")
    for package in truck:
        print(package)
    print()

# Rev 4/6/2023 - Prints path, distances, and delivery times from trucks_with_paths for each truck
for i, truck in enumerate(trucks_with_paths):
    print(f"Truck {i+1} Path:")
    print("Path:", truck["path"])
    print("Distances:", truck["distances"])
    print("Times:", [t.strftime("%H:%M:%S") for t in truck["times"]])
    print()


# Rev1 - 4/7/2023 Update package info with truck departure times and delivery times for each package in each truck
# Time complexity is O(T * V * P) where T is the number of trucks, V the number of vertices, and P number of packages.
# Space complexity is O(V) where V is the number of vertices.
def update_package_info(allocated_truck_packages, trucks_paths_input, addresses_dict):
    for truck_index, truck_info in enumerate(trucks_paths_input):
        path = truck_info['path']
        delivery_times = [delivery_time.strftime('%H:%M:%S') for delivery_time in truck_info['times']]
        truck_departure_time = delivery_times[0]

        for address_index, delivery_time in zip(path, delivery_times):
            current_address = addresses_dict[address_index]
            for current_package in allocated_truck_packages[truck_index]:  # For each package in the current truck
                package_address = current_package[2]  # The address is in the second position in the package_info list
                if package_address == current_address[1]:
                    current_package[1] = address_index  # Update the address index
                    current_package[9] = truck_departure_time   # Update the truck departure time
                    current_package[10] = delivery_time # [10:]   Update the delivery time
    return allocated_truck_packages


# Rev1- 4/7/2023 Update the package information in the hashtable
# Time complexity is O(T * P) where T is the number of trucks and P number of packages.
# Space complexity is O(1)
def update_packages_hashtable(allocated_truck_packages, packages_hashtable):
    for truck_packages in allocated_truck_packages:
        for package in truck_packages:
            package_id = package[0]
            truck_departure_time = package[9]
            delivery_time = package[10]

            # Look up the package information in the hashtable
            current_package = packages_hashtable.lookup(package_id)
            if current_package:
                # Update the package information
                current_package[9] = truck_departure_time
                current_package[10] = delivery_time

                # Update the hashtable using the update function
                packages_hashtable.update(package_id, current_package)
    return packages_hashtable


print("Allocated Trucks Packages: ", allocated_trucks_packages)

# Call the update_package_info function
updated_allocated_truck_packages = update_package_info(allocated_trucks_packages, trucks_with_paths, address_dict)
print("UPDATED allocated_truck_packages: ", updated_allocated_truck_packages)


# Update the packages hashtable
update_packages_hashtable(updated_allocated_truck_packages, get_package_hash_table())


# Print the packages hashtable
# Time complexity is O(n)
# Space complexity is O(1)
def print_hashtable(hashtable):
    print("Packages Hash Table: ")
    for bucket in hashtable.map:
        for pair in bucket:
            print(pair)


print_hashtable(get_package_hash_table())
