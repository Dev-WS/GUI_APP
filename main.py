from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.start_button()

    def create_widgets(self):
        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")
        self.quit = Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

    def start_button(self):
        self.button_start = Button(self)
        self.button_start["text"] = "Start Button"
        self.button_start ["command"] = self.clicked_start
        self.button_start.pack(side = "top")


    def clicked_start(self):
        print("Clicked Start Button")




root = Tk()
app = Application(master=root)
app.mainloop()