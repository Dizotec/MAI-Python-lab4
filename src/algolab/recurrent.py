
def iter(value:int ,degree : int )->int:
    result = 1.0
    while  degree > 0:
        if degree %2 == 1:
            result *= value
        value *= value 
        degree //=2
    return result 
def recur(value:int , degree:int ) -> int:
    if degree == 0 :
        return 1 
    if degree % 2 ==0 :
        return recur(value * value , degree //2)
    else:
        return recur(value,degree-1) * value

def recurrent(method:str, value: int , degree: int ) -> int:
    if method == '--iter':
        return iter(value,degree)
    elif method == '--recur':
        return recur(value,degree)