import serial
import smbus
import time
import sys
import LCD1602 as LCD

if __name__ == '__main__':  
    LCD.init_lcd()
    time.sleep(1)
    
    ser = serial.Serial("/dev/ttyUSB0", 9600)
	
    while True:
        now = time.strftime('%m/%d %H:%M:%S', time.localtime(time.time()))
        LCD.print_lcd(1, 1, now)
        time.sleep(0.2)
        if ser.in_waiting > 0:
            received_data = ser.readline().decode().strip()
            print("Received data from Arduino:",received_data)
            LCD.print_lcd(2, 0, received_data)