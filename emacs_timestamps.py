
BITS = 64
EMACS_LSBITS = 16

LSB_MASK = (1 << EMACS_LSBITS) - 1
MSB_MASK = ~LSB_MASK & ((1 << BITS) -1) # Strip off two's complement


# Captured values in the wild - ignore picos and nanos for now.
# (current-time) (26095 53160 665501 998000)
ms_bits = 26095
ls_bits = 53160

#(26095 << 16) | 53160 & ((1 << 16) - 1 )
#In [93]: (26095 << 16) | 53160 & ((1 << 16) - 1 )
# Out[93]: 1710215080

print( ( (ms_bits << EMACS_LSBITS ) & MSB_MASK) | ls_bits & LSB_MASK)
