import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msb
import serial
import serial.tools.list_ports
import time



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        
        self.master = master
        self.pack()
        self.create_widgets()
        self.serial_ports()
        self.create_combobox(self.connected)
        self.create_textbox()

        for check in self.connected:
            if check == 'COM3':
                self.serial_connect()
        #self.serial_connect()

        print(self.connected)


    def create_textbox(self):
        self.textbox = tk.Text()
        self.textbox.pack(side="bottom")

        self.textbox.insert(tk.INSERT, "Conneted COM's:\n")
        self.textbox.insert(tk.END, self.connected)

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")


    def create_button(self):
        self.button = tk.Button(self)
        self.button["text"] = "button"
        self.button["command"] = print("clicked button")


    def create_combobox(self, values):

        self.cb_value = tk.StringVar()
        self.combobox = ttk.Combobox(root, textvariable = self.cb_value)

        self.combobox.place(x= 0, y=10)
        self.combobox['values'] = values
        self.combobox.current(0) 
        self.combobox.bind("<<ComboboxSelected>>", self.on_select_changed)

    def on_select_changed(self, event):
        msb.showinfo("Info", self.cb_value.get())

    def serial_ports(self):

        self.connected = []
        self.ports = serial.tools.list_ports.comports()
        for port in self.ports:
            self.connected.append(port.device)

    def serial_connect(self):

        self.serial_port = serial.Serial(port="COM3", baudrate=115200, bytesize=8, timeout=2, stopbits= serial.STOPBITS_ONE)
        print(self.serial_port.name)
        res = self.serial_port.read()
        print(res)
        print('1')

  
root = tk.Tk()
root.geometry('500x500')
root.title('GUI_APP')

root = Application(master=root)
root.mainloop()