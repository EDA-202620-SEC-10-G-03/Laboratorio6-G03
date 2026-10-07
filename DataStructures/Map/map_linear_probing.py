from random import randint
from DataStructures.Map import map_functions as mf
from DataStructures.Map import map_entry as me
from DataStructures.List import array_list as al


def new_map(num_elements, load_factor, prime=109345121):
    
    capacity = mf.next_prime(num_elements/load_factor)
    scale = randint(1, prime-1)
    shift =  randint(0, prime-1)
    table = al.new_list()
    for i in range(capacity):
        entry = me.new_map_entry(None, None)
        al.add_last(table, entry)
    current_factor = 0
    limit_factor = load_factor
    size = 0

    diccionario = {"prime": prime, "capacity": capacity, "scale": scale, "shift": shift, "table": table, "current_factor": current_factor, "limit_factor": limit_factor, "size": size}

    return diccionario


def rehash(my_map):
    nuevo_mapa = new_map(2*my_map["capacity"],1, my_map["prime"])
    nuevo_mapa["limit_factor"] = my_map["limit_factor"]
    for i in range(my_map["capacity"]):
        if not is_available(my_map["table"],i):
            entry = al.get_element(my_map["table"],i)
            put(nuevo_mapa, me.get_key(entry), me.get_value(entry))
    
    my_map["capacity"] = nuevo_mapa["capacity"]
    my_map["scale"] = nuevo_mapa["scale"]
    my_map["shift"] = nuevo_mapa["shift"]
    my_map["current_factor"] = nuevo_mapa["current_factor"]
    my_map["table"] = nuevo_mapa["table"]
    return my_map


def put(my_map, key, value):
    posicion = mf.hash_value(my_map, key)
    a, b = find_slot(my_map, key, posicion)
    if not a:
        entry = me.new_map_entry(key, value)
        al.change_info(my_map["table"], b, entry)
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"]/my_map["capacity"]
        if my_map["current_factor"] > my_map["limit_factor"]:
            my_map = rehash(my_map)   
    else:
        entry = al.get_element(my_map["table"], b)
        me.set_value(entry, value)
    return my_map


def contains(my_map, key):
    posicion = mf.hash_value(my_map, key)
    a, b = find_slot(my_map,key, posicion)
    return a


def get(my_map, key):
    posicion = mf.hash_value(my_map, key)
    a, b = find_slot(my_map, key, posicion)
    if not a:
        return None
    else:
        elemento = al.get_element(my_map["table"], b)
        valor = me.get_value(elemento)
        return valor    


def remove(my_map, key):
    posicion = mf.hash_value(my_map, key)
    a, b = find_slot(my_map, key, posicion)
    if a:
        entry = me.new_map_entry("__EMPTY__","__EMPTY__")
        al.change_info(my_map["table"], b, entry)
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"]/my_map["capacity"]
    
    return my_map
    
    
def size(my_map):
    return my_map["size"]


def is_available(table, pos):

   entry = al.get_element(table, pos)
   if me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__":
      return True
   return False


def default_compare(key, entry):

   if key == me.get_key(entry):
      return 0
   elif key > me.get_key(entry):
      return 1
   return -1


def find_slot(my_map, key, hash_value):
   first_avail = None
   found = False
   ocupied = False
   while not found:
      if is_available(my_map["table"], hash_value):
            if first_avail is None:
               first_avail = hash_value
            entry = al.get_element(my_map["table"], hash_value)
            if me.get_key(entry) is None:
               found = True
      elif default_compare(key, al.get_element(my_map["table"], hash_value)) == 0:
            first_avail = hash_value
            found = True
            ocupied = True
      hash_value = (hash_value + 1) % my_map["capacity"]
   return ocupied, first_avail