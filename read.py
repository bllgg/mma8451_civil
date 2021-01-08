import serial
import datetime
import time
import os
# ser = serial.Serial('COM73', 115200)
ser = serial.Serial('/dev/ttyACM0', 115200)

fileName = "VW_Stabletest_"+str(int(time.time()))+".log"
start_time =  int(time.time())
timeNow    = start_time
while (1):#(timeNow < (start_time +(60*5))):
    try:
       cTime =datetime.datetime.utcnow()
       received = ser.readline().decode("utf-8")
       print (received)
       f = open(fileName, "a")
       f.write(str(cTime)+" : " + str(received))
       f.flush()
       os.fsync(f)
       f.close()
       
    except Exception as e:
        print(str(e))
    timeNow = int(time.time())
   