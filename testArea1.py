import json
import sys

#Create the functions for each of the algorithm here, then we call that algorithm later.



# Main program - reading the file
if len(sys.argv) < 2:
    print("Usage: python main.py input.json > output.json")

with open(sys.argv[1], "r") as file:
    jsonData = json.load(file) #jsonData contains the json file now.


if (jsonData[" policy "] == " RR "): # RoundRobin
    print("Round Robin")

elif (jsonData[" policy "] == "FIFO"): #FIFO
    print("FIFO")

elif (jsonData[" policy "] == "SJF"): #SJF
    print("SJF")

elif (jsonData[" policy "] == "Priority"): #Priority
    print("Priority")

