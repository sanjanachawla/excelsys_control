from convert_data import convert_data
#import excelsys_commands as cc
#import excelsys_control as control
import time
import math
import decimal
from decimal import *
# Global variables
global inputVoltage
global inputCurrent 
global modTemps
global outputVoltages
global outputCurrents
global outputPowers
global reply
global inputTextVars
global status
global outputButtons
global light
global units
global pb
global progressWindow
global loggingButton
global loggingText
global gi
global vout_mode
import serial
try:
    s = serial.Serial('COM9', 2400, parity=serial.PARITY_NONE, timeout = 10)
    print("connected to COM9 STM")
except:
    print("failed to connect to STM")

slots = [1];
PAGE_1 = [0x00, 0x01]
EN_1 = [0x01, 0x80]

num_bytes = 2;
while (1): 
    reply = s.read(num_bytes)
    #print("reply = ", reply) #this is a string
    #hex = "".join("{:02X}".format(ord(c)) for c in reply) # print hex representation of string
    #print("hex = ", hex) #sting
    #reply_data = [int(hex[i:i+2],16) for i in range(0, len(hex), 2)] #list of reply ints
  
    if reply:
        hex = "".join("{:02X}".format(ord(c)) for c in reply) # print hex representation of string
        if(num_bytes >= 2):
            #hex_swap = [hex[2], hex[3], hex[0], hex[1]]
            #hex_swap = "".join("{:02X}".format(ord(c)) for c in hex_swap)
            #print(hex_swap)

        reply_data = int(hex, 16)
        #print("reply = ", reply) #this is a string
        #need to swap order of bytes

        print("hex = ", hex) #sting
        #print("reply_data_int = ", reply_data) #list of reply ints
        val = Decimal(reply_data)/Decimal(pow(2, 8))
        print("val = ", val)
   
   
