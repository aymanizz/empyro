from random import randint
from itertools import starmap

from empyro import color
from empyro.color import Color
from empyro.terminals.surface import SurfaceTerminal

# generated using https://www.ascii-art-generator.org/
text = r"""
_|_|_|_|  _|      _|  _|_|_|    _|      _|  _|_|_|      _|_|
_|        _|_|  _|_|  _|    _|    _|  _|    _|    _|  _|    _|
_|_|_|    _|  _|  _|  _|_|_|        _|      _|_|_|    _|    _|
_|        _|      _|  _|            _|      _|    _|  _|    _|
_|_|_|_|  _|      _|  _|            _|      _|    _|    _|_|
""".strip().splitlines()

print(*text, sep='\n')

terminal = SurfaceTerminal((max([len(s) for s in text]), len(text)))

for y, line in enumerate(text):
    for x, char in enumerate(line):
        fg, bg = starmap(
            Color, [[randint(0, 255) for _ in range(3)] for _ in range(2)])
        if char == ' ':
            bg = color.BLACK
        terminal.write(' ', (x, y), fg, bg)

terminal.render()
input('Press enter to exit.')
