import datetime

BITS = 64
EMACS_LSBITS = 16
MICRO = 1e-6
PICO = 1e-12

LSB_MASK = (1 << EMACS_LSBITS) - 1
MSB_MASK = ~LSB_MASK & ((1 << BITS) -1) # Strip off two's complement

# (current-time) (26095 53160 665501 998000)
ms_bits = 26095
ls_bits = 53160
µ = 665501
pico = 998000

#(26095 << 16) | 53160 & ((1 << 16) - 1 )
#In [93]: (26095 << 16) | 53160 & ((1 << 16) - 1 )
# Out[93]: 1710215080
x = (((ms_bits << EMACS_LSBITS ) & MSB_MASK) | (ls_bits & LSB_MASK) ) + (µ * MICRO) + (pico * PICO)
print( x)
print(datetime.datetime.utcfromtimestamp(x))

# Woot!
#In [285]: datetime.utcfromtimestamp(1710215080)
#Out[285]: datetime.datetime(2024, 3, 12, 3, 44, 40)

