"""
Test script to check the output of the VLC atmolight plugin.

Connect to a (virtual) COM port where the atmolight protocol is send
through and display the content.

1. Create a virtual COM port using socat:
    $> socat PTY,link=ttyS10 PTY,link=ttyS11

2. Setup VLC by enabling the AtmoLight Filter:
    - Check Preferences -> Video -> Filters -> AtmoLight Filter
    - Enter the virtual serial port into the AtmoLight Filter's property window
    - Save
    - Restart VLC and start a video (check console output for errors)

3. Start this script (Python 3)
"""

import tkinter as tk
from tkinter import ttk

import serial
import time
import threading
import traceback

protocol = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

class SerialThread(threading.Thread):
    def __init__(self, com_port):
        threading.Thread.__init__(self)
        self.com_port = com_port

    def run(self):
        try:
            self.open_serial()
            while True:
                for index, item in enumerate(self.connection.read(19)):
                    protocol[index] = item
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

class ChannelWidget(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.r = tk.IntVar()
        self.g = tk.IntVar()
        self.b = tk.IntVar()

        self.prg_channel_r = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255, variable=self.r)
        self.prg_channel_g = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255, variable=self.g)
        self.prg_channel_b = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255, variable=self.b)

        self.grid(column=3, row=1)
        self.prg_channel_r.grid(column=0, row=0)
        self.prg_channel_g.grid(column=1, row=0)
        self.prg_channel_b.grid(column=2, row=0)

    def update(self, r, g, b):
        self.r.set(r)
        self.g.set(g)
        self.b.set(b)

class AtmoDummy(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.mainframe = ttk.Frame(self)
        self.mainframe.grid(column=4, row=1)

        self.channel_1 = ChannelWidget(self.mainframe)
        self.channel_2 = ChannelWidget(self.mainframe)
        self.channel_3 = ChannelWidget(self.mainframe)
        self.channel_4 = ChannelWidget(self.mainframe)
        
        self.channel_1.grid(column=0, row=0)
        self.channel_2.grid(column=1, row=0)
        self.channel_3.grid(column=2, row=0)
        self.channel_4.grid(column=3, row=0)

        #self.button = ttk.Button(text="start", command=self.start)
        #self.button.grid(column=3, row=0)

        #self.button5 = ttk.Button(text="start5", command=self.start5)
        #self.button5.grid(column=4, row=0)

        self.after(50, self.update_gui)

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
        self.channel_1.update(protocol[ 7], protocol[ 8], protocol[ 9])
        self.channel_2.update(protocol[10], protocol[11], protocol[12])
        self.channel_3.update(protocol[13], protocol[14], protocol[15])
        self.channel_4.update(protocol[16], protocol[17], protocol[18])
        self.after(50, self.update_gui)

if __name__ == "__main__":
    try:
        reader = SerialThread("/dev/pts/6")
        reader.start()

        app = AtmoDummy()
        app.mainloop()
    except:
        traceback.print_exc()