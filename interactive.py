import readline
from prover import Prover
from proposition import PropParseTree, parser as prop_parser


def main():
    prop_parse_tree = PropParseTree()
    while True:
        try:
            goal = prop_parse_tree.transform(prop_parser.parse(input('Proposition? < ')))
        except Exception as e:
            print(e)
        else:
            break
    prover = Prover(goal)
    tactic_dict = {
        "undo": (prover.undo, 0),
        "intro": (prover.intro, 0),
        "assumption": (prover.assumption, 0),
        "apply": (prover.apply, 1),
        "left": (prover.left, 0),
        "right": (prover.right, 0),
        "destruct": (prover.destruct, 1),
        "specialize": (prover.specialize, 2),
        "add_dn": (prover.add_dn, 0)
    }
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
        tactics = input('pyprover < ')
        if not tactics:
            continue
        for tactic in tactics.split(";"):
            words = tactic.split()
            if not words:
                continue
            elif words == ['auto']:
                if results := prover.auto():
                    for result in results:
                        print(f'auto: {result}')
                else:
                    print(f'auto: tactic failed(Could not find proof)')
            elif words[0] not in tactic_dict:
                print(f'{tactic}: invalid tactic')
                continue
            elif len(words)-1 != tactic_dict[words[0]][1]:
                print(f'{tactic}: {tactic_dict[words[0]][1]} argument(s) expected but given {len(words)-1}')
                continue
            elif not all(map(lambda arg: arg.isdigit(), words[1:])):
                print(f'{tactic}: invalid argument(s)')
                continue
            elif tactic_dict[words[0]][0](*map(int, words[1:])):
                print(f'{tactic}: tactic failed')


if __name__ == '__main__':
    main()
