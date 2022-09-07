# pyprover
A simple theorem prover, which has a coq-like interactive interface and supports classical logic.

## Usage
### Create venv & Install requirements
```shell
pip3 install virtualenv
git clone https://github.com/kaicho8636/pyprover.git
cd pyprover
virtualenv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

### Interactive session
```shell
python3 interactive.py
```

### Propositional symbols
| Symbol | Name    |
|--------|---------|
| →, ->  | implies |
| ∧, /\\ | and     |
| ∨, \\/ | or      |
| ¬, ~   | not     |


### Tactics
m, n : assumption number
- assumption
- intro
- apply n
- specialize m n
- split
- left
- right
- destruct n
- add_dn
- auto (This tactic only supports intuitionistic logic)

You can also use 'undo'

### Basic example
```
Proposition variables? < p r s
Proposition? < (p->r\/s)->((p->r)\/(p->s))
1 goal

  ============================
  ((p → (r ∨ s)) → ((p → r) ∨ (p → s)))

pyprover < intro
1 goal

  H0 : (p → (r ∨ s))
  ============================
  ((p → r) ∨ (p → s))

pyprover < add_dn
1 goal

  H0 : (p → (r ∨ s))
  ============================
  ((((p → r) ∨ (p → s)) → False) → False)

pyprover < intro
1 goal

  H0 : (p → (r ∨ s))
  H1 : (((p → r) ∨ (p → s)) → False)
  ============================
  False

pyprover < apply 1
1 goal

  H0 : (p → (r ∨ s))
  H1 : (((p → r) ∨ (p → s)) → False)
  ============================
  ((p → r) ∨ (p → s))

pyprover < left
1 goal

  H0 : (p → (r ∨ s))
  H1 : (((p → r) ∨ (p → s)) → False)
  ============================
  (p → r)

pyprover < intro
1 goal

  H0 : (p → (r ∨ s))
  H1 : (((p → r) ∨ (p → s)) → False)
  H2 : p
  ============================
  r

pyprover < specialize 0 2
1 goal

  H0 : (r ∨ s)
  H1 : (((p → r) ∨ (p → s)) → False)
  H2 : p
  ============================
  r

pyprover < destruct 0
2 goals

  H0 : r
  H1 : (((p → r) ∨ (p → s)) → False)
  H2 : p
  ============================
  r

goal 2 is:
r

pyprover < assumption
1 goal

  H0 : s
  H1 : (((p → r) ∨ (p → s)) → False)
  H2 : p
  ============================
  r

pyprover < add_dn
1 goal

  H0 : s
  H1 : (((p → r) ∨ (p → s)) → False)
  H2 : p
  ============================
  ((r → False) → False)

pyprover < intro
1 goal

  H0 : s
  H1 : (((p → r) ∨ (p → s)) → False)
  H2 : p
  H3 : (r → False)
  ============================
  False

pyprover < apply 1
1 goal

  H0 : s
  H1 : (((p → r) ∨ (p → s)) → False)
  H2 : p
  H3 : (r → False)
  ============================
  ((p → r) ∨ (p → s))

pyprover < right
1 goal

  H0 : s
  H1 : (((p → r) ∨ (p → s)) → False)
  H2 : p
  H3 : (r → False)
  ============================
  (p → s)

pyprover < intro
1 goal

  H0 : s
  H1 : (((p → r) ∨ (p → s)) → False)
  H2 : p
  H3 : (r → False)
  H4 : p
  ============================
  s

pyprover < assumption
No more goals.
```

