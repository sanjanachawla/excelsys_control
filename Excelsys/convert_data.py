#assume it comes in as a binary array, figure out data formatting later 
from tokenize import Exponent

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val  

#converts data to readable int format from the incoming data format
def lin_to_int(command, data, vout_mode):
    #vout_mode = -8
    print(data)
    format = command["data format"]
    if(format == 'lin'):
       # print(bin(data))
        mantessa = (bin((data>>0)&0b11111111111)) #shifts from left in str format
        exponent = (bin((data>>11)&0b11111))
        #print("mantessa = ", mantessa)
        #print("exponent = ", exponent)
        mantessa_val = twos_comp(int(mantessa, 2), 11)
        exponent_val = twos_comp(int(exponent, 2), 5)
        #print("mantessa_val= ", mantessa_val)
        #print("exponent_val =" , exponent_val)
        converted_data = mantessa_val * pow(2,exponent_val)
        #print(converted_data)
        return converted_data

    if(format == 'ex lin'):
        #print(bin(data))
        mantessa = (bin((data>>0)&0b1111111111111111)) #shifts from left in str format
        #exponent = (bin((data>>11)&0b11111))
        mantessa_val = twos_comp(int(mantessa, 2), 11)
        exponent_val = -8
        #print("mantessa_val= ", mantessa_val)
        #print("exponent_val =" , exponent_val)
        converted_data = mantessa_val * 2^(exponent_val)
   # if (format == 'unasigned binary int'):
    #    1
    #if(format == 'read block'):
    #    1
   # if(format == 'read byte'):
    #    1
    converted_data = data
    return converted_data

def int_to_lin(command, arg, vout_mode):
    format = command["data format"]
    #print("format = ", format)
    if(format == 'ex lin'):
        #1. convert arg to ext lin by /vout mode
        float_ext_lin = arg/vout_mode
        hex_cmd = "".join("{:04X}".format((int(float_ext_lin))) )
        byte_0 = int(hex_cmd[2:4], 16)
        #send_command.append(byte_0)
        byte_1 = int(hex_cmd[0:2], 16)
        #send_command.append(byte_1)
        #print(byte_0, byte_1)
        return byte_0, byte_1
