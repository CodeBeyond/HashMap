# Name: Allison Butler
# OSU Email: butleall@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/02/22
# Description: Implementation of a HashMap table that uses open addressing for collision resolution.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #
    def get_hash_index(self, key):
        """Helper for put method. Gets the current index in the hash table."""
        hashed_key = self._hash_function(key)
        index = hashed_key % self._capacity  # how to make this str???
        return index

    def put(self, key: str, value: object) -> None:
        """Inserts a value in the hash table. If the value is present, hashes to next open space.
        Otherwise, value is place in the spot originally asked for."""
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        index = self.get_hash_index(key)
        entry = HashEntry(key, value)
        offset = 1
       # tombstone = self._buckets[index].is_tombstone
       # tombstone_check = HashEntry(key, value)
        #da = DynamicArray.get_at_index(tombstone)

        # open addressing
        while self._buckets[index] is not None and self._buckets[index].is_tombstone == False:
       # while self._buckets[index] is not None and tombstone == False:
            # check if we are overwriting an existing key
            if self._buckets[index].key == key:
                self._buckets[index] = entry
                return

            # perform quadratic probing until an empty spot is found
            index = (self._hash_function(key) + offset ** 2) % self._capacity
            offset += 1

        # after while, empty slot is found
        self._buckets[index] = entry
        self._size += 1

    def table_load(self) -> float:
        """
        Calculates the load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the amount of empty buckets
        """
        count = 0
        for i in range(0, self._buckets.length()):
            if self._buckets[i] is None:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
             Resizes the hash table by changing capacity of internal hash table.
             Rehashes all hash table links and key/value pairs stay in the
             new hash map.
             """
        if new_capacity < 1:
            return

        if new_capacity >= 1:
            if self._is_prime(new_capacity) == False:
                new_capacity = self._next_prime(new_capacity)

            # use new capacity to create new, bigger hash map
            hash_map_copy = self._buckets
            self._capacity = new_capacity
            self.clear()

            # iterate over addresses in the hash copy
            for i in range(0, hash_map_copy.length()):
                hash_entry = hash_map_copy.get_at_index(i)
                if hash_entry is not None:
                    self.put(hash_entry.key, hash_entry.value)
            return None

    def get(self, key: str) -> object:
        """
        This method returns the value of a given key. If the key asked for is not in the hash table,
        returns None.
        """
        for i in range(0, self._buckets.length()):
            hash_entry = self._buckets[i]
            if hash_entry is not None:
                if hash_entry.is_tombstone is False:
                    this_key = hash_entry.key
                    if this_key == hash_entry.key:
                        return hash_entry.value
        # outside the traversal

        return None

    def contains_key(self, key: str) -> bool:
        """
        If the key provided is in the hash map, bool of True returned.
        Otherwise, bool of False returned.
        """
        for i in range(0, self._buckets.length()):
            if self._buckets[i] is not None:
                this_item = self._buckets[i].key
                if this_item == key:
                    return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes a key, value pair from the hash map. If the key asked to
        be removed is not in the hash map, returns None.
        """
        for i in range(0, self._buckets.length()):
            if self._buckets[i] is not None:
                if self._buckets[i].is_tombstone == False:
                    self._buckets[i].is_tombstone = True
                    self._size -= 1

    def clear(self) -> None:
        """
        Clears the contents of the hash table.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(DynamicArray())
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        gets the keys and values of the dynamic array.
        """
        result_da = DynamicArray()

        # for chain in hash table
        for i in range(0, self._buckets.length()):
            node = self._buckets[i]
            # for node in chain
            if node is not None and node.is_tombstone is False:
                this_tuple = (node.key, node.value)
                result_da.append(node)
            # end for node
        # end for chain

        return result_da

    #def __iter__(self):
        #"""
        #
       # """
       # pass

    #def __next__(self):
        #"""
        #
        #"""
        #pass

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(20, hash_function_1)
    for i in range(40):
        m.put('str' + str(i), i * 100)
        #if i % 25 == 24:
        print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
"""
    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value) """
