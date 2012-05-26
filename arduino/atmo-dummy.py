"""
Test script to check the output of the VLC atmolight plugin.

Connect to a (virtual) COM port where the atmolight protocol is send
through and display the content.
"""

import tkinter as tk
from tkinter import ttk

# Still under development, does not work yet at all.
class AtmoDummy(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.content = ttk.Frame(self)
        
        self.i0 = tk.IntVar()
        self.i0.set(64)

        self.progress_channel0 = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255)
        self.progress_channel1 = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255)
        self.progress_channel2 = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255)
        self.progress_channel3 = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255)
        self.progress_channel4 = ttk.Progressbar(self, orient=tk.VERTICAL, length=255, mode="determinate", maximum=255, variable=self.i0)

        self.content.grid(column=7, row=1)
        self.progress_channel0.grid(column=0, row=0)
        self.progress_channel1.grid(column=1, row=0)
        self.progress_channel2.grid(column=2, row=0)
        self.progress_channel3.grid(column=3, row=0)
        self.progress_channel4.grid(column=4, row=0)

        self.button = ttk.Button(text="start", command=self.start)
        self.button.grid(column=5, row=0)

        self.button5 = ttk.Button(text="start5", command=self.start5)
        self.button5.grid(column=6, row=0)

    def start(self):
        self.progress_channel0["value"] = 0
        self.read_bytes()

    def read_bytes(self):
        self.progress_channel0["value"] += 1
        if self.progress_channel0["value"] < self.progress_channel0["maximum"]:
            self.after(100, self.read_bytes)

    def start5(self):
        self.i0.set(0)
        self.read_bytes5()

    def read_bytes5(self):
        self.i0.set(self.i0.get() + 1)
        if self.i0.get() < self.progress_channel0["maximum"]:
            self.after(75, self.read_bytes5)

if __name__ == "__main__":
  try:
    app = AtmoDummy()
    app.mainloop()
  except:
    traceback.print_exc()