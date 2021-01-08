import signal
import os
import time

def handler(signum, frame):
    signal.alarm(5)
    print ('Signal handler called with signal', signum)
    

# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGALRM, handler)
signal.alarm(5)

while True:
    print ("Looping in main thread\r\n")
    time.sleep(1)

# signal.alarm(0)          # Disable the alarm