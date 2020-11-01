# ex: set tabstop=8 softtabstop=0 expandtab shiftwidth=2 smarttab:

import serial
import time
import numpy as np

import threading

import logging


class PyDMX:
    def __init__(self,port):
        #start serial
        self.serial = serial.Serial(port,baudrate=250000,bytesize=8,stopbits=2)
        self.data = np.zeros([513],dtype='uint8')

        self.data[0] = 0 # StartCode

        # Delete this _
        self.breakus = 88 + 4
        self.MABus = 8 + 4


    def setData(self,id,data):
        self.data[id]=data

    def showData(self):
        print(self.data)

    def start(self):
      self._t = threading.Thread(target=self._send)
      self._run = True
      self._t.start()

    def stop(self):
      self._run = False

    def _send(self):
      while self._run:
        # self.showData()

        # Send Break : 88us - 1s
        self.serial.break_condition = True
        time.sleep(self.breakus/1e6)
       
        # Send MAB : 8us - 1s
        self.serial.break_condition = False
        time.sleep(self.MABus/1e6)
       
        # Send Data
        self.serial.write(bytearray(self.data))
       
        # Sleep
        # time.sleep(8) # between 0 - 1 sec

    def sendZero(self):
        self.data = np.zeros([513],dtype='uint8')
        self._send()

    def __del__(self):
        print('Close serial server!')
        self._run = False
        self.sendZero()
        self.serial.close()


class DMXlight:
  _dmx = None
  _dmx_x = None
  _dmx_y = None
  dmx_x_channel = None
  dmx_y_channel = None

  _y = None
  _x = None

  _x_constant = 255/540
  _y_constant = 208/180

  def __init__(self, dmx: PyDMX, dmx_x: int = 0, dmx_y: int = 27, dmx_x_channel: int = 1, dmx_y_channel: int = 3):
    self._dmx = dmx
    self._dmx_x = dmx_x
    self.dmx_x_channel = dmx_x_channel
    self._dmx_y = dmx_y
    self.dmx_y_channel = dmx_y_channel
    self._x = 0.0
    self._y = 0.0

  def degrees(self, x: float = None, y: float = None):
    if not x == None:
      if x < 0.0:
        x = 0.0
      elif x > 360.0:
        x = 360.0

      short_path = (x - self._x + 540) % 360 - 180
      logging.debug('self._x: {} - short_path: {}'.format(self._x, short_path))
      if self._x + short_path > 540.0:
        new_x = self._x + short_path - 360
        self._dmx.setData(self.dmx_x_channel, self._x_constant * new_x)
        self._x = new_x
      elif self._x + short_path < 0.0:
        new_x = self._x + short_path + 360
        self._dmx.setData(self.dmx_x_channel, self._x_constant * new_x)
        self._x = new_x
      else:
        new_x = self._x + short_path
        self._dmx.setData(self.dmx_x_channel, self._x_constant * new_x)
        self._x = new_x

    if not y == None:
      self._y = y

      tmp_y = int(self._y_constant * self._y + self._dmx_y)
      if tmp_y < 0:
        tmp_y = 0
      elif tmp_y > 255:
        tmp_y = 255
      self._dmx.setData(self.dmx_y_channel, tmp_y)



