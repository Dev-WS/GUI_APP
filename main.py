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
        self.create_label()

        for check in self.connected:
            if check == 'COM3':
                self.serial_connect()
                self.open_serial_com3 = True
            else:
                self.open_serial_com3 = False
        #self.serial_connect()

        self.testx = 1

        self.update()

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
                              command=self.stop_app)
        self.quit.pack(side="bottom")

    def stop_app(self):
        self.master.destroy()

        if self.open_serial_com3:
            self.serial_port.close()
        #self.quit.configure(command =self.master.destroy)

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

    def create_label(self):
        self.label = tk.Label(root, text="Label Text")
        self.label.pack()

    def serial_ports(self):

        self.connected = []
        self.ports = serial.tools.list_ports.comports()
        for port in self.ports:
            self.connected.append(port.device)

    def serial_connect(self):

        self.serial_port = serial.Serial(port="COM3", baudrate=115200, bytesize=8, timeout=2, stopbits= serial.STOPBITS_ONE)
        print(self.serial_port.name)
        res = self.serial_port.readline()
        print(res)
        print('1')

    def update(self):



        self.label.config(text=str(self.serial_port.readline()))
        print("serial:", self.serial_port.readline())
        self.testx += 1
        #self.textbox.config(text = "Test")
        #self.textbox.insert(tk.INSERT, "test")
        root.after(100, self.update)

  
root = tk.Tk()
root.geometry('500x500')
root.title('GUI_APP')


#root.after(1000, Application(master=root).update)
root = Application(master=root)
root.mainloop()