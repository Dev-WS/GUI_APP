import time
import serial
import tkinter as tk
import tkinter.messagebox as msb
import serial.tools.list_ports
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W


class ConsolePlotUi:
    def __init__(self, frame):
        self.frame = frame
        ttk.Label(self.frame, text='Test1').grid(column=0, row=1, sticky=W)
        ttk.Label(self.frame, text='Test1').grid(column=0, row=4, sticky=W)

class ConsoleUi:
    def __init__(self, frame):
        self.frame = frame
        ttk.Label(self.frame, text='Test2').grid(column=0, row=1, sticky=W)
        ttk.Label(self.frame, text='Test2').grid(column=0, row=4, sticky=W)

class ConsoleBoardUi:
    def __init__(self, frame):
        self.frame = frame
        ttk.Label(self.frame, text='Test3').grid(column=0, row=1, sticky=W)
        ttk.Label(self.frame, text='Test3').grid(column=0, row=4, sticky=W)

        self.button_connect = ttk.Button(self.frame, text="CONNECT", command=print('connected'))
        self.button_connect.grid(column=1, row=2, sticky=W)

        self.connected = []
        self.ports = serial.tools.list_ports.comports()
        for port in self.ports:
            self.connected.append(port.device)

        self.create_combobox(self.connected)

    def create_combobox(self, values):
        self.cb_value = tk.StringVar()
        self.combobox = ttk.Combobox(self.frame, textvariable=self.cb_value)
        #self.combobox.place(x=0, y=10)
        self.combobox.grid(column=2, row=3, sticky=W)
        self.combobox['values'] = values
        self.combobox.current(0)
        self.combobox.bind("<<ComboboxSelected>>", self.on_select_changed)

    def on_select_changed(self, event):
        msb.showinfo("Info", self.cb_value.get())


class Application:
    def __init__(self, root):
        self.root = root
        root.title('GUI_APP')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        vertical_pane = ttk.PanedWindow(self.root, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky="nsew")
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)

        controlboard_frame = ttk.Labelframe(horizontal_pane, text="Control Board")
        controlboard_frame.columnconfigure(1, weight=1)
        horizontal_pane.add(controlboard_frame, weight=1)

        plot_frame = ttk.Labelframe(horizontal_pane, text="Plot")
        plot_frame.columnconfigure(1, weight=1)
        horizontal_pane.add(plot_frame, weight=1)

        console_frame = ttk.Labelframe(vertical_pane, text="Console")
        vertical_pane.add(console_frame, weight=1)

        self.consoleboard = ConsoleBoardUi(controlboard_frame)
        self.console = ConsoleUi(console_frame)
        self.plotboard = ConsolePlotUi(plot_frame)

        self.root.protocol('WM_DELETE_WINDOW', self.stop_app)

    def stop_app(self):
        self.root.destroy()
        print('App Closed')
        #serial_port.close()


def main():
    root = tk.Tk()
    app = Application(root)
    app.root.mainloop()


if __name__ == '__main__':
    main()