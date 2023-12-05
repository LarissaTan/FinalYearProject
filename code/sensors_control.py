import time
import LCD1602 as LCD
from pulsesensor import PulseSensor
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)      # Ignore warning for now

if __name__ == '__main__':
    LCD.init_lcd()
    time.sleep(1)

    p = PulseSensor()
    p.startAsyncBPM()

    while True:
        bpm = p.BPM
        if(bpm-125) > 0:
            #GPIO.output(12, GPIO.HIGH)
            LCD.print_lcd(1, 1, str(bpm - 125))
            print("HIGH" % (bpm - 125))
        else:
            print("no heart beat")
        
        #now = time.strftime('%m/%d %H:%M:%S', time.localtime(time.time()))
        #LCD.print_lcd(1, 1, 'Hello, world!')
        time.sleep(0.2)
