def quadratic(els:list):
    els_copy = els.copy() 
    for i in range(len(els_copy)-1):
        for j in range(len(els_copy)-1-i):
            if els_copy[j] > els_copy[j+1] :
                tmp = els_copy[j]
                els_copy[j] = els_copy[j+1]
                els_copy[j+1] = tmp
    
    return els_copy 

def merge(left,right):
    result = [] 
    i = 0 
    j = 0 
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i+=1
        else:
            result.append(right[j])
            j+=1
    result.extend(left[i:])
    result.extend(right[j:])
    return result 
        
def effective(els:list):
    els_copy = els.copy() 
    mid = len (els ) // 2
    if len(els_copy) <= 1 :
        return els_copy
    left = effective(els[:mid])
    right = effective(els[mid:])
    return merge(left, right)


def sorting(method : str , els: list):
    
    if method == '--quadratic':
        return quadratic(els)
    if method == '--effective':
        return effective(els)
