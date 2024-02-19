masks = [0x7F, 0x1F, 0x0F, 0x07]

for example in [0x3f,0xC0, 0x80, 0xE0, 0xF0] + masks:
    print(f"{example:>02x} = {example:>08b}")

def utf8_to_code_point(byte_sequence):
    # Determine the number of bytes used for the character
    num_bytes = len(byte_sequence)
    
    # Determine the bitmask for extracting the bits representing the character
    bitmask = masks[num_bytes - 1]
    
    # Extract the bits representing the character from the byte sequence
    code_point = byte_sequence[0] & bitmask
    print(f"Byte is {byte_sequence[0]:>08b}")
    for byte in byte_sequence[1:]:
        print(f"Byte is {byte:>08b}")
        code_point = (code_point << 6) | (byte & 0x3F)
    
    return code_point

# 3f = 00111111 -> Mask to strip of 2 bit 'extension byte header'
# c0 = 11000000 -> Mask for start of two byte message
# e0 = 11100000 -> Mask for start of three byte messag
# f0 = 11110000 -> Mark for start of four byte message
# 80 = 10000000 -> Mask for an declaring extension byte - 'or' me with remaining 0x3f

# 7f = 01111111 -> Bitmask for byte 1 of 1 byte message - header = 0 - i.e. 7 bit ascii
# 1f = 00011111 -> Bitmask for byte 1 of 2 byte message - header = 110
# 0f = 00001111 -> Bitmask for byte 1 of 3 byte message - header = 1110
# 07 = 00000111 -> Bitmask for byte 1 of 4 byte message - header = 11110

def code_point_to_utf8(code_point):
    if code_point < 0x80:
        return bytes([code_point])
    elif code_point < 0x800:
        byte1 = 0xC0 | (code_point >> 6)
        byte2 = 0x80 | (code_point & 0x3F)
        return bytes([byte1, byte2])
    elif code_point < 0x10000:
        byte1 = 0xE0 | (code_point >> 12)
        byte2 = 0x80 | ((code_point >> 6) & 0x3F)
        byte3 = 0x80 | (code_point & 0x3F)
        return bytes([byte1, byte2, byte3])
    elif code_point < 0x110000:
        byte1 = 0xF0 | (code_point >> 18)
        byte2 = 0x80 | ((code_point >> 12) & 0x3F)
        byte3 = 0x80 | ((code_point >> 6) & 0x3F)
        byte4 = 0x80 | (code_point & 0x3F)
        return bytes([byte1, byte2, byte3, byte4])
    else:
        raise ValueError("Invalid code point")

# Example usage:
code_point = 0x65E5  # Unicode code point for character 日
byte_sequence = code_point_to_utf8(code_point)
print("UTF-8 byte sequence:", byte_sequence)


# Example usage:
byte_sequence = b'\xE6\x97\xA5'  # UTF-8 byte sequence representing the character 日
byte_sequence = b'\xEF\xBB\xBF'  # UTF-8 BOM
code_point = utf8_to_code_point(byte_sequence)
print(f"Code point: {hex(code_point)} {code_point:>16b}")

print("Reverse decode", code_point_to_utf8(code_point))
