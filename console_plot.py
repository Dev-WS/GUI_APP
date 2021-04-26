

import serial
import tkinter as tk
import tkinter.messagebox as msb
import serial.tools.list_ports

from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W


class ConsolePlotUi:
    def __init__(self, frame):
        self.frame = frame
        ttk.Label(self.frame, text='Test1').grid(column=0, row=1, sticky=W)
        ttk.Label(self.frame, text='Test1').grid(column=0, row=4, sticky=W)
