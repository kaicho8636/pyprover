# pyprover
A Python-based theorem prover  
Only intuitionistic propositional logic is supported now.

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
| ->     | implies |
| /\\    | and     |
| \\/    | or      |
| ~      | not     |


### Tactics
n : assumption number
- assumption()
- intro()
- apply(n)
- split()
- left()
- right()
- destruct(n)

### Basic example
![](example.png)

