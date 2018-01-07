#!/usr/bin/env Python3

"""Coninuiously output tx rate of wifi"""

import os
import re
import time


def return_numbers(string):   # Returns only numbers from an input string
    values = re.findall("\d",string)
    return "".join(values)


def time_now():     # Returns time when run
    time_now = time.strftime("%H:%M:%S", time.gmtime())
    return time_now


def get_SSID():     # Returns SSID of the connected wifi network from osx
    SSID = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep ' SSID'").readline()
    SSID = SSID.strip(" \n")
    return SSID

def get_channel():      # Returns the channel info of the connected wifi network from osx
    channel = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep channel").readline()
    channel = channel.strip(" \n")
    return channel


def calc_freq(channel):     # Determines if 2.4g of 5g network. Requires int input
    if 1 <= channel <= 11:
        return "2.4Ghz"
    elif 3000 <= channel <= 8800:
        return "5Ghz"
    else:
        return "Wifi Frequency Unknown"


def measure_tx():  # Returns wifi tx rate from osX
    tx = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep lastTxRate").readline()
    return (tx)

"""Start up messages"""
print("Starting Wifi TX Tracker\n(Use cntl +c to end)\n")
channel_number = get_channel()
channel_number = int(return_numbers(channel_number))
print("{}\n{} - {}\n".format(get_SSID(), get_channel(), calc_freq(channel_number)))
time.sleep(1)


while True:
    measure_value = measure_tx()
    measure_value = return_numbers(measure_value)
    measure_time = time_now()
    print("{} - {} Mbps".format(measure_time, measure_value))
    time.sleep(2)
