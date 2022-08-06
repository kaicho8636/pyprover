import readline
from prover import Prover
from proposition import PropParseTree, parser as prop_parser


def main():
    prop_parse_tree = PropParseTree(set(input('Proposition variables? < ').split()))
    while True:
        try:
            goal = prop_parse_tree.transform(prop_parser.parse(input('Proposition? < ')))
        except Exception as e:
            print(e)
        else:
            break
    prover = Prover(goal)
    while True:
        if prover.goal is None:
            print('No more goals.')
            print()
            break
        else:
            print(f'{len(prover.subgoals)+1} goal{"s" if prover.subgoals else ""}')
            print()
            for i, v_type in enumerate(prover.variables):
                print(f'  H{i} : {str(v_type)}')
            print('  ============================')
            print(f'  {prover.goal}')
            print()
            for i, goal in enumerate(prover.subgoals):
                print(f'goal {i+2} is:')
                print(goal[0])
                print()
        eval('prover.' + input('pyprover < '))


if __name__ == '__main__':
    main()
