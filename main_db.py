import threading
import RPi.GPIO as GPIO
import time
import os
import accelOnly
import datetime
from accelOnly import Accel
import signal
import Node
import sqlite3
from threading import Lock, Thread
lock = Lock()


conn = sqlite3.connect('test.db',check_same_thread=False)
print ("Opened database successfully")

conn.execute('''CREATE TABLE IF NOT EXISTS MMA4851
         (ID           INT     NOT NULL,
         X             INT    NOT NULL,
         Y             INT     NOT NULL,
         Z             INT NOT NULL,
        Batch_No       INT NOT NULL);''')
print ("Table created successfully")

# from accelOnly import TestFunc 

GPIO.setmode(GPIO.BCM)
startTime = 1
DataBuffer = []
nodeId = Node.nodeId
# fileName = "Data/Acc_Data"+str(nodeId)+str(int(time.time()))+".csv"
# f = open(fileName, "a")
# working = False
counter =0
maxCounter =40000
batchNo = 0


def SyncCallBack(channel):
    global f, DataBuffer,counter,conn
    # conn.close()
    # conn = sqlite3.connect('test.db')
    # if not f.closed:
    #     f.close()
    signal.setitimer(signal.ITIMER_REAL,0,0)
    conn.commit()
    conn.close()
    dbName = "Data_"+str(nodeId)+"_"+str(int(time.time()))+".db"
    conn = sqlite3.connect(dbName,check_same_thread=False)
    print ("Opened database successfully")

    conn.execute('''CREATE TABLE MMA4851
            (ID           INT     NOT NULL,
            X             INT    NOT NULL,
            Y             INT     NOT NULL,
            Z             INT NOT NULL
            );''')
    print ("Table created successfully")

    signal.setitimer(signal.ITIMER_REAL,startTime,0.02)
    # global batchNo
    del DataBuffer[:]
    counter =0
    # batchNo = int(time.time())
    # fileName = "Data/Acc_Data_"+str(nodeId)+"_"+str(int(time.time()))+".csv"
    # f = open(fileName, "a")
    print "Data Collecting Started",dbName,"\r\n"
    

def PutData():
    global f, DataBuffer
    
    if(len(DataBuffer)):
        try:
            cTime =datetime.datetime.utcnow()
            # f = open(fileName, "a")
            f.write(str(cTime)+", " + DataBuffer.pop(0) +"\r\n")
            f.flush()
            os.fsync(f)
            # if not f.closed:
                # f.close()
        except Exception as e:
            print("Error " ,str(e))

def GetData(signum, frame):

    global counter,f
    # print counter
    if(counter<maxCounter):
        buffData = MMA8451.getAxisValue()
        # buffData.append(counter)
        # lock.acquire()
        # DataBuffer.append(buffData)
        # lock.release()
        conn.execute("INSERT INTO MMA4851 (ID, X, Y, Z) VALUES (?, ?, ?, ?)",
            (counter,buffData[0],buffData[1], buffData[2]))
        conn.commit()
        # f.write(str(counter)+", " + MMA8451.getAxisValue() +"\r\n")
        # f.flush()
        # os.fsync(f)
        # print counter
        counter +=1
    else:
        # counter = 0
        signal.setitimer(signal.ITIMER_REAL,0,0)
        print "Counter Stoped\r\n"
      
    # print ('Signal handler called with signal', signum)

def background_threads():

    # dbThread = threading.Thread(target = SaveData)
    # dbThread.daemon = True
    # dbThread.start()

    while True:
        continue
        # global DataBuffer
    
        # if(len(DataBuffer)):
        #     try:
        #         lock.acquire()
        #         dbData = DataBuffer.pop(0)
        #         lock.release()
        #         # print dbData
        #         conn.execute("INSERT INTO MMA4851 (ID, X, Y, Z) VALUES (?, ?, ?, ?)",
        #         (dbData[3],dbData[0],dbData[1], dbData[2]))
        #         conn.commit()
        #         # f.write(DataBuffer.pop(0) +"\r\n")
        #         # f.flush()
        #         # os.fsync(f)

        #     except Exception as e:
        #         print("Error " ,str(e))
        # else:
        #     print "Going to sleep\r\n"
        #     time.sleep(0.1)


# if __name__ == "__main__":
print "Starting UoM SHM...\r\n"

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