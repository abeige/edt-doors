from gpiozero import LED
from time import sleep
import asyncio
import random

led = {
    "red": LED(6),
    "green": LED(13),
    "blue": LED(19),
    "yellow": LED(26),
}

order = ["red", "green", "blue", "yellow"]

def main():
    i = 0
    dir = 1
    for _ in range(40):
        led[order[i]].on()
        sleep(0.1)
        led[order[i]].off()
        i += dir
        if i == len(order):
            i -= 2
            dir *= -1
        elif i == -1:
            i += 2
            dir *= -1
    print(led.keys())

if __name__ == "__main__":
    main()