import sys 
from algolab.recurrent import recurrent
from algolab.sorting import sorting
def main()->None:
    args = sys.argv[1:]
    if args[0] == 'recurrent' :
        print(recurrent(args[1],int(args[2]),int(args[3])))
    elif args[0] == 'sorting':
        els = [int(value) for value in args[2:]]
        print(sorting(args[1],els))
    
    