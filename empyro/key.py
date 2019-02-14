"""The keycodes used by the terminal for signaling input.

Note that the backend used might not signal all control keys.
"""

from functools import wraps
from typing import NamedTuple
from enum import IntEnum

# FUTURE: Support more keys, add event handling, mainly key up and down events.
class KeyCode(IntEnum):
    # control keys
    SPACE = 32
    TAB = 9
    ENTER = 13
    BACKSPACE = 8
    DELETE = 127
    ESCAPE = 27

    # arrows
    UP = 273
    DOWN = 274
    RIGHT = 275
    LEFT = 276

    # numbers
    ZERO = 48
    ONE = 49
    TWO = 50
    THREE = 51
    FOUR = 52
    FIVE = 53
    SIX = 54
    SEVEN = 55
    EIGHT = 56
    NINE = 57

    # letters
    A = 97
    B = 98
    C = 99
    D = 100
    E = 101
    F = 102
    G = 103
    H = 104
    I = 105
    J = 106
    K = 107
    L = 108
    M = 109
    N = 110
    O = 111
    P = 112
    Q = 113
    R = 114
    S = 115
    T = 116
    U = 117
    V = 118
    W = 119
    X = 120
    Y = 121
    Z = 122

    # symbols
    SEMICOLON = 59
    EQUALS = 61
    COMMA = 44
    HYPHEN = 45
    PERIOD = 50
    SLASH = 51
    BACKTICK = 52
    LEFTBRACKET = 53
    BACKSLASH = 54
    RIGHTBRACKET = 55
    APOSTROPHE = 56

    @property
    def name(self) -> chr:
        # numbers
        if self in range(KeyCode.ZERO, KeyCode.NINE + 1):
            return chr(ord('0') + self - KeyCode.ZERO)
        # symbols
        if self in range(KeyCode.SEMICOLON, KeyCode.APOSTROPHE + 1):
            return _symbols_names[self]
        # control keys
        if self == KeyCode.SPACE:
            return ' '
        if self == KeyCode.TAB:
            return '    '
        # letters, numbers and other control characters
        return super().name

    @property
    def is_control(self) -> bool:
        return self in range(KeyCode.SPACE, KeyCode.ESCAPE + 1)


class KeyMod(IntEnum):
    NO_MOD = 0
    CTRL = 1
    SHIFT = 2
    ALT = 4


Key = NamedTuple('Key', [('code', KeyCode), ('mod', KeyMod)])

_symbols_names = {
    KeyCode.SEMICOLON: ';',
    KeyCode.EQUALS: '=',
    KeyCode.COMMA: ',',
    KeyCode.HYPHEN: '-',
    KeyCode.PERIOD: '.',
    KeyCode.SLASH: '/',
    KeyCode.BACKTICK: '`',
    KeyCode.LEFTBRACKET: '[',
    KeyCode.BACKSLASH: '\\',
    KeyCode.RIGHTBRACKET: ']',
    KeyCode.APOSTROPHE: "'",
}
