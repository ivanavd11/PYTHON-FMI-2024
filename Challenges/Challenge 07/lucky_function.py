from secret import clue

ZERO = 0 
LEFT_SHIFT_BITS = 5
RIGHT_SHIFT_BITS = 5
BW_AND_MASK = 16
BW_OR_MASK = 247  
BW_OR_RESULT = 255  
FIFTH_BIT_POSITION = 4  
FOURTH_BIT_POSITION = 3

def lucky():
    address = ZERO

    high_bits = clue(left_shift=LEFT_SHIFT_BITS) >> LEFT_SHIFT_BITS
    address |= high_bits 

    low_bits = clue(right_shift=RIGHT_SHIFT_BITS) << RIGHT_SHIFT_BITS
    address |= low_bits 

    fifth_bit = clue(bw_and=BW_AND_MASK)
    address |= ((fifth_bit != ZERO) << FIFTH_BIT_POSITION)

    fourth_bit = clue(bw_or=BW_OR_MASK)
    address |= ((fourth_bit == BW_OR_RESULT) << FOURTH_BIT_POSITION)

    return address
