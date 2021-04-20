import time
import serial
import tkinter as tk
import tkinter.messagebox as msb
import serial.tools.list_ports

from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
import threading

import datetime
import queue
import logging
import signal


logger = logging.getLogger(__name__)

class Clock(threading.Thread):
    """Class to display the time every seconds
    Every 5 seconds, the time is displayed using the logging.ERROR level
    to show that different colors are associated to the log levels
    """
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        logger.debug('Clock started')
        previous = -1
        while not self._stop_event.is_set():
            now = datetime.datetime.now()
            if previous != now.second:
                previous = now.second
                if now.second % 5 == 0:
                    level = logging.ERROR
                else:

                    level = logging.INFO

                logger.log(level, now)
            time.sleep(0.2)

    def stop(self):
        self._stop_event.set()


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue
    It can be used from different threads
    The ConsoleUi class polls this queue to display records in a ScrolledText widget
    """
    # Example from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06
    # (https://stackoverflow.com/questions/13318742/python-logging-to-tkinter-text-widget) is not thread safe!
    # See https://stackoverflow.com/questions/43909849/tkinter-python-crashes-on-new-thread-trying-to-log-on-main-thread

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class ConsolePlotUi:
    def __init__(self, frame):
        self.frame = frame
        ttk.Label(self.frame, text='Test1').grid(column=0, row=1, sticky=W)
        ttk.Label(self.frame, text='Test1').grid(column=0, row=4, sticky=W)

class ConsoleUi:
    def __init__(self, frame):
        self.frame = frame

        self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('ERROR', foreground='red')

        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        self.frame.after(10, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)


    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)

        self.frame.after(1000, self.poll_log_queue)


class ConsoleBoardUi:
    def __init__(self, frame):
        self.frame = frame
        ttk.Label(self.frame, text='Test3').grid(column=0, row=1, sticky=W)
        ttk.Label(self.frame, text='Test3').grid(column=0, row=4, sticky=W)

        #self.create_button_connect()
        #threading.Thread(target=self.create_button_connect).start()


        self.connected = []
        self.ports = serial.tools.list_ports.comports()
        for port in self.ports:
            self.connected.append(port.device)

        self.create_combobox(self.connected)

        self.create_button_connect()

        self.read_serialport()
        #self.connect_serial()

    def create_button_connect(self):
        self.button_connect = ttk.Button(self.frame, text="CONNECT", command=self.print_smthg)
        self.button_connect.grid(column=0, row=3, sticky=W)

        getport = self.combobox.get()
        getport_status = self.combobox.current()


        print("Getport values is:", getport, "status:", getport_status)
        self.button_connect.bind('<Button-1>', self.serial_connect('COM3'))


    def print_smthg(self):
        print(str(test))

    def create_combobox(self, values):
        self.cb_value = tk.StringVar()
        self.combobox = ttk.Combobox(self.frame, textvariable=self.cb_value)
        #self.combobox.place(x=0, y=10)
        self.combobox.grid(column=0, row=2, sticky=W)
        self.combobox['values'] = values
        self.combobox.current(0)
        self.combobox.bind("<<ComboboxSelected>>", self.on_select_changed)

    def on_select_changed(self, event):
        msb.showinfo("Info", str(self.cb_value.get()))
        print(self.combobox.get())

        return self.combobox.get()


    def connect_serial(self):

        print(self.combobox.get())

        port_number = self.combobox.get()
        print(str(self.on_select_changed))
        self.serial_connect(port_number)
        self.open_serial_com3 = True

    def serial_connect(self, port_number):

        self.serial_port = serial.Serial(port=port_number, baudrate=115200, bytesize=8, timeout=2, stopbits= serial.STOPBITS_ONE)
        print(self.serial_port.name)
        res = self.serial_port.readline()
        print(res)
        print('1')


    def read_serialport(self):

        readedvalue = self.serial_port.read()
        print(readedvalue)
        self.frame.after(100, self.read_serialport)


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

        self.clock = Clock()
        self.clock.start()


        #loop = threading.Thread(target=self.infinitie_loop).start()
        #loop.start()

    def infinitie_loop(self):

        # test += 1
        # if test > 10000:
        #     test = 0
        # print(test)
        self.root.after(100, self.infinitie_loop)


    def stop_app(self):
        self.root.destroy()
        self.clock.stop()
        #loop.stop()
        print('App Closed')
        #serial_port.close()


def main():
    global test
    test = 0

    root = tk.Tk()
    app = Application(root)
    app.root.mainloop()


if __name__ == '__main__':
    main()