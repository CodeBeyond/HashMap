# Name: Allison Butler
# OSU Email: butleall@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/02/22
# Description: Implementation of a HashMap table that uses separate chaining for collision resolution.


from a6_include import (DynamicArray, LinkedList, SLNode,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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

    def print_it(self):
        for index in range(0, self._buckets.length()):
            asdf = self._buckets[index]
            li = []
            node = asdf._head
            while node:
                li.append((node.key, node.value))
                node = node.next
            print(li)

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
        """
        Updates the key/value pair in a HashMap. If the key provided is already
        in the Hash Map, it's value is replaced by another value. If that
        key is not in the map, it will then be added.
        """
       # print("Putting key: " + str(key) + " val: " + str(value))
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        index = self.get_hash_index(key)
        #print(index)

        ll_chain = self._buckets[index]
        # if length of this chain is 0 then this is the first element being added to this address
        #if ll_chain.length() == 0:
            #print("Element is added to new chain")
            #ll_chain.insert(key, value)
            #self._buckets[index] = ll_chain
            #self._size += 1

        if ll_chain.contains(key):
            ll_chain.remove(key)
            ll_chain.insert(key, value)
            self._buckets.set_at_index(index, ll_chain)
        else:
            ll_chain.insert(key, value)
            self._buckets.set_at_index(index, ll_chain)
            self._size += 1

        if ll_chain.length() == 0:
            # print("Element is added to new chain")
            ll_chain.insert(key, value)
            self._buckets[index] = ll_chain
            self._size += 1


    def empty_buckets(self) -> int:
        """
        Returns the amount of empty buckets in the table.
        """
        empty_count = 0

        for i in range(0, self._buckets.length()):
            chain = self._buckets[i]
            if chain.length() == 0:
                empty_count += 1

        return empty_count

    def table_load(self) -> float:
        """Returns table load."""
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the hash table. The has table capacity is not
        effected.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table by changing capacity of internal hash table.
        Rehashes all hash table links and key/value pairs stay in the
        new hash map.
        """
        #print("Enter resize_table")





        if new_capacity < 1:
            return



            #  If new_capacity is 1 or more, make sure it is a prime number. If not, change it to the next
            # highest prime number. You may use the methods _is_prime() and C from the
            # skeleton code.
        if new_capacity >= 1:
            if self._is_prime(new_capacity) == False:
                new_capacity = self._next_prime(new_capacity)

                # use new capacity to create new, bigger hash map
            hash_map_copy = self._buckets
            self._capacity = new_capacity
            self.clear()

            # make deep copy - where????
            
            # iterate over addresses in the hash copy
            for i in range(0, hash_map_copy.length()):
                #chain = hash_map_copy[i]
                chain = hash_map_copy.get_at_index(i)
                # iterate over every node in this chain
                for key_val in chain:
                    key = key_val.key
                    val = key_val.value

                    self.put(key, val)


    def get(self, key: str):
        """
        This method returns the value of a given key. If the key asked for is not in the hash table,
        returns None.
        """

        for i in range(0, self._buckets.length()):
            chain = self._buckets[i]
            for key_val in chain:
                this_key = key_val.key
                if this_key == key:
                    return key_val.value
        # outside the traversal
        return None

    def contains_key(self, key: str) -> bool:
        """
        If the key provided is in the hash map, bool of True returned.
        Otherwise, bool of False returned.
        """
        for i in range(0, self._buckets.length()):
            chain = self._buckets[i]
            for key_val in chain:
                this_key = key_val.key
                if this_key == key:
                    return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes a key, value pair from the hash map. If the key asked to
        be removed is not in the hash map, returns None.
        """
        index = self.get_hash_index(key)

        ll_chain = self._buckets.get_at_index(index)

        if ll_chain is not None:
            for node in ll_chain:
                if node.key == key:
                    ll_chain.remove(key)
                    self._size -= 1
        else:
            return None
       # index = self._hash_function(key)
       # if self._buckets[index] is None:
            #return None
       # ll = self._buckets[index]
        #ll2 = []

        #for node in ll:
            #if str(node.key) is not str(key):
                #ll2.append(node)
        #self._buckets[index] = None

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a Dynamic Array of all key/value pairs in hash map in
        tuple form. Order does not matter.
        """
        result_da = DynamicArray()

        # for chain in hash table
        for i in range(0, self._buckets.length()):
            chain = self._buckets[i]
            # for node in chain
            for key_val in chain:
                this_key = key_val.key
                this_value = key_val.value
                this_tuple = (this_key, this_value)

                result_da.append(this_tuple)
            # end for node
        # end for chain
        return result_da

#def find_mode(da: DynamicArray) -> (DynamicArray, int):
    #"""
    #Receives a Dynamic array that is either sorted or not sorted. Returns
    #a tuple if the most occurring item in the dynamic array, and the frequency
    #that item occurred in the array (integer).
    #"""
    # if you'd like to use a hash map,
     # use this instance of your Separate Chaining HashMap
    #map = HashMap()


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(4, hash_function_1)
    for i in range(15):
        m.put('str' + str(i), i * 100)
        if i % 4 == 0:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

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

    print("nPDF - resize example 1")
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

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
        
