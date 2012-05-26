"""
Test script to check the output of the VLC atmolight plugin.

Connect to a (virtual) COM port where the atmolight protocol is send
through and display the content.
"""

import tkinter as tk
from tkinter import ttk

import serial
import time
import threading
import traceback

channel_left = [0, 0, 0]

class SerialThread(threading.Thread):
    def __init__(self, com_port):
        threading.Thread.__init__(self)
        self.com_port = com_port

    def run(self):
        try:
            self.open_serial()
            while True:
                #data = self.connection.read(19)
                #data_ord = [ord(x) for x in data]
                data_ord = self.connection.read(19)
                channel_left[0] = data_ord[7]
                channel_left[1] = data_ord[8]
                channel_left[2] = data_ord[9]
        except KeyboardInterrupt:
            self.close_serial()

    def open_serial(self):
        self.connection = serial.Serial(self.com_port,
                                        baudrate=38400,
                                        parity=serial.PARITY_NONE,
                                        bytesize=serial.EIGHTBITS,
                                        stopbits=serial.STOPBITS_ONE)

    def close_serial(self):
        self.connection.close()

class AtmoDummy(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.content = ttk.Frame(self)

        self.left_r = tk.IntVar()
        self.left_g = tk.IntVar()
        self.left_b = tk.IntVar()

        #self.progress_channel0 = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255)
        self.progress_channel1_r = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255, variable=self.left_r)
        self.progress_channel1_g = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255, variable=self.left_g)
        self.progress_channel1_b = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255, variable=self.left_b)
        #self.progress_channel2 = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255)
        #self.progress_channel3 = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255)
        #self.progress_channel4 = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255, variable=self.i0)

        #self.progress_channel1_r["background"] = "red"
        self.content.grid(column=5, row=1)
        #self.progress_channel0.grid(column=0, row=0)
        self.progress_channel1_r.grid(column=0, row=0)
        self.progress_channel1_g.grid(column=1, row=0)
        self.progress_channel1_b.grid(column=2, row=0)
        #self.progress_channel2.grid(column=2, row=0)
        #self.progress_channel3.grid(column=3, row=0)
        #self.progress_channel4.grid(column=4, row=0)

        #self.button = ttk.Button(text="start", command=self.start)
        #self.button.grid(column=3, row=0)

        #self.button5 = ttk.Button(text="start5", command=self.start5)
        #self.button5.grid(column=4, row=0)

        self.after(100, self.update_gui)

    #def start(self):
        #self.progress_channel0["value"] = 0
        #self.read_bytes()

    #def read_bytes(self):
        #self.progress_channel0["value"] += 1
        #if self.progress_channel0["value"] < self.progress_channel0["maximum"]:
            #self.after(100, self.read_bytes)

    #def start5(self):
        #self.i0.set(0)
        #self.read_bytes5()

    #def read_bytes5(self):
        #self.i0.set(self.i0.get() + 1)
        #if self.i0.get() < self.progress_channel0["maximum"]:
            #self.after(75, self.read_bytes5)

    def update_gui(self):
        self.left_r.set(channel_left[0])
        self.left_g.set(channel_left[1])
        self.left_b.set(channel_left[2])
        self.after(100, self.update_gui)

if __name__ == "__main__":
    try:
        reader = SerialThread("/dev/pts/6")
        reader.start()

        app = AtmoDummy()
        app.mainloop()
    except:
        traceback.print_exc()