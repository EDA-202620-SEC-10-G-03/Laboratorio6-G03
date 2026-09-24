from DataStructures.List import array_list as lt
import random as r
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.Map import map_functions as mp
def new_map(num_elements, load_factor, prime=109345121):
    
    capacity = mf.next_prime(num_elements/load_factor)
    scale = r.randint(1, prime-1)
    shift = r.randint(0, prime-1)
    table = lt.new_list(capacity)
    
    for i in range(capacity):
        lt.add_last(table, None)
    
    return {"table": table, "capacity": capacity, "size": 0, "limit_factor": load_factor, "current_factor": 0, "scale": scale, "shift": shift}

def put(my_map, key, value):

    hash_value = mf.hash_value(my_map, key)

    found, pos = find_slot(my_map, key, hash_value)

    if found:
        entry = lt.get_element(my_map["table"], pos)
        me.set_value(entry, value)

    else:
        entry = me.new_map_entry(key, value)
        lt.change_info(my_map["table"], pos, entry)

        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

        if my_map["current_factor"] > my_map["limit_factor"]:
            my_map = rehash(my_map)

    return my_map


def contains(my_map, key):

    hash_value = mf.hash_value(my_map, key)

    found, pos = find_slot(my_map, key, hash_value)

    return found
    

def get(my_map, key):

    hash_value = mf.hash_value(my_map, key)

    found, pos = find_slot(my_map, key, hash_value)

    if not found:
        return None

    entry = lt.get_element(my_map["table"], pos)
    return me.get_value(entry)


def remove(my_map, key):

    hash_value = mf.hash_value(my_map, key)

    found, pos = find_slot(my_map, key, hash_value)

    if found:
        entry = me.new_map_entry("__EMPTY__", "__EMPTY__")
        lt.change_info(my_map["table"], pos, entry)
        my_map["size"] -= 1

    return my_map

def size(my_map):
    return my_map["size"]
