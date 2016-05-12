import RPi.GPIO as GPIO
import time
# blinking function
def blink(pin):
        GPIO.output(pin,GPIO.HIGH)
        if(GPIO.input(pin)):
            print("HIGH")
        time.sleep(1)
        GPIO.output(pin,GPIO.LOW)
        if(not GPIO.input(pin)):
            print("LOW")
        time.sleep(1)
        return
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO output channel
GPIO.setup(11, GPIO.OUT)
# blink GPIO17 50 times
for i in range(0,50):
        blink(11)
GPIO.cleanup()
