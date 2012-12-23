import sys
import serial
import time
import threading
import traceback

protocol = [
    255,
    0, 0, 0,
    0, 0, 0,
    0, 0, 0,
    254, 0, 0,
    0, 254, 0,
    0, 0, 0
]

class SerialThread(threading.Thread):
    def __init__(self, com_port):
        super(SerialThread, self).__init__()
        self.com_port = com_port
        self.stop_requested = False

    def run(self):
        try:
            self.open_serial()
            while not self.stop_requested:
                self.connection.write(bytes(protocol))
            self.close_serial()
        except:
            traceback.print_exc()
            self.close_serial()

    def stop(self):
        self.stop_requested = True

    def open_serial(self):
        self.connection = serial.Serial(self.com_port,
                                        baudrate=38400,
                                        parity=serial.PARITY_NONE,
                                        bytesize=serial.EIGHTBITS,
                                        stopbits=serial.STOPBITS_ONE,
                                        timeout=1)

    def close_serial(self):
        self.connection.close()

if __name__ == "__main__":
    try:
        reader = SerialThread(sys.argv[1])
        reader.start()
        reader.join()
    except:
        traceback.print_exc()
