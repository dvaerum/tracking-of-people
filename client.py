#!/usr/bin/env python3

# ex: set tabstop=8 softtabstop=0 expandtab shiftwidth=2 smarttab:

import socket
import sys
import json
import argparse

from dmx_alan import PyDMX, DMXlight

from pprint import pprint as pp

arg = argparse.ArgumentParser()
arg.add_argument("--host", required=True,
  help="Host/IP for the server")
arg.add_argument("--tty", required=True,
  help="The serial port used for DMX")
args = arg.parse_args()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (args.host, 10000)
sock.connect(server_address)

dmx = PyDMX(args.tty)
dmx.start()
light = DMXlight(dmx)
light.degrees(359, 0)

x_constant = (1920 / 61) * 0.6
#x_constant = 43
y_constant = (1080 / 32) * 0.6

while True:
  data = json.loads(sock.recv(4096).decode('utf-8'))
  if data:
    data = sorted(data, key=lambda x: x['class_id'])[0]

    if data['class_id'] == 0:
      dmx.setData(5, 0)
    elif data['class_id'] == 56:
      # yellow: 70
      # orange: 50
      # red: 30
      # green: 90
      # blue: 110
      dmx.setData(5,110)

    dmx.setData(8, 100)
    x_center = (data['x'] + (data['width'] / 2))
    x_degrees = 335 + x_center / x_constant
    if x_degrees > 360.0:
      x_degrees = x_degrees - 360.0

    y_degrees = -14 + data['y'] / y_constant
    print('x: {}, y:{}'.format(x_degrees, y_degrees))
    light.degrees(x_degrees, y_degrees)

  else:
    light.degrees(0, 90)
    dmx.setData(8,0)

    





