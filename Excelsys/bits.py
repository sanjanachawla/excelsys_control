# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
print("Hello world")
number = 0b1011010001111010
#hex_number =0x5d
#print(bin(number[0:5]))

# getting your message as int
#i = int(hex_number, 16)#

# getting bit at position 28 (counting from 0 from right)
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val  

# getting bits at position 24-27
#print(bin((number >> 24) & 0b111))
print(bin(number))
mantessa = (bin((number>>0)&0b11111111111)) #from left
exponent = (bin((number>>11)&0b11111))
print(mantessa)
print(exponent)
mantessa_val = twos_comp(int(mantessa, 2), 11)
exponent_val = twos_comp(int(exponent, 2), 5)
print("mantessa_val= ", mantessa_val)
print("exponent_val =" , exponent_val)

final_val = mantessa_val * 2^(exponent_val)
print(final_val)