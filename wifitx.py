#!/usr/bin/env Python3

"""Coninuiously output tx rate of wifi"""

import re
import sys
import time
import subprocess


def return_numbers(string):  # Returns only numbers from an input string
    values = re.findall("\d", string)
    return "".join(values)


def time_now():  # Returns time when run
    time_now = time.strftime("%H:%M:%S", time.gmtime())
    return time_now


def data_filter(data, search_term):
    data = [x.strip() for x in data]
    for item in data:
        if item.startswith(search_term):
            return item


def get_airport_data(stat):
    airport_stdout = subprocess.Popen(
        ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
         "-I"], stdout=subprocess.PIPE)
    airport_data = airport_stdout.communicate()[0].decode("utf-8").split('\n')   # [0] is stdout, [1] is stderr
    airport_data = data_filter(airport_data, stat)
    return airport_data


def check_wifi_on():
    if "AirPort: Off" in get_airport_data(""):
        sys.exit("Wireless Off. Exiting...\n")
    else:
        pass


def get_SSID():  # Returns SSID of the connected wifi network from osx
    SSID = get_airport_data("SSID")
    return SSID


def get_channel():  # Returns the channel info of the connected wifi network from osx
    channel = get_airport_data("channel")
    return channel


def calculate_freq(channel):  # Determines if 2.4g of 5g network. Requires int input
    channel = channel.rsplit(":")[-1].split(",")
    for x in channel:
        if 1 <= int(x) <= 11:
            return "2.4 Ghz"
        elif 30 <= int(x) <= 88:
            return "5 Ghz"
        else:
            return "Wifi Frequency Unknown"


def measure_tx():  # Returns wifi tx rate from osX
    tx_string = get_airport_data("lastTxRate")
    tx_value = return_numbers(tx_string)
    return tx_value

def get_max_tx():
    tx_max_string = get_airport_data("maxRate")
    tx_max_value = return_numbers(tx_max_string)
    return tx_max_value


try:
    """Start up messages"""
    print("Starting Wifi TX Tracker\n(Use cntl +c to end)\n")
    check_wifi_on()
    wifi_channel = get_channel()
    print("{}\n{} - {}\n".format(get_SSID(), wifi_channel, calculate_freq(wifi_channel)))
    time.sleep(1)
except (KeyboardInterrupt):
    sys.exit("\nKeyboared Interrupt, Exiting...\n")

while True:
    try:
        print("{} - {} / {} Mbps".format(time_now(), measure_tx(), get_max_tx()))
        time.sleep(2)
    except (KeyboardInterrupt):
        sys.exit("\nKeyboard Interrupt, Exiting...\n")
