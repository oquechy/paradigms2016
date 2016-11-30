from unittest.mock import MagicMock
from model import Read, Number

if __name__ == '__main__':
    r = Read('a')
    r.evaluate = MagicMock(return_value=42)
    print(r.evaluate())
