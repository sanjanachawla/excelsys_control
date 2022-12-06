#from convert_data import convert_data
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
    s = serial.Serial('COM12', 2400, parity=serial.PARITY_NONE, timeout = 10)
    print("connected to COM12 STM")
except:
    print("failed to connect to STM")

SLV_ADDR = 0x51
slots = [1]
PAGE_1 = [SLV_ADDR, 0x00, 0x01, 0x00, 0x01, 0X01]
PAGE_2 = [SLV_ADDR, 0x00, 0x01, 0x00, 0x02, 0X02]
PAGE_3 = [SLV_ADDR, 0x00, 0x01, 0x00, 0x03, 0X03]
EN_ON =  [SLV_ADDR, 0x00, 0x01, 0x01, 0x80, 0x80]
EN_OFF = [SLV_ADDR, 0x00, 0x01, 0x01, 0x00, 0X00]
VOUT =   [SLV_ADDR, 0x00, 0x02, 0x21, 0x33, 0x06]# [slv_adr, read/write, length, mem_addr, lsb, msb] #need to make this arrays for each commandj
                                     # 1= read, 0 = write
READ_V = [SLV_ADDR, 0x01, 0x02, 0x8B, 0x0, 0x0]
READ_EN =[SLV_ADDR, 0x01, 0x01, 0x01, 0x00, 0x00]
TEST = [0x08, 0x07, 0x06]


#cannot read the control commands. have to see what is enabled a diff way.

num_bytes = 2;
command_data = VOUT
for j in range (0, 1): 
    send_command = ""
    for i in command_data:
        send_command = send_command + chr(i) #converting commanddata to char? the command to send
    hex = "".join("{:02X}".format(ord(c)) for c in send_command) # print hex representation
    print("send comm= ", send_command)

    while(1):
        try:
            print("send comm= ", send_command)
            s.write(send_command)
            print("command written")
        except:
            print("not able to send")
        time.sleep(1)
        reply = s.read(2)
        print("reply = ", reply)
        if reply:
            hex = "".join("{:02X}".format(ord(c)) for c in reply) # print hex representation of string
            if(num_bytes ==2):
                #byte come in reversed order
                print(hex)
                hex_swap = []
                hex = list(hex)
                hex_swap[0:1] = hex[2:4]
                hex_swap[2:3] = hex[0:2]
                hex_str = "".join(hex_swap)
                #print(hex_str)

                reply_data = int(hex_str, 16)
                val = Decimal(reply_data)/Decimal(pow(2, 8))
                print(" reply val = ", val)
            else:
                print("reply = ", reply)
                reply_data = int(hex, 16)
                val = Decimal(reply_data)/Decimal(pow(2, 8))
                print(" reply val = ", val)


 