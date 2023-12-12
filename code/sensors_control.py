import time
import LCD1602 as LCD
from pulsesensor import PulseSensor
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from scipy import signal,stats
import multiprocessing
import pandas as pd

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)      # Ignore warning for now

#Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))



if __name__ == '__main__':
    LCD.init_lcd()
    time.sleep(1)

    p = PulseSensor()
    p.startAsyncBPM()

    #value = mcp.read_adc(0)
    #print("value of ECG: " + str(value))

    while True:

        bpm = int(p.BPM)
        value = mcp.read_adc(0)
        voltage_ecg = (value / 1023.0) * 3.3
        amplitude_ecg = round(voltage_ecg * (3.0 / 3.3), 3)
        ecg_output = "E:" + str(amplitude_ecg)
        print("value of ECG: " + str(amplitude_ecg))
  
        if(bpm-125) > 0:
            #GPIO.output(12, GPIO.HIGH)
            pulse_output = "P:" + str(bpm - 125)
            print("HIGH, " + str(bpm - 125))
        else:
            print("no heart beat")
            pulse_output = "No"
        
        LCD.print_lcd(1, 1, ecg_output + "|" + pulse_output)
        
        #now = time.strftime('%m/%d %H:%M:%S', time.localtime(time.time()))
        #LCD.print_lcd(1, 1, 'Hello, world!')
        time.sleep(0.2)
