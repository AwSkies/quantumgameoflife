from enum import StrEnum, auto
class ColorMode(StrEnum):
    A_MOD = '|a|'
    A_PHASE= 'arg(a)'
    B_ABS = '|b|'
    B_PHASE= 'arg(b)'
    DELTA_PHASE_BA = 'arg(b / a)'
    DELTA_PHASE_AB = 'arg(a / b)'
    CONST = 'Constant'