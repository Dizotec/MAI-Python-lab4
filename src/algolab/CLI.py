import sys 
from algolab.recurrent import recurrent
from algolab.sorting import sorting
from algolab.stack import Stack , demo_stack
import argparse
from algolab.generators import generate
from algolab.benchmark import benchmark_recurn_iter, benchmark_recurn_recur , benchmark_sort_quad , benchmark_sort_effect
def main()->None:
    args = sys.argv[1:]
    if args[0] == 'benchmark':
        if args[1] == 'recurrent' :
            if args[2] == '--iter':
                benchmark_recurn_iter(args[3:])
            elif args[2] == '--recur':
                benchmark_recurn_recur(args[3:])
             
        elif args[1] == 'sorting':
            if args[2] == '--quadratic':
                benchmark_sort_quad(args[3:])
            elif args[2] == '--effective':
                benchmark_sort_effect(args[3:])

    elif args[0] == 'recurrent' :
        print(recurrent(args[1],int(args[2]),int(args[3])))
    elif args[0] == 'sorting':
        els = [int(value) for value in args[2:]]
        print(sorting(args[1],els))
    elif args[0] == 'struct':
        demo_stack()
    elif args[0] == "generate":
        parser = argparse.ArgumentParser(prog="algolab generate")

        parser.add_argument(
            "--kind",
            choices=["random", "sorted", "reverse", "almost-sorted", "duplicates"],
            required=True,
        )
        parser.add_argument("--size", type=int, required=True)
        parser.add_argument("--seed", type=int, default=None)

        options = parser.parse_args(args[1:])

        print(generate(options.kind, options.size , options.seed))
        
    