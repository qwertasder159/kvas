from customtkinter import *
from PIL import Image


class Window(CTk):

    def __init__(self):
        super().__init__()

        self.geometry("800x500")
        self.title("menu")
        self.configure(fg_color="#D98023")


        self.left = CTkFrame(self)
        self.left.pack(side="left", padx=100)

        image = Image.open(r"c:\Users\Potap\Desktop\6850919.png")
        img = CTkImage(light_image=image, dark_image=image, size=(350, 350))

        self.lb = CTkLabel(self.left, text="WELCOME", image=img, compound="center")
        self.lb.pack()

        self.right = CTkFrame(self)
        self.right.pack(side="right", padx = 50)

        self.name = CTkEntry(self.right, placeholder_text="Name")
        self.name.pack(padx=20,pady=20)

        self.host = CTkEntry(self.right, placeholder_text="Host")
        self.host.pack(padx=20,pady=20)

        self.port = CTkEntry(self.right, placeholder_text="Port")
        self.port.pack(padx= 20,pady=20)

        self.btn = CTkButton(self.right, text="Start", command=self.start)
        self.btn.pack(padx= 20,pady=20)

        self.result = None

    def start(self):

        name = self.name.get() if self.name.get() else "Anonymous"
        host = self.host.get() if self.host.get() else "localhost"
        port = self.port.get() if self.port.get() else "8080"

        self.result = {
            "name": name,
            "host": host,
            "port": port
        }

        self.after(10, self.destroy)  


def run_menu():

    win = Window()
    win.mainloop()
    return win.result