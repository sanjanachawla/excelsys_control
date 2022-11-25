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
    global slv_adr


    def __init__(self, root):
        
        # Sends test command message to Cosel power supply, for debugging purposes
        def sendTestCommand(command, argumentInput, address):
            slv_adr = int(address['address'], 16)
            Label(testFrame, text = address['address']).place(relx = 0.35, rely = 0.15, anchor = "center")
            argument = ""
            # Checks the expected length of the argument
            if int(command["arg len"]) > 0: #in bytes
                #try:
                    # Gets argument value from text input box
                argument = float(argumentInput.get())
                control.sendCommand(command, argument, slv_adr)
                #except:
                #    print("Invalid argument please try again")               
            # For commands with no arguments

            else:
                control.sendCommand(command, argument, slv_adr)
                #print(control.receiveReply(command))
                reply.set(control.receiveReply(command))
                units.set(command['units'])

        # Opens pop up window for user to update the selected slot's output voltage
        def makeVInWindow(slot, address):
            # Creating new window to enter in voltage
            slv_adr = int(address['address'], 16)
            #slv_adr = 0x51
            
            voltageInputWindow = Toplevel()
            voltageInputWindow.title("Update Voltage")
            voltageInputWindow.geometry("250x150")

            # Window widgets (label, entry, button)
            control.sendCommand(cc.commands['PAGE'], slot+1, slv_adr = 0x51)#page the module
            #control.receiveReply(cc.commands['PAGE'])
            upper_lim = '15'
            lower_lim = '6'
            Label(voltageInputWindow, text = "Upper limit: "+ upper_lim, font = ("Arial", 8)).place(anchor = "nw", relx = 0.1, rely = 0.05)
            Label(voltageInputWindow, text = "Lower limit: " + lower_lim, font = ("Arial", 8)).place(anchor = "nw", relx = 0.1, rely = 0.15)
            
            Label(voltageInputWindow, text = "Enter new voltage (V):", font = ("Arial", 8)).place(anchor = "nw", relx = 0.1, rely = 0.25)    
            voltageInput = Entry(voltageInputWindow)
            voltageInput.place(anchor = "n", relx = 0.5, rely = 0.4)
            Button(voltageInputWindow, text = "Update Voltage", command = lambda : userInputVoltage(voltageInput.get(), slot, voltageInputWindow, 5.999, 15, slv_adr)).place(anchor = "n", relx = 0.5, rely = 0.6)

        # Creates a new pop up window with input error message 
        def errorMessage(msg):
            errorWindow = Toplevel()
            errorWindow.title("Error")
            errorWindow.geometry("300x60")
            Label(errorWindow, text = msg, font =  ("Arial", 8)).place(anchor = "n", relx = 0.5, rely = 0.2)

        # Checks if correct voltage is applied
        # If yes, sends commands to change the voltage
        def userInputVoltage(v, slot, window, upper_limit, lower_limit, slv_adr):
            # If numerical value
            # If within range upper/lower voltage limit
            #slv_adr = int(address['address'], 16)
            upper_limit = 15
            lower_limit = 5.99
           # try:
           # control.sendCommand(cc.commands['PAGE'], slot, slv_adr = 0x51)
            newVoltage = float(v)             
            if (float(lower_limit) < newVoltage) and (float(upper_limit) > newVoltage):
                control.sendCommand(cc.commands['VOUT_COMMAND'], newVoltage, slv_adr = 0x51)
                #control.receiveReply(cc.commands['VOUT_COMMAND'])
                window.destroy()
                voltage, current, power, temperature = getVCPT(slv_adr=0x51)
                setVCPT(voltage, current, power,temperature ,slot, slv_adr = 0x51)
            else:
                errorMessage("Error this is an invalid input. \n Please enter a number between " + str(upper_limit) + " and " + str(lower_limit))
            #except:
                errorMessage("Error this is an invalid input. \n Please enter a number between " + str(upper_limit) + " and " + str(lower_limit))

        # Updates measurements of selected output
        def updateSlot(slot, address):
            slv_adr = int(address['address'], 16)
            control.sendCommand(cc.commands['PAGE'], slot+1, slv_adr) #pages that module
            #control.receiveReply(cc.commands['PAGE'])
            voltage, current, power, temperature = getVCPT(slv_adr)
            setVCPT(voltage, current, power, temperature ,slot, slv_adr)
            if(voltage <5.70 ):
                state = 0
            else:
                state = 1
 
            status[slot].set(light[state]["text"])
            outputButtons[slot].configure(bg = light[state]["bg"])

        # Changes the output state of the specified slot
        def setOnOff(state, slot, address):
            slv_adr = int(address['address'], 16)
            # Select slot
            control.sendCommand(cc.commands['PAGE'], slot+1, slv_adr)
            voltage, current, power, temperature = getVCPT(slv_adr)
            setVCPT(voltage, current, power, temperature ,slot, slv_adr )
            if(voltage > 5.70 ): #turn off
                state = 0
                print("turning off")
                control.sendCommand(cc.commands['OPERATION'],0, slv_adr)
                
            else: #turn on 
                state = 1     
                print("turning on")
                control.sendCommand(cc.commands['OPERATION'],128, slv_adr)
              
            # Determine if the slot is on or off
      
            # Switch to opposite state, update button features and voltage and current measurements
            status[slot].set(light[ state]["text"])
            outputButtons[slot].configure(bg = light[ state]["bg"])
            #control.sendCommand(cc.commands["PAGE"], slot + 1, slv_adr = 0x51)
            #control.receiveReply(cc.commands['PAGE'])
            
            #control.sendCommand(cc.commands[light[not state]["command"]], None)
            #control.receiveReply(cc.commands[light[not state]["command"]])
            voltage, current, power, temperature = getVCPT(slv_adr)
            setVCPT(voltage, current, power, temperature, slot, slv_adr )
        
        # Updates the measured voltage and current values of the selected slot
        def setVCPT(v, c, p, T, slot, slv_adr):
            outputVoltages[slot].set(v)
            outputCurrents[slot].set(c)
            outputPowers[slot].set(p)
            outputTemperatures[slot].set(T)
        
        # Updates the current and voltage value of the selected output slot
        def getVCPT(slv_adr):
            #time.sleep(0.5) # time delay to account for voltage change ramp rate, could make variable
            control.sendCommand(cc.commands["MON_IOUT"], None, slv_adr )
            current = round((control.receiveReply(cc.commands["MON_IOUT"])), 4) #dont understand how it is formatting - need to print out and check
            
            control.sendCommand(cc.commands["MON_VOUT"], None, slv_adr )
            voltage = round((control.receiveReply(cc.commands["MON_VOUT"])), 4)

            control.sendCommand(cc.commands["READ_TEMPERATURE"], None, slv_adr )
            temperature = round((control.receiveReply(cc.commands["READ_TEMPERATURE"])), 4)
            
            #control.sendCommand(cc.commands["MON_OUTPUT_POWER"], None)
            #power = '{:.3f}'.format(control.receiveReply(cc.commands["MON_OUTPUT_POWER"]))
            power = round(float(voltage) * float(current), 4);
            return voltage, current, power, temperature

        # Creates a pop-up window that displays the current progress of an output update
        def progressUpdate():
            progressWindow = Toplevel()
            progressWindow.title("Progress")
            progressWindow.geometry("300x100+50+20")
            Label(progressWindow, text = "Updating Module", font =  ("Arial", 8)).place(anchor = "n", relx = 0.5, rely = 0.2)
            pb = Progressbar(progressWindow, orient = HORIZONTAL, length = 100, mode = 'determinate')
            pb.place(relx = 0.35, rely = 0.5)
            root.update()
            return pb, progressWindow
        
        # Gets Updated values of power supply parameters
        def updatePS(address):
            # Storing measurements 
            print(address['address'])
            slv_adr = int(address['address'], 16)
            Label(inputFrame, text = address['address']).place(relx = 0.9, rely = 0.13, anchor = "center")
            #print('slv_adr = ', slv_adr)

            input_commands = ['MON_VIN', 'MON_FAN_SPEED']
            measured_inputs = [0, 0]

            # Get power supply measurements
            for i in range(0, len(input_commands)):
                control.sendCommand(cc.commands[input_commands[i]], None, slv_adr)
                measured_inputs[i] = '{:.0f}'.format(control.receiveReply(cc.commands[input_commands[i]]))
            
            #inputVoltage, fanSpeed = measured_inputs
            # Loads measured values into their respective widgets
            for i in range(0, len(measured_inputs)):
                inputTextVars[i].set(measured_inputs[i])
            return 

        # Updates the values of all displays
        def updateAll():
            # Initiate progress window
            pb, window = progressUpdate()
            NUM_COMMANDS = 20
            pb['value'] = 0

            # Storing measurements 
            input_commands = ['MON_VIN', 'MON_FAN_SPEED_1']
            measured_inputs = [0, 0, 0, 0]

            # Get power supply measurements
            for i in range(0, len(input_commands)):
                control.sendCommand(cc.commands[input_commands[i]], None)
                measured_inputs[i] = '{:.0f}'.format(control.receiveReply(cc.commands[input_commands[i]]))
                pb['value'] = pb['value'] + 100.0/NUM_COMMANDS
                root.update()
            
            # Determine if GI is on or off
            #control.sendCommand(cc.commands['READ_CTL_GI'], None)
            #state = int(control.receiveReply(cc.commands['READ_CTL_GI']))
            # Switch to opposite state, update button features 
            #giText.set(gi[state]["text"])
            #giButton.configure(bg = gi[state]["bg"])

            # Get output measurements 
            slots = [1, 2, 3, 4, 5, 6]
            output_voltage = [None] * 6
            output_current = [None] * 6
            output_power = [None] * 6
            output_temperature = [None] * 6
            states = [None] * 6
            for s in range(0, len(slots)):  
                # Select the slot to communicate with     
                control.sendCommand(cc.commands['PAGE'], slots[s], slv_adr)
                #control.receiveReply(cc.commands['PAGE'])
                
                pb['value'] = pb['value'] + 100.0/NUM_COMMANDS
                root.update()
                # Get output voltage and current values
                output_voltage[s], output_current[s], output_power[s], output_temperature[s] = getVCPT()  
                pb['value'] = pb['value'] + 100.0/NUM_COMMANDS
                root.update()
                # Get slot state and set button color
                #control.sendCommand(cc.commands['READ_REMOTE_CONTROL'], None) # no way to read state of module, just can enable them
                #states[s] = control.receiveReply(cc.commands['READ_REMOTE_CONTROL'])
                
                pb['value'] = pb['value'] + 100.0/NUM_COMMANDS
                root.update()
            
            # Loads measured values into their respective widgets
            for i in range(0, len(inputTextVars)):
                inputTextVars[i].set(measured_inputs[i])

            for s in range(0, len(slots)):
                status[s].set(light[states[s]]["text"])
                outputButtons[s].configure(bg = light[states[s]]["bg"])
                setVCPT(output_voltage[s], output_current[s], output_power[s], output_temperature[s], s)
            
            window.destroy()



        # Power supply frame
        inputFrame = Frame(root, height = 200, width = 200, relief = "groove", bd = 2)
        inputFrame.place(anchor = 'nw', relx = 0.02, rely = 0.02)
        Label(inputFrame, text = "Power Supply",  font = ("Arial", 8, 'bold')).place(anchor = "n", relx = 0.5, rely = -0.04)

        # text variables for power supply inputs
        inputVoltage = StringVar(inputFrame, value = None)
        fanSpeed = StringVar(inputFrame, value = None)
        errorMessage = StringVar(inputFrame, value= None)
    #    fan2Speed = StringVar(inputFrame, value = None)
    #    fanTemp = StringVar(inputFrame, value = None)
        inputLabels = ["Input Voltage:", "Fan Speed:", "Error:" ]
        inputTextVars = [inputVoltage, fanSpeed, errorMessage]
        inputUnits = ["V", "krmp", " "]

        # Power supply parameter labels and values
        valueInside_adr = StringVar(inputFrame, value = cc.addresses.keys()[0])
        adr_val = OptionMenu(inputFrame, valueInside_adr, *sorted(cc.addresses.keys()))
        adr_val.config(width = 3)
        adr_val.config(font = ("Arial", 8))
        adr_val.place(relx = 0.65, rely =  0.13, anchor = "center")
        #Label(inputFrame, text = "Address: ").place(relx = 0.15, rely = 0.33, anchor = "center")
        Label(inputFrame, text = cc.addresses[valueInside_adr.get()]['address']).place(relx = 0.9, rely = 0.13, anchor = "center")
        updatePSButton = Button(inputFrame, text = "Update", command= lambda : updatePS(cc.addresses[valueInside_adr.get()]))
        updatePSButton.place(relx = 0.2, rely = 0.9, anchor = "center")
        Label(inputFrame, text = "Address:", font = ("Arial", 10, 'bold')).place(relx = 0, rely =  0.07)
        #
        # Label(inputFrame, textvariable = inputTextVars[i], bd = 2, relief = "sunken", font = ("Arial", 9), width = 5, height = 0).place(relx = 0.65, rely = float(i) / 5 + 0.05)
        #Label(inputFrame, text = inputUnits[i], font = ("Arial", 8)).place(relx = 0.85, rely = float(i) / 5 + 0.05)

        for i in range(0, len(inputLabels)):
            Label(inputFrame, text = inputLabels[i], font = ("Arial", 10)).place(relx = 0, rely = float(i+1) / 5 + 0.05)
            Label(inputFrame, textvariable = inputTextVars[i], bd = 2, relief = "sunken", font = ("Arial", 9), width = 5, height = 0).place(relx = 0.65, rely = float(i+1) / 5 + 0.05)
            Label(inputFrame, text = inputUnits[i], font = ("Arial", 8)).place(relx = 0.85, rely = float(i+1) / 5 + 0.05)
        
        # Output slots frames
        outputFrame = Frame(root, height = 420, width = 525, relief = "groove", bd = 2)
        outputFrame.place(anchor = 'sw', relx = 0.02, rely = 0.98)
        Label(outputFrame, text = "Outputs",  font = ("Arial", 8)).place(anchor = "n", relx = 0.5, rely = -0.02)

        # text variables for power supply outputs
        outputVoltages = []
        outputCurrents = []
        outputPowers = []
        outputTemperatures = []
        status = []
        for i in range(0, 6):
            outputVoltages.append(StringVar(outputFrame, value = ""))
            outputCurrents.append(StringVar(outputFrame, value = ""))  
            outputPowers.append(StringVar(outputFrame, value = ""))
            outputTemperatures.append(StringVar(outputFrame, value = ""))               
            status.append(StringVar(outputFrame, value = ""))       
        
        outputFrames = []
        changeButtons = []
        outputButtons = []
        updateButtons = []
        light = {1:{"bg": "#4cc924", "text": "ON", "command": "OPERATION"}, 0:{"bg": "#ed3737", "text": "OFF", "command": "OPERATION"}}
        for i in range (0,2):
            for j in range(0,3):
                # Slot frame initialization
        
                
                #add slv_adr things

                outputFrames.append(Frame(outputFrame, height = 200, width = 150, relief = "groove", bd = 2))
                outputFrames[-1].place(anchor = 'sw', relx = float(j)/3.0 + 0.025, rely = float(i)/2.0 + 0.5)
                # Status Widgets
                Label(outputFrames[-1], text = "Slot " + str(i*3+j +1) + " status:", font = ("Arial", 10)).place(relx = 0, rely = 0.05)
                outputButtons.append(Button(outputFrames[-1], textvariable = status[i*3+j], width = 3, command = lambda t = len(outputButtons):setOnOff(status[t].get(),  t, cc.addresses[valueInside_adr.get()])))
                outputButtons[-1].place(relx = 0.76, rely = 0.05)
                # Output current and voltage labels + power
                Label(outputFrames[-1], text = "Voltage:", font = ("Arial", 10)).place(relx = 0, rely = 0.20)
                Label(outputFrames[-1], text = "Current:", font = ("Arial", 10)).place(relx = 0, rely = 0.35)
                Label(outputFrames[-1], text = "Power:", font = ("Arial", 10)).place(relx = 0, rely = 0.50)
                Label(outputFrames[-1], text = "Temp:", font = ("Arial", 10)).place(relx = 0, rely = 0.65)
                # Output current and voltage values + power

                #valueInside_adr = StringVar(outputFrames[-1], value = cc.addresses.keys()[0])
                #adr_val = OptionMenu(outputFrames[-1], valueInside_adr, *sorted(cc.addresses.keys()))
                #adr_val.config(width = 5)
                #adr_val.config(font = ("Arial", 8))
                #adr_val.place(relx = 0.25, rely = 0.1, anchor = "center")
                #Label(outputFrames[-1], text = "Address: ").place(relx = 0, rely = 0.1, anchor = "center")
                #Label(outputFrames[-1], text = cc.addresses[valueInside_adr.get()]['address']).place(relx = 0.5, rely = 0.1, anchor = "center")
                #slv_adr = cc.addresses[valueInside_adr.get()] #['address']

                Label(outputFrames[-1], textvariable = outputVoltages[i*3+j], bd = 2, relief = "sunken", font = ("Arial", 10), width = 7, height = 0).place(relx = 0.45, rely = 0.20)
                Label(outputFrames[-1], textvariable = outputCurrents[i*3+j], bd = 2, relief = "sunken", font = ("Arial", 10), width = 7, height = 0).place(relx = 0.45, rely = 0.35)
                Label(outputFrames[-1], textvariable = outputPowers[i*3+j], bd = 2, relief = "sunken", font = ("Arial", 10), width = 7, height = 0).place(relx = 0.45, rely = 0.50)
                Label(outputFrames[-1], textvariable = outputTemperatures[i*3+j], bd = 2, relief = "sunken", font = ("Arial", 10), width = 7, height = 0).place(relx = 0.45, rely = 0.65)
                Label(outputFrames[-1], text = "V", font = ("Arial", 8)).place(relx = 0.88, rely = 0.20)
                Label(outputFrames[-1], text = "A", font = ("Arial", 8)).place(relx = 0.88, rely = 0.35)
                Label(outputFrames[-1], text = "W", font = ("Arial", 8)).place(relx = 0.88, rely = 0.50)
                Label(outputFrames[-1], text = "C", font = ("Arial", 8)).place(relx = 0.88, rely = 0.65)
                # Button for changing voltage
                changeButtons.append(Button(outputFrames[-1], text = "Change", command= lambda t= len(changeButtons): makeVInWindow(t, cc.addresses[valueInside_adr.get()])))
                changeButtons[-1].place(relx = 0.1, rely = 0.85)
                # Buttone for updating readings
                updateButtons.append(Button(outputFrames[-1], text = "Update", command= lambda t= len(updateButtons): updateSlot(t, cc.addresses[valueInside_adr.get()])))
                updateButtons[-1].place(relx = 0.57, rely = 0.85)
                # Toggle for output on/off

        # Test command frame
        
        #test frame
        testFrame = Frame(root, height = 190, width = 315, relief = "groove", bd = 2)
        testFrame.place(anchor = 'nw', relx = 0.4, rely = 0.02)

        #address:
        #valueInside_adr = StringVar(testFrame, value = cc.addresses.keys()[0])
        #adr_val = OptionMenu(testFrame, valueInside_adr, *sorted(cc.addresses.keys()))
        #adr_val.config(width = 5)
        #adr_val.config(font = ("Arial", 8))
        #adr_val.place(relx = 0.5, rely = 0.15, anchor = "center")
        Label(testFrame, text = "Address: ").place(relx = 0.2, rely = 0.15, anchor = "center")
        #Label(testFrame, text = cc.addresses[valueInside_adr.get()]['address']).place(relx = 0.75, rely = 0.15, anchor = "center")

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
        Button(testFrame, text = "Send Command", font = ("Arial", 10), command = lambda : sendTestCommand(cc.commands[valueInside.get()], argumentInput, cc.addresses[valueInside_adr.get()])).place(relx = 0.5, rely = 0.50, anchor = "center")
        
        #reply
        Label(testFrame, text = "Reply: ").place(relx = 0.15, rely = 0.65)
        reply = StringVar(testFrame, value = "")
        Label(testFrame, textvariable = reply, bd = 2,  relief = "sunken", font = ("Arial", 10), width = 16, height = 0).place(relx = 0.3, rely = 0.65)
        units = StringVar(testFrame, value = "")
        Label(testFrame, textvariable = units,font = ("Arial", 8)).place(relx = 0.75, rely = 0.65)

root = Tk()
root.geometry("550x640+500+20")
root.attributes("-topmost", True)
frame = Frame(root)
frame.pack()
my_gui = powerSupplyGUI(root)
root.mainloop()
control.endLog()