from re import S
from socket import timeout
from sre_constants import SUCCESS
import serial
import numpy as np
from datetime import datetime 
import os
import csv
import socket
import time 
import convert_data as cd
from decimal import *

# Establish connection to serial port (Excelsys power supply via STM32)
#for testing and understanding, lets print out what we are sending 
#try:
#     # Sending over usb
#s = serial.Serial('COM12', 2400, parity=serial.PARITY_NONE, timeout = 0.25)
     # Sending over ethernet server
ip = '169.254.36.51' #change for new lantronix
port_num = 10001
s = socket.socket()
s.connect((ip, port_num))
#except:
#    print("Failed to connect to power supply. \nPlease check connection and try again")
#     quit()

# Create log file
log_file_dir = "c://Users//dyang//OneDrive - D-Wave Systems Inc//Documents//transition report//Cosel RTE PSU Prototype//Cosel Control GUI//" + "\\Cosel communication logs\\"
file_name = datetime.now().strftime("%d_%m_%Y %H_%M_%S") + ".csv"
log_file = open(log_file_dir + file_name, 'wb')
log_writer = csv.writer(log_file, delimiter = ',')
log_writer.writerow(["Time", "Command", "Type", "Argument/Value", "Units", "Complete"])
logging_status = 0

START_TIME = time.time()
#send a command asking for vout_mode so we know what exponent to use. for now, make -8;

# Sending command to Cosel unit
def sendCommand(command, arg, slv_adr):
    vout_mode = -8
    #print("in send command")
    #print("command = ", command, "arg = ", arg)
    command_data = command['data'][:]
    command_data.insert(0, slv_adr)
    #print("command_data1 = ", command_data)
    arg_length = int(command['arg len'])
    #print(arg_length)
   # conversion = float(command['conversion factor'])

    if arg_length > 0:
       # Generates additional data bytes based on argument and expected argument length
        argument = int(arg )         
        if(command['data format'] == "ex lin"):
            #print(arg)
            (byte_0, byte_1) = cd.int_to_lin(command, arg, vout_mode = pow(2, -8))
            #print(byte_0, byte_1)
            command_data.append(byte_0)
            command_data.append(byte_1)
        elif(command['data format'] == 'unasigned binary int'):
            command_data.append(int(arg))
            command_data.append(int(arg))
            
        #print("command data2 = ", (command_data))
   
    send_command = ""
    #print("command data int= ", (command_data))
    for i in command_data:
        send_command = send_command + chr(i) #converting commanddata to char? the command to send
    #command_data
    hex = "".join("{:02X}".format(ord(c)) for c in send_command) # print hex representation
    print("hex Command = ", hex)
    #print("bin data = ", bin(command_data[0]))
    #print("send comm= ", send_command)
    success = "Complete"
    try:
        s.send(send_command)
        #s.write(send_command)
        #print("sent")

    except:
        print("Failed to send command")
        success = "Failed"

    if logging_status:
        log_writer.writerow([datetime.now().strftime("%H:%M:%S"), command['name'], "Tx", arg, command['units'], success])
    time.sleep(0.2)


# Read reply from Excelsys
def receiveReply(command):
    #reply = s.read(2)
    reply = s.recv(2)
    #print("in receive reply")
    num_bytes = 2
    #reply = s.read(num_bytes)#read 2 bytes
    print("reply = " ,reply)
    if reply:
        hex = "".join("{:02X}".format(ord(c)) for c in reply) # print hex representation of string
        if(num_bytes ==2):
            #byte come in reversed order
            print("hex reply = ", hex)
            hex_swap = []
            hex = list(hex)
            hex_swap[0:1] = hex[2:4]
            hex_swap[2:3] = hex[0:2]
            hex_str = "".join(hex_swap)
            #print(hex_str)
            reply_data = int(hex_str, 16)
        if(command):
            if(command['data format'] == 'lin'):
                ##print("reply = ", reply)
                
                #print("reply data = ", reply_data)
                val = cd.lin_to_int(command, reply_data, vout_mode = -8)
                return val
            elif (command['data format'] == 'ex lin'):
                hex = "".join("{:02X}".format(ord(c)) for c in reply) # print hex representation of string
                if(num_bytes ==2):
                    #byte come in reversed order
                    #print(hex)
                    hex_swap = []
                    hex = list(hex)
                    hex_swap[0:1] = hex[2:4]
                    hex_swap[2:3] = hex[0:2]
                    hex_str = "".join(hex_swap)
                    #print(hex_str)

                    reply_data = int(hex_str, 16)
                    val = Decimal(reply_data)/Decimal(pow(2, 8))
                    ##print(" reply val = ", val)
                    return val
            else:
                #print("reply = ", reply)
                reply_data = int(hex, 16)
                val = Decimal(reply_data)/Decimal(pow(2, 8))
                #print(" reply val = ", val)
                return val
        return reply_data #for errors, there will be a reply but no command. 
    #return val
        

  

def getErrorMessage(data):
    # WILL PROBS MOVE THIS TO SOMEWHERE ELSE
    errors =  {0: "Error: command does not exist",
                  1: "Error: argument exceeds settable range",
                  2: "Error: argument is inconsistant with existing parameters",
                  3: "Error: command disobeys with device settings",
                  4: "Error: the internal process is busy",
                  5: "Error: the selected slot is empty",
                  6: "Error: the command does not apply to the target module",
                  256: "Error: checksum mismatch",
                  8449: "Error: internal communication error"}
    return errors[data]

# Checks if the data log is empty at the end of the program and deletes it if it is
def endLog():
    log_file.close()
    read_file = open(log_file_dir + file_name, 'rb')
    lines = len(list(csv.reader(read_file)))
    read_file.close()
    if lines < 2:
        os.remove(log_file_dir + file_name)
