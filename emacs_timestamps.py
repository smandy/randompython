
BITS = 64

LSB_MASK = (1 << 16) - 1
MSB_MASK = ~LSB_MASK & ((1 << 64) -1) # Strip off two's complement

ms_bits = 26095
ls_bits = 53160

#(26095 << 16) | 53160 & ((1 << 16) - 1 )

#In [93]: (26095 << 16) | 53160 & ((1 << 16) - 1 )
# Out[93]: 1710215080

print( ( (ms_bits << 16 )  & MSB_MASK) | ls_bits & LSB_MASK)
