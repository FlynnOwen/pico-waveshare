import network
from machine import Pin
from time import sleep


def connect(pin: Pin, ssid: str, ssid_password: str):
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, ssid_password)
    while not wlan.isconnected():
        print("Waiting for connection...")
        pin.on()
        sleep(0.5)
        pin.off()
        sleep(0.5)
    ip = wlan.ifconfig()[0]
    pin.on()

    return ip
