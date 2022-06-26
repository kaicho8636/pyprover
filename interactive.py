from prover import Prover
from proposition import parser as prop_parser


def main():
    while True:
        prover = Prover(prop_parser.parse(input('Proposition? < ')))
        while True:
            if prover.goal is None:
                print('No more goals.')
                print()
                break
            else:
                if not prover.subgoals:
                    print('1 goal')
                else:
                    print(f'{len(prover.subgoals)+1} goals')
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
