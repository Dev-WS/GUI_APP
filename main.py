import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msb
import serial



#port = serial.tools.list_ports.comports()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.create_combobox()
        self.serial_ports()

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


    def create_combobox(self):

        self.cb_value = tk.StringVar()
        self.combobox = ttk.Combobox(root, textvariable = self.cb_value)

        self.combobox.place(x= 0, y=10)
        self.combobox['values'] = ('A', 'B', 'C')
        self.combobox.current(0) 
        self.combobox.bind("<<ComboboxSelected>>", self.on_select_changed)

    def on_select_changed(self, event):
        msb.showinfo("Info", self.cb_value.get())

    def serial_ports(self):

        self.test = 1

  
root = tk.Tk()
app = Application(master=root)
app.mainloop()