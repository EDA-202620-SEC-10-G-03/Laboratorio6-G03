from random import randint
from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll
from DataStructures.Map import map_entry as me



def new_map(num_elements, load_factor, prime=109345121):
    capacity = mf.next_prime(num_elements/load_factor)
    scale = randint(1, prime-1)
    shift = randint(0, prime-1)
    table = al.new_list()
    for i in range(capacity):
        al.add_last(table, sll.new_list())
    current_factor = 0
    limit_factor = load_factor
    size = 0
    
    return {"prime": prime, "capacity": capacity, "scale": scale, "shift": shift, "table": table, "current_factor": current_factor, "limit_factor": limit_factor, "size" : size}


def default_compare(key, element):

   if (key == me.get_key(element)):
      return 0
   elif (key > me.get_key(element)):
      return 1
   return -1


def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    if my_map["size"] == 0:
        return True
    else:
        return False

def rehash(my_map):
    return my_map

def put(my_map, key, value):
    posicion = mf.hash_value(my_map, key)
    lista = al.get_element(my_map["table"], posicion)
    pos = sll.is_present(lista, key, default_compare)
    if pos != -1:
        entry = sll.get_element(lista, pos)
        me.set_value(entry, value)
    else:
        sll.add_last(lista,(me.new_map_entry(key, value)))
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"]/my_map["capacity"]
        if my_map["current_factor"] > my_map["limit_factor"]:
            my_map = rehash(my_map)
    
    return my_map

def contains(my_map, key):
    posicion = mf.hash_value(my_map, key)
    lista = al.get_element(my_map["table"], posicion)
    pos = sll.is_present(lista, key, default_compare)
    if pos != -1:
        return True
    else:
        return False
    
def get(my_map, key):
    posicion = mf.hash_value(my_map, key)
    lista = al.get_element(my_map["table"], posicion)
    pos = sll.is_present(lista, key, default_compare)
    if pos != -1:
        entry = sll.get_element(lista, pos)
        return me.get_value(entry)
    else:
        return None

def remove(my_map, key):
    posicion = mf.hash_value(my_map, key)
    lista = al.get_element(my_map["table"], posicion)
    pos = sll.is_present(lista, key, default_compare)
    
    if pos != -1:
        sll.delete_element(lista, pos)
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"]/my_map["capacity"]
    return my_map
    
def key_set(my_map):
    resultado = al.new_list()
    for i in range(my_map["capacity"]):
        lista = al.get_element(my_map["table"], i)
        for j in range(sll.size(lista)):
            entry = sll.get_element(lista, j)
            al.add_last(resultado, me.get_key(entry))
    return resultado

def value_set(my_map):
    resultado = al.new_list()
    for i in range(my_map["capacity"]):
        lista = al.get_element(my_map["table"], i)
        for j in range(sll.size(lista)):
            entry = sll.get_element(lista, j)
            al.add_last(resultado, me.get_value(entry))
    return resultado
    
def rehash(my_map):
    nuevo_mapa = new_map(2 * my_map["capacity"], 1, my_map["prime"])
    nuevo_mapa["limit_factor"] = my_map["limit_factor"]

    for i in range(my_map["capacity"]):
        lista = al.get_element(my_map["table"], i)
        for j in range(sll.size(lista)):
            entry = sll.get_element(lista, j)
            put(nuevo_mapa, me.get_key(entry), me.get_value(entry))

    my_map["capacity"] = nuevo_mapa["capacity"]
    my_map["scale"] = nuevo_mapa["scale"]
    my_map["shift"] = nuevo_mapa["shift"]
    my_map["current_factor"] = nuevo_mapa["current_factor"]
    my_map["table"] = nuevo_mapa["table"]
    return my_map