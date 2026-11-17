import sys 
from algolab.recurrent import recurrent
def main()->None:
    args = sys.argv[1:]
    if args[0] == 'recurrent' :
        print(recurrent(args[1],int(args[2]),int(args[3])))
    