import time
import LCD1602 as LCD

if __name__ == '__main__':
    LCD.init_lcd()
    time.sleep(1)

    while True:
        now = time.strftime('%m/%d %H:%M:%S', time.localtime(time.time()))
        LCD.print_lcd(1, 1, now)
        time.sleep(0.2)
