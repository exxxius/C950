import csv
from typing import Tuple, Dict

from Hashtable import HashTable


# Function to return address and distance dictionaries.
# Time complexity: O(V^2) where V is the number of vertices.
# Space complexity: O(V^2) where V is the number of vertices.
def read_csv_files(addresses_file_path: str, distances_file_path: str) -> Tuple[Dict[int, Tuple[str, str]], Dict[Tuple[int, int], float]]:
    addresses_dict = {}
    with open(addresses_file_path, newline='') as address_file:
        reader = csv.reader(address_file)
        for row in reader:
            addresses_dict[int(row[0])] = (row[1], row[2])

    distances_dict = {}
    with open(distances_file_path, newline='') as distance_file:
        reader = csv.reader(distance_file)
        for i, row in enumerate(reader):
            for j, val in enumerate(row):
                if val.strip() and float(val) != 0:
                    distances_dict[(i, j)] = float(val)

    return addresses_dict, distances_dict


# Reads the packages.csv file and returns a hash table of packages with the package ID as the key and the package info
# as the value.
with open('csv\Packages.csv') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')

    package_hash_table = HashTable()
    package_list = []

    for row in csv_reader:
        package_ID = row[0]
        address = row[1]
        city = row[2]
        state = row[3]
        zip_code = row[4]
        delivery_deadline = row[5]
        size = row[6]
        special_note = row[7]
        delivery_start = ''
        address_location = ''
        delivery_status = 'At the hub'
        package_info = [package_ID, address_location, address, city, state,
                        zip_code, delivery_deadline, size, special_note, delivery_start,
                        delivery_status]

        package_list.append(package_info)

    for package_info in package_list:
        key = package_info[0]
        value = package_info
        package_hash_table.insert(key, value)


# returns the package hash table
# Time Complexity: O(1)
# Space Complexity: O(1)
def get_package_hash_table():
    return package_hash_table




