# -*- coding: utf-8 -*-

"""
Distance sensor by TeraRanger Evo Mini.

・PySerial is required.
・PRINT OUT MODE = TEXT / PIXEL MODE = PIXEL1 / RANGE MODE = LONG
"""

import serial, queue, threading, time

PRINTOUT_TEXT = bytearray(b'\x00\x11\x01\x45')
PX1 = bytearray(b'\x00\x21\x01\xBC')
RANGE_LONG = bytearray(b'\x00\x61\x03\xE9')

class TeraRangerEvoMini:
    def __init__(self, port='COM1', baudrate=115200, bytesize=8, parity='N', stopbits=1):
        """
        Initialize.
        """
        self.conn = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits)
        self.conn.write(PX1)
        self.conn.write(RANGE_LONG)
        self.conn.write(PRINTOUT_TEXT)
        print('------------------------')
        print('TeraRangerEvoMini.__init__')
        print('------------------------')
        print('Port = {0}'.format(port))
        print('Baud Rate = {0}'.format(baudrate))
        print('Byte Size = {0}'.format(bytesize))
        print('Parity = {0}'.format(parity))
        print('Stop Bits = {0}'.format(stopbits))
        print('PRINT OUT MODE = TEXT')
        print('PIXEL MODE = PIXEL1')
        print('RANGE MODE = LONG')
        for i in range(20):
            val = self._get_until_lf()
            print('Check value : {0}'.format(val))
        self.q = queue.Queue()
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()
    def __del__(self):
        """
        Shutdown.
        """
        self.t.join(0)
        self.conn.close()
    def _get_until_lf(self):
        """
        Read until LF.
        """
        try:
            val = ''
            res = ''
            while res != '\n':
                val = val + res
                res = self.conn.read().decode()
            return int(val)
        except:
            return -1
    def _reader(self):
        """
        The queue always contains the latest values.
        """
        while True:
            val = self._get_until_lf()
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(val)
    def open(self):
        """
        Open.
        """
        try:
            if self.conn.isOpen():
                return
            else:
                self.conn.open()
            print('Reopen.')
        except Exception as e:
            print(e)
    def isConnect(self):
        """
        Check connection.
        
        * Closes when an error occurs.
        """
        try:
            if not self.conn.isOpen():
                self.conn.open()
            bret = self.conn.write(PRINTOUT_TEXT) == 4
            return bret
        except Exception as e:
            print(e)
            self.conn.close()
            return False
    def getDistance(self):
        """
        Measure the distance.
        """
        try:
            if not self.conn.isOpen():
                self.conn.open()
            t_start = time.time()
            val = self.q.get()
            proc_time = time.time() - t_start
            print('calc time : {0} ms'.format(proc_time))
            return val
        except Exception as e:
            print(e)
            return -1
