from enum import StrEnum, auto
class DisplayType(StrEnum):
    a_real = 'Real part of a'
    a_imag = 'Imaginary part of a'
    a_abs = 'Absolute value of a'
    b_real = 'Real part of b'
    b_imag = 'Imaginary part of b'
    b_abs = 'Absolute value of b'
    phase_a= 'Argument a'
    phase_b= 'Argument b'
    phase_difference_ba = 'phase difference b-a'
    phase_difference_ab = 'phase difference a-b'
    #UNKNOWN = auto()
