from enum import StrEnum, auto
class DisplayType(StrEnum):
    a_real = 'real part of a'
    a_img = 'imaginary part of a'
    b_real = 'real part of b'
    b_img = 'imaginary part of b'
    phase_diff_1= 'phase difference a-b'
    phase_diff_2= 'phase difference b-a'
    UNKNOWN = auto()
