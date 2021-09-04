#!/usr/bin/env python3
# ls -dev
# python client.py --host 127.0.0.1 --tty /dev/ttyUSB0
# ex: set tabstop=8 softtabstop=0 expandtab shiftwidth=2 smarttab:

import socket
import sys
import importlib, client_misc
import json
import argparse
import os

from dmx_allan import PyDMX, DMXlight

from pprint import pprint as pp

parser = argparse.ArgumentParser()
parser.add_argument("--host", required=True,
                  help="Host/IP for the server")
parser.add_argument("--tty", required=True,
                  help="The serial port used for DMX")
parser.add_argument("--x-constant", required=False, type=float, default=0.6)
parser.add_argument("--y-constant", required=False, type=float, default=0.6)

args = parser.parse_args()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (args.host, 10000)
sock.connect(server_address)

dmx = PyDMX(args.tty)
dmx.start()
light = DMXlight(dmx)
light.degrees(359, 0)

try:
    while True:
        try:
            data = json.loads(sock.recv(4096).decode('utf-8'))
        except json.decoder.JSONDecodeError:
            data = None

        if data:
            data = sorted(data, key=lambda x: x['class_id'])[0]

            class_id = data['class_id']

            # Reload calc module
            if os.path.isfile(client_misc.__file__):
                importlib.reload(client_misc)

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
                if client_misc.skip_class_id(class_id):
                  dmx.setData(8, 0)
                  continue

            dmx.setData(8, 100)

            x_degrees, y_degrees = client_misc.pixel2degrees(
              data['x'], data['width'],
              data['y'], data['height'],
            )
            light.degrees(x_degrees, y_degrees)
            print('class_id: {}, x: {}, y:{}'.format(data['class_id'], x_degrees, y_degrees))

        else:
            light.degrees(0, 90)
            dmx.setData(8, 0)

except KeyboardInterrupt:
    dmx.stop()

