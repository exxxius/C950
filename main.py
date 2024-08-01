# # # Author: Mehdi Rahimi
# # # Date: 04//08/2023
# # # Student ID: 001510177
# #
from csvReader import get_package_hash_table as get_hash_table
from Package import trucks_with_paths
from Distance import get_distances
import datetime


class PackageTracker:
    @staticmethod
    # Since the address of Package #9 changes after 10:20 in the hash table, this method
    # shows the initial wrong address before 10:20, just for display purposes.
    # Time complexity: O(1) - Mainly limited by the 'get_hash_table' method.
    # Space complexity: O(1) - Determined by the called methods.
    def initial_package_9_address(input_time, package):
        updated_package = package.copy()
        if package[0] == '9' and input_time < datetime.timedelta(hours=10, minutes=20):
            updated_package[2] = '300 State St'
            updated_package[5] = '84103'
        return updated_package

    @staticmethod
    # Function to display mileage for each truck
    # Time complexity: O(1)The function takes constant time to execute, regardless of the input size.
    # Space complexity: O(1) - The function uses a constant amount of additional memory.
    def display_truck_mileage():
        truck_number = int(input("Enter the truck number (1, 2, or 3): "))
        if truck_number not in [1, 2, 3]:
            print("Invalid truck number. Please enter 1, 2, or 3.")
            return
        truck_total_distances, _ = get_distances(trucks_with_paths) # Replace the existing function call
        print(f"Total mileage for Truck {truck_number}: {truck_total_distances[truck_number - 1]} miles")

    @staticmethod
    # This function displays the program's main menu and calls the corresponding functions based on user input.
    def main_menu():
        # Welcome message and display total route distance
        print('<<<*** Welcome to the WGUPS Delivery Service ***>>>')
        _, total_distance = get_distances(trucks_with_paths) # Replace the existing function call
        print('Total distance of all routes is: ', "{0:.2f}".format(total_distance, 2), 'miles.')

        while True:
            print("\nDisplaying main menu")
            option = input("=================================================="
                           "\n 1 - Track a single Package"
                           "\n 2 - View Delivery Status for all packages"
                           "\n 3 - Display total mileage for each truck"
                           "\n 4 - Exit"
                           "\n Please select an option: ")

            # Execute the corresponding function based on user input
            if option == '1':
                PackageTracker.track_package()
            elif option == '2':
                PackageTracker.view_delivery_status()
            elif option == '3':
                PackageTracker.display_truck_mileage()
            elif option == '4':
                print("Exiting the program...")
                break
            else:
                print("Invalid input, please try again.")

    # static method for the main menu to track a single package
    @staticmethod
    # Time complexity: O(N) - Where N is the number of packages
    # Space complexity: O(1) - Uses a few variables to store intermediate results
    def track_package():
        try:
            pkg_id = input('Please enter a package ID to lookup: ')
            pkg_status_time = input('Please enter a time in the HH:MM format: ')

            if get_hash_table().lookup(str(pkg_id)) is None:
                raise ValueError("Invalid Package ID")

            original_pkg = get_hash_table().lookup(str(pkg_id))
            pkg = original_pkg.copy()
            first_time = pkg[9]
            print("first time: ", first_time)
            second_time = pkg[10]

            try:
                (h, m) = pkg_status_time.split(':')
                user_time = datetime.timedelta(hours=int(h), minutes=int(m))
                # Update the address for package 9 if the time is after 10:20
                pkg = PackageTracker.initial_package_9_address(user_time, original_pkg)

            except ValueError:
                raise ValueError("Invalid Time Format")

            (h, m, s) = str(first_time).split(':')
            first_time_converted = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            (h, m, s) = str(second_time).split(':')
            second_time_converted = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            # Update package status based on user-provided time
            if first_time_converted >= user_time:
                pkg[10] = 'At Hub'
                pkg[9] = '\nLeaves at ' + first_time
            elif first_time_converted <= user_time:
                if user_time < second_time_converted:
                    pkg[10] = 'En Route'
                    pkg[9] = 'Left at ' + str(first_time)
                else:
                    pkg[10] = 'Delivered at ' + second_time
                    pkg[9] = '\nLeft at ' + str(first_time)

            # Display package information
            print('Package ID:', pkg[0], '\nStreet address:',
                  pkg[2], pkg[3], pkg[4], pkg[5],
                  '  Delivery deadline:', pkg[6],
                  '\nPackage weight:', pkg[7], '\nTruck status:',
                  pkg[9], '\nDelivery status:',
                  pkg[10])

        except ValueError as e:
            print(str(e))

    # static method for the main menu to view delivery status for all packages
    @staticmethod
    # Time complexity: O(N) - Where N is the number of packages
    # Space complexity: O(N) - Creates a table to store package information
    def view_delivery_status():
        try:
            time_input = input('Please enter a time (HH:MM) : ')
            (h, m) = time_input.split(':')
            input_time = datetime.timedelta(hours=int(h), minutes=int(m))

            table_data = []

            for count in range(1, 41):
                original_pkg = get_hash_table().lookup(str(count))
                pkg = original_pkg.copy()

                # Check if the package ID is 9 and the input time is 10:20 or later
                pkg = PackageTracker.initial_package_9_address(input_time, pkg)
                package_info = [pkg[0], f"{pkg[2]}, {pkg[3]}, {pkg[4]}, {pkg[5]}", pkg[6], pkg[7]]

                try:
                    time_one = pkg[9]
                    time_two = pkg[10]
                    time_one_str = str(time_one)
                    (h, m, s) = time_one_str.split(':')
                    convert_time_one = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    time_two_str = str(time_two)
                    (h, m, s) = time_two_str.split(':')
                    convert_time_two = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

                except ValueError:
                    pass

                # Update package status based on input time
                if convert_time_one >= input_time:
                    package_info.append("At Hub")
                    package_info.append("At Hub")
                elif convert_time_one <= input_time:
                    if input_time < convert_time_two:
                        package_info.append("En Route")
                        package_info.append("Left at " + str(time_one))
                    else:
                        package_info.append("Delivered")
                        package_info.append("Delivered at " + str(time_two))
                else:
                    package_info.append("Unknown")
                    package_info.append("Unknown")
                table_data.append(package_info)

            # Set column widths for table display
            col_widths = [max(len(str(max(col, key=lambda x: len(str(x))))) for col in zip(*table_data)) for _ in
                          range(6)]
            col_widths[0] = len("Package ID")
            col_widths[2] = len("Delivery Deadline")
            col_widths[3] = len("Package Weight")
            col_widths[4] = len("Truck Status")
            col_widths[5] = len("Delivery Status")

            header = ["Package ID", "Address", "Delivery Deadline", "Package Weight", "Truck Status", "Delivery Status"]

            # Print table header
            for i, h in enumerate(header):
                print(h.ljust(col_widths[i] + 1), end="")
            print("\n" + "-" * (sum(col_widths) + len(col_widths) + 5))

            # Print table rows
            for row in table_data:
                for i, col in enumerate(row):
                    print(col.ljust(col_widths[i] + 1), end="")
                print()

        except IndexError:
            print("Error: Invalid package index")
        except ValueError:
            print('Invalid Time')


if __name__ == '__main__':
    tracker = PackageTracker()
    tracker.main_menu()
