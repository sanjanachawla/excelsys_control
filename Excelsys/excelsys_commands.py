# intermediate script for converting .csv data to json to python dictionary
import csv
import codecs
import os

# file = os.getcwd() + "\\cosel commands py.csv"
file = ".\Excelsys commands py.csv"
file2 = ".\PS_address.csv"
with open(file, mode = 'r') as infile:
    reader = csv.reader(codecs.EncodedFile(infile, 'utf-8', 'utf-8-sig'), delimiter=",")
    commands = {}
    for line in reader:
        try:
            data = line[1].split(',')
            for i in range(0,len(data)):
                data[i] = int(data[i], 16)
                #print(data[i])
            commands[line[0]] = {"name": line[0],"data":data,"arg len": line[2], "data format": line[3],  "type": line[4], "units": line[5], "description": line[6]}
        except:
            print("Error could not import all commands")
    #print(commands["data"])


with open(file2, mode = 'r') as infile:
    reader = csv.reader(codecs.EncodedFile(infile, 'utf-8', 'utf-8-sig'), delimiter=",")
    addresses = {}
    for line in reader:
        try:
            data = line[1].split(',')
            for i in range(0,len(data)):
                data[i] = int(data[i], 16)
                #print(data[i])
            addresses[line[0]] = {"PS": line[0],"address":line[1]}
        except:
            print("Error could not import all addresses")
    print(addresses)