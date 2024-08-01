# This is the Hash Table Class. It's self-adjusting, so it will rehash itself when the load factor is reached.
# Space Complexity: O(n), where n is the number of key-value pairs
class HashTable:
    def __init__(self, initial_capacity=10, load_factor=0.75):
        self.map = [[] for _ in range(initial_capacity)]
        self.load_factor = load_factor
        self.size = 0

    # This is the hash function. It takes a key and returns an index.
    # Time Complexity: O(1)
    def _hash(self, key):
        return int(key) % len(self.map)

    # This is the insert function. It takes a key and a value and inserts them into the hash table.
    # Average Time Complexity: O(1) (amortized)
    # Worst Time Complexity: O(n) (due to rehashing)
    def insert(self, key, value):
        if self.size + 1 > len(self.map) * self.load_factor:
            self._rehash()

        index = self._hash(key)
        key_value = [key, value]

        if not self.map[index]:
            self.map[index] = [key_value]
            self.size += 1
            return True

        for pair in self.map[index]:
            if pair[0] == key:
                pair[1] = value
                return True

        self.map[index].append(key_value)
        self.size += 1
        return True

    # This is the rehash function. It doubles the size of the hash table and rehashes all the keys.
    # Time Complexity: O(n), where n is the number of key-value pairs
    def _rehash(self):
        old_map = self.map
        self.map = [[] for _ in range(len(old_map) * 2)]
        self.size = 0

        for bucket in old_map:
            for pair in bucket:
                self.insert(pair[0], pair[1])

    # This is the lookup function. It takes a key and returns the value associated with it.
    # Average Time Complexity: O(1)
    # Worst Time Complexity: O(n) (due to bucket collisions)
    def lookup(self, key):
        index = self._hash(key)
        if self.map[index]:
            for pair in self.map[index]:
                if pair[0] == key:
                    return pair[1]
        return None

    # This is the update function. It takes a key and a value and updates the value associated with the key.
    # Average Time Complexity: O(1)
    # Worst Time Complexity: O(n) (due to bucket collisions)
    def update(self, key, value):
        index = self._hash(key)
        updated = False
        if self.map[index]:
            for pair in self.map[index]:
                if pair[0] == key:
                    pair[1] = value
                    updated = True
                    break

        if not updated:
            self.insert(key, value)

        return updated

    # This is the remove function. It takes a key and removes the key-value pair from the hash table.
    # Average Time Complexity: O(1)
    # Worst Time Complexity: O(n) (due to bucket collisions)
    def remove(self, key):
        index = self._hash(key)

        if not self.map[index]:
            return False

        for i, pair in enumerate(self.map[index]):
            if pair[0] == key:
                self.map[index].pop(i)
                return True
        return False

    # Add this method to your HashTable class
    def to_list(self):
        package_list = []
        for bucket in self.map:
            for pair in bucket:
                package_list.append(
                    pair[1])  # Assuming the package information is stored as the value in the key-value pair
        return package_list


# It takes a hash table and converts it into a graph. This is used for the Dijkstra's algorithm. Revision
def convert_hashtable_to_graph(hashtable):
    graph = {}

    for location1, distances in hashtable.items():
        graph[location1] = {}
        for location2, distance in distances.items():
            graph[location1][location2] = distance
    return graph
