#!/usr/bin/env python3
"""
Continuously output tx rate of wifi
"""

import re
import sys
import time
import argparse
import subprocess

__author__ = "Nick Everett"
__version__ = "0.5.0"
__license__ = "GNU GPLv3"


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


def bits_to_bytes(number):  # converts input to bytes
    number = int(number)
    number /= 8
    return number


def return_numbers(string):  # Returns only numbers as string from an input string
    values = re.findall("\d", string)
    return "".join(values)


def measure_tx(airport_data):      # Returns wifi tx rate from osX
    tx_string = data_filter(airport_data, "lastTxRate")
    tx_value = return_numbers(tx_string)
    tx_max_string = data_filter(airport_data, "maxRate")
    tx_max_value = return_numbers(tx_max_string)
    return tx_value, tx_max_value


def parse_args():       # Command line arguments
    description = (
        'Command line interface for testing wifi transmission speed\n'
        '------------------------------------------------------------'
        '--------------\n'
        'https://github.com/nickever/wifitx')

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-i", type=int, dest="interval", action="store", default=5,
                        help="interval between each wifi tx measurement"
                             " in seconds. Default is 5.")
    parser.add_argument("-c", type=int, dest="count", action="store", default=float("inf"),
                        help="number of times to repeat the wifi tx measurement.")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="verbosity (-v, -vv, etc)")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))
    parser.add_argument("-b", "--bytes", dest="bytes", action="store_true", default=False,
                        help="wifi tx rate is in Megabytes per second.")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    try:       # Start up messages
        print("Starting Wifi TX Tracker\n(Use cntl +c to end)\n")
        initial_data = get_airport_data()
        check_wifi_connection(initial_data, True)
        network = get_network(initial_data)
        print("{}\n{} - {}\n".format(network[0],network[1], calculate_freq(network[1])))
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit("\nKeyboard Interrupt, Exiting...\n")

    while args.count > 0:     # Loop to report wifi tx and time stamp
        try:
            airport_data = get_airport_data()
            connection_status = check_wifi_connection(airport_data)
            tx = measure_tx(airport_data)
            if args.bytes is True:
                print("{} - {} / {} MBps {}".format(time_now(), bits_to_bytes(tx[0]),
                                                    bits_to_bytes(tx[1]), connection_status))
            else:
                print("{} - {} / {} Mbps {}".format(time_now(), tx[0], tx[1], connection_status))
                args.count -= 1
            if args.count > 0:
                time.sleep(args.interval)
            else:
                sys.exit("\nComplete. Exiting...\n")
        except KeyboardInterrupt:
            sys.exit("\nKeyboard Interrupt, Exiting...\n")


if __name__ == "__main__":      # executed when run from the command line
    main()
