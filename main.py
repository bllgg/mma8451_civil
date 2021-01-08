import threading
import RPi.GPIO as GPIO
import time
import os
import accelOnly
import datetime
from accelOnly import Accel
import signal
import Node
from datetime import datetime as dt

# from accelOnly import TestFunc 

GPIO.setmode(GPIO.BCM)
startTime = 1
DataBuffer = []
nodeId = Node.nodeId
fileName = "Data/Acc_Data"+str(nodeId)+str(int(time.time()))+".csv"
f = open(fileName, "a")
state = False
lastState = False
counter =0
maxCounter =240000

def turn_on_launchpad():
    print("Launchpad offline")
    time.sleep(12.0)
    os.system("echo 1 > /sys/devices/platform/soc/3f980000.usb/buspower")
    print("Launchpad online")

def SyncCallBack(channel):
    global f, DataBuffer,counter,state
    
    # if not f.closed:
    #     f.close()
    signal.setitimer(signal.ITIMER_REAL,0,0)
    # signal.signal(signal.SIGALRM, GetData)
    signal.setitimer(signal.ITIMER_REAL,startTime,0.01)
    global fileName
    del DataBuffer[:]
    # print DataBuffer
    counter =0
    fileName = "Data/Acc_Data_"+str(nodeId)+"_"+str(int(time.time()))+".csv"
    # f = open(fileName, "a")
    state = not(state)
    print ("Data Collecting Started",fileName,"\r\n")
    



def GetData(signum, frame):

    global counter
    # print counter
    if(counter<maxCounter):
        time_val = dt.now()
        accle_value = MMA8451.getAxisValue()
        date_time = str(time_val.year) +"-"+ str(time_val.month) +"-"+ str(time_val.day) +","+ str(time_val.hour ) +":"+ str(time_val.minute) +":"+ str(time_val.second) +":"+  str(time_val.microsecond / 1000) +","
        DataBuffer.append(date_time)
        DataBuffer.append(accle_value)  
        # f.write(str(counter)+","+MMA8451.getAxisValue() +"\r\n")
        # # f.flush()
        # os.fsync(f)
        # # f.write(str(counter)+", " + MMA8451.getAxisValue() +"\r\n")
        # # f.flush()
        # os.fsync(f)
        # print counter
        counter +=1
    else:
        # counter = 0
        signal.setitimer(signal.ITIMER_REAL,0,0)
        print ("Counter Stoped\r\n")
      
    # print ('Signal handler called with signal', signum)

def background_threads():

    # dbThread = threading.Thread(target = SaveData)
    # dbThread.daemon = True
    # dbThread.start()
    localCounter =0
    localStrBuff = ""

    while True:
        # time.sleep(1)
        
        # continue
        global f, DataBuffer,lastState

        if(state!=lastState):
            if not f.closed:
                f.close()
            f = open(fileName, "a")
            lastState = state
        else:
            if(len(DataBuffer)):
                try:
                    localStrBuff += DataBuffer.pop(0)
                    localCounter += 1
                    # print localCounter
                    if(localCounter==1000):
                        f.write(localStrBuff)
                        f.flush()
                        os.fsync(f)
                        localCounter =0
                        localStrBuff = ""
                        # print "DataWritten"

                except Exception as e:
                    print("Error " ,str(e))
            else:
                # print "Going to Sleep \r\n"
                time.sleep(0.01)

# if __name__ == "__main__":
print ("Starting UoM SHM...\r\n")

# GPIO 21 set up as an input, pulled down, connected to 3V3 on button press
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
signal.signal(signal.SIGALRM, GetData)

# when a falling edge is detected on port 21, regardless of whatever 
# else is happening in the program, the function my_callback will be run
GPIO.add_event_detect(21, GPIO.RISING, callback=SyncCallBack, bouncetime=10)

MMA8451 = Accel()
MMA8451.init()

if MMA8451.whoAmI() != accelOnly.deviceName:
    print("Error! Device not recognized! (" + str(accelOnly.deviceName) + ")")

background_threads()
GPIO.cleanup()           # clean up GPIO on normal exit