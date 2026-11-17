from math import pow 
def iter(value:int ,degree : int )->int:
    result = 1.0
    while  degree > 0:
        if degree %2 == 1:
            result *= value
        value *= value 
        degree //=2
    return result 
def recur(value , degree ) -> int:
    if degree == 0:
        return 1 
    half = recur(value, degree // 2)
    if degree %2 !=0 :
        return value * half * half
    if degree %2 ==0 :
        return half * half 

def recurrent(type:str, value: int , degree: int ) -> int:
    if type == '--iter':
        return iter(value,degree)
    elif type == '--recur':
        return recur(value,degree)