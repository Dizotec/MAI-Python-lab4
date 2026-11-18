import random
def rand_gener(size : int , seed : int ) -> list:
    result = []
    rng = random.Random(seed)
    for i in range(size):
        result.append(rng.randint(-1000,1000))
    return result 
def sorted_gener(size:int) -> list:
    result = list(range(size))
    return result 
def reverse_gener(size:int)-> list:
    result = list(range(size - 1, -1, -1))
    return result 
def almost_sorted_gener(size: int , seed:int)->list:
    result = list(range(size))
    if size <= 1:
        return result
    rng = random.Random(seed)
    swaps = max(1, size // 20)# пусть 5 процентов 
    swap_indexes = []
    for i in range(swaps): 
        swap_indexes.append(rng.randint(0,size -2 ))
    for i in swap_indexes:
        if i != len(result)-1:
            tmp = result[i]
            result[i] = result[i+1]
            result[i+1] = tmp 
    return result 
def duplicates_gener(size: int , seed:int)->list:
    result = list(range(size))
    if size <= 1:
        return result
    rng = random.Random(seed)
    swaps = max(1, size // 5) # пусть 20 процентов 
    swap_indexes = []
    for i in range(swaps): 
        swap_indexes.append(rng.randint(0,size -2 ))
    for i in swap_indexes:
        if i != len(result)-1:
            
            result[i] = result[i+1]
            
    return result 


def generate(kind , size , seed ):
    if kind == 'random':
        return rand_gener(size,seed)
    if kind == 'sorted':
        return sorted_gener(size)
    if kind == 'reverse':
        return reverse_gener(size)
    if kind == 'almost-sorted':
        return almost_sorted_gener(size,seed )
    if kind == 'duplicates':
        return duplicates_gener(size,seed )
    