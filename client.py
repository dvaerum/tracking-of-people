#!/usr/bin/env python3
# ls -dev
# python client.py --host 127.0.0.1 --tty /dev/ttyUSB0
# ex: set tabstop=8 softtabstop=0 expandtab shiftwidth=2 smarttab:

import socket
import sys
import importlib
import json
import argparse

from dmx_allan import PyDMX, DMXlight

from pprint import pprint as pp

args = argparse.ArgumentParser()
args.add_argument("--host", required=True,
                  help="Host/IP for the server")
args.add_argument("--tty", required=True,
                  help="The serial port used for DMX")
args.add_argument("--x-constant", required=False, type=float, default=0.6)
args.add_argument("--y-constant", required=False, type=float, default=0.6)

args = args.parse_args()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (args.host, 10000)
sock.connect(server_address)

dmx = PyDMX(args.tty)
dmx.start()
light = DMXlight(dmx)
light.degrees(359, 0)

x_constant = (1920 / 61) * args.x_constant * -1
# x_constant = 43
y_constant = (1080 / 32) * args.y_constant * -1

try:
    while True:
        data = json.loads(sock.recv(4096).decode('utf-8'))
        if data:
            data = sorted(data, key=lambda x: x['class_id'])[0]

            class_id = data['class_id']
            if class_id == 0:
                dmx.setData(5, 0)
            elif class_id == 56:
                # yellow: 70
                # orange: 50
                # red: 30
                # green: 90
                # blue: 110
                dmx.setData(5, 110)
            else:
                dmx.setData(8, 0)
                continue

            dmx.setData(8, 100)
            x_center = (data['x'] + (data['width'] / 2))
            x_degrees = 35 + x_center / x_constant
            if x_degrees > 360.0:
                x_degrees = x_degrees - 360.0
            elif x_degrees < 0:
                x_degrees = x_degrees + 360.0

            y_degrees = 24 + data['y'] / y_constant
            print('class_id: {}, x: {}, y:{}'.format(data['class_id'], x_degrees, y_degrees))
            light.degrees(x_degrees, y_degrees)

        else:
            light.degrees(0, 90)
            dmx.setData(8, 0)

except KeyboardInterrupt:
    dmx.stop()
