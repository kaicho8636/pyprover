# pyprover
A Python-based theorem prover

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

### Basic example
![](example.png)


### Tactics
n : assumption number
- assumption()
- intro()
- apply(n)
- split()
- left()
- right()
- destruct(n)
