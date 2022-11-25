from ttk import Progressbar
from Tkinter import *
import convert_data as cd
import excelsys_commands as cc
import excelsys_control as control
import time
import tkFileDialog
import csv
import codecs
import os
from datetime import datetime 

class powerSupplyGUI:
    # Global variables
    global slv_adr
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


    def __init__(self, root):
        # first thing to do is set wakeup command, and read and save vout_mode. 
        # Sends test command message to Cosel power supply, for debugging purposes
        def sendTestCommand(command, argumentInput, address):
            slv_adr = int(address['address'], 16)
            Label(testFrame, text = address['address']).place(relx = 0.75, rely = 0.15, anchor = "center")
            argument = ""
            # Checks the expected length of the argument
            if int(command["arg len"]) > 0: #in bytes
                try:
                    # Gets argument value from text input box
                    argument = float(argumentInput.get())
                    control.sendCommand(command, argument, slv_adr)
                except:
                    print("Invalid argument please try again")               
            # For commands with no arguments

            else:
                control.sendCommand(command, argument, slv_adr)
                reply.set('{:.3f}'.format(control.receiveReply(command)))
                units.set(command['units'])
       
        
        # Gets Updated values of power supply parameters
        def updatePS(address):
            # Storing measurements 
            print(address['address'])
            slv_adr = int(address['address'], 16)
            Label(inputFrame, text = address['address']).place(relx = 0.9, rely = 0.33, anchor = "center")
            print('slv_adr = ', slv_adr)
            input_commands = ['MON_VIN']
            measured_inputs = [0]
            # Get power supply measurements
            for i in range(0, len(input_commands)):
                control.sendCommand(cc.commands[input_commands[i]], None, slv_adr)
                measured_inputs[i] = '{:.0f}'.format(control.receiveReply(cc.commands[input_commands[i]]))
            # inputVoltage= measured_inputs
            # Loads measured values into their respective widgets
            # add text box on slot box too to make sure we know which supply it is for. 
            for i in range(0, len(inputTextVars)):
                inputTextVars[i].set(measured_inputs[i])
            return 


        self.root = root
        root.title("Excelsys Control")
        frame = Frame(root)
        frame.pack()

        # Power supply frame
        inputFrame = Frame(root, height = 200, width = 200, relief = "groove", bd = 2)
        inputFrame.place(anchor = 'nw', relx = 0.02, rely = 0.02)
        Label(inputFrame, text = "Power Supply",  font = ("Arial", 8)).place(anchor = "n", relx = 0.5, rely = -0.04)

        # text variables for power supply inputs
        inputVoltage = StringVar(inputFrame, value = None)

        inputLabels = ["Input Voltage:" ]
        inputTextVars = [inputVoltage]
        inputUnits = ["V"]

        # Power supply parameter labels and values
        #address
        valueInside_adr = StringVar(inputFrame, value = cc.addresses.keys()[0])
        adr_val = OptionMenu(inputFrame, valueInside_adr, *sorted(cc.addresses.keys()))
        adr_val.config(width = 5)
        adr_val.config(font = ("Arial", 8))
        adr_val.place(relx = 0.6, rely = 0.33, anchor = "center")
        Label(inputFrame, text = "Address: ").place(relx = 0.15, rely = 0.33, anchor = "center")

        print("addresses_only = ", cc.addresses[valueInside_adr.get()])
       
        Label(inputFrame, text = cc.addresses[valueInside_adr.get()]['address']).place(relx = 0.9, rely = 0.33, anchor = "center")
        updatePSButton = Button(inputFrame, text = "Update", command= lambda : updatePS(cc.addresses[valueInside_adr.get()]))
        updatePSButton.place(relx = 0.2, rely = 0.9, anchor = "center")
 

    

        # Test command frame
        
        #test frame
        testFrame = Frame(root, height = 200, width = 315, relief = "groove", bd = 2)
        testFrame.place(anchor = 'nw', relx = 0.4, rely = 0.02)

        #address:
        valueInside_adr = StringVar(testFrame, value = cc.addresses.keys()[0])
        adr_val = OptionMenu(testFrame, valueInside_adr, *sorted(cc.addresses.keys()))
        adr_val.config(width = 5)
        adr_val.config(font = ("Arial", 8))
        adr_val.place(relx = 0.5, rely = 0.15, anchor = "center")
        Label(testFrame, text = "Address: ").place(relx = 0.2, rely = 0.15, anchor = "center")
        Label(testFrame, text = cc.addresses[valueInside_adr.get()]['address']).place(relx = 0.75, rely = 0.15, anchor = "center")

        #command drop down
        valueInside = StringVar(testFrame, value = cc.commands.keys()[0])
        testCommands = OptionMenu(testFrame, valueInside, *sorted(cc.commands.keys()))
        testCommands.config(width = 10)
        testCommands.config(font = ("Arial", 8))
        testCommands.place(relx = 0.42, rely = 0.33, anchor = "center")
        Label(testFrame, text = "Command: ").place(relx = 0.15, rely = 0.33, anchor = "center")
        #arg:
        Label(testFrame, text = "Arg: ").place(relx = 0.68, rely = 0.33, anchor = "center")
        argumentInput = Entry(testFrame, width = 5, font = ("Arial", 13))
        argumentInput.place(relx = 0.8, rely = 0.33, anchor = "center")
        #send command button
        Button(testFrame, text = "Send Command", font = ("Arial", 8), command = lambda : sendTestCommand(cc.commands[valueInside.get()], argumentInput, cc.addresses[valueInside_adr.get()])).place(relx = 0.5, rely = 0.50, anchor = "center")
        
        #reply
        Label(testFrame, text = "Reply: ").place(relx = 0.15, rely = 0.65)
        reply = StringVar(testFrame, value = "")
        Label(testFrame, textvariable = reply, bd = 2,  relief = "sunken", font = ("Arial", 10), width = 16, height = 0).place(relx = 0.3, rely = 0.65)
        units = StringVar(testFrame, value = "")
        Label(testFrame, textvariable = units,font = ("Arial", 8)).place(relx = 0.75, rely = 0.45)
 
        
        
root = Tk()
root.geometry("550x640+500+20")
root.attributes("-topmost", True)
frame = Frame(root)
frame.pack()
my_gui = powerSupplyGUI(root)
root.mainloop()
control.endLog()