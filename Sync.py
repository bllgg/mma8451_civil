import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

# GPIO 21 set up as an input, pulled down, connected to 3V3 on button press
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# now we'll define two threaded callback functions
# these will run in another thread when our events are detected
def my_callback(channel):
    print "Rising Edge edge detected on 17"



# when a falling edge is detected on port 21, regardless of whatever 
# else is happening in the program, the function my_callback will be run
GPIO.add_event_detect(21, GPIO.RISING, callback=my_callback, bouncetime=10)

while True:
    print "Waiting for GPIO\r\n"
    time.sleep(10)

GPIO.cleanup()           # clean up GPIO on normal exit
