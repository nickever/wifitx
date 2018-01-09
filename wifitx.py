#!/usr/bin/env Python3

"""Continuously output tx rate of wifi"""

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


def data_filter(data, search_term=None):     # Filters input data list by search term.
    data = [x.strip() for x in data if x.strip()]
    if search_term is not None:
        for item in data:
            if item.startswith(search_term):
                return item
    else:
        return data


def get_airport_data():     # Fetches wifi data from terminal command
    airport_stdout = subprocess.Popen(
        ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
         "-I"], stdout=subprocess.PIPE)
    airport_data = airport_stdout.communicate()[0].decode("utf-8").split('\n')  # [0] is stdout, [1] is stderr
    return airport_data


def check_wifi_connection(airport_data, startup=False):     # Check wifi on and network connected
    airport_data = data_filter(airport_data, None)
    if "AirPort: Off" in airport_data:
        sys.exit("Wireless Off. Exiting...\n")
    elif "BSSID: 0:0:0:0:0:0" in airport_data:
        if startup is True:
            sys.exit("No Wireless Network Connection, Exiting...\n")
        else:
            return " - * Wireless Network Connection Disconnected *"
    else:
        return ""


def get_network(airport_data):  # Returns SSID and channel of the connected wifi network from osx
    SSID = data_filter(airport_data, "SSID")
    channel = data_filter(airport_data, "channel")
    return SSID, channel


def calculate_freq(channel):  # Determines if 2.4g of 5g network. Requires int input
    channel = channel.rsplit(":")[-1].split(",")
    for x in channel:
        if 1 <= int(x) <= 11:
            return "2.4 Ghz"
        elif 30 <= int(x) <= 88:
            return "5 Ghz"
        else:
            return "Wifi Frequency Unknown"


def measure_tx(airport_data):      # Returns wifi tx rate from osX
    tx_string = data_filter(airport_data, "lastTxRate")
    tx_value = return_numbers(tx_string)
    tx_max_string = data_filter(airport_data, "maxRate")
    tx_max_value = return_numbers(tx_max_string)
    return tx_value, tx_max_value


try:       # Start up messages
    print("Starting Wifi TX Tracker\n(Use cntl +c to end)\n")
    initial_data = get_airport_data()
    check_wifi_connection(initial_data, True)
    network = get_network(initial_data)
    print("{}\n{} - {}\n".format(network[0], network[1], calculate_freq(network[1])))
    time.sleep(1)
except KeyboardInterrupt:
    sys.exit("\nKeyboard Interrupt, Exiting...\n")

while True:     # Loop to report wifi tx and time stamp
    try:
        airport_data = get_airport_data()
        connection_status = check_wifi_connection(airport_data)
        tx = measure_tx(airport_data)
        print("{} - {} / {} Mbps {}".format(time_now(), tx[0], tx[1], connection_status))
        time.sleep(5)
    except KeyboardInterrupt:
        sys.exit("\nKeyboard Interrupt, Exiting...\n")
