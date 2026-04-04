from customtkinter import *
from menu import run_menu
from socket import *
import threading

setting = run_menu()


class Window(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x500")
        self.title("chat")
        self.configure(fg_color="#5F63E4")

        self.msgbox = CTkTextbox(
            self,
            width=500,
            height=400,
            font=("Arial", 20, "bold"),
            fg_color="#E8DB38",
            text_color ="#9722B5",
            state="disabled",
            border_color="#37CC7A",
            border_width=5
        )
        self.msgbox.pack(pady=10)

        self.text = CTkEntry(self, height=40, width=350)
        self.text.place(x=20, y=430)

        self.btn = CTkButton(self, text="Надіслати", width=100, height=40, command=self.send_msg)
        self.btn.place(x=380, y=430)

        self.nickname = "Anonymous" if not setting["name"] else setting["name"]

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((setting["host"], int(setting["port"])))

            hello = f"TEXT@{self.nickname}@[SYSTEM] {self.nickname} приєднався до чату!\n"
            self.sock.send(hello.encode("utf-8"))

            threading.Thread(target=self.rec_msg, daemon=True).start()

        except Exception as e:
            self.add_msg(f"Не вдалося підключитися: {e}")

    def add_msg(self, text):
        self.msgbox.configure(state="normal")
        self.msgbox.insert(END, text + "\n")
        self.msgbox.configure(state="disabled")
        self.msgbox.see(END)

    def send_msg(self):
        msg_text = self.text.get()
        
        if msg_text:
            try:
                msg = f"TEXT@{self.nickname}@{msg_text}\n"
                self.sock.send(msg.encode("utf-8"))
                self.text.delete(0, END)
            except:
                pass

    def rec_msg(self):
        buffer = ""

        while True:
            try:
                chunk = self.sock.recv(4096).decode("utf-8")

                if not chunk:
                    break

                buffer += chunk

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_line(line.strip())

            except:
                break

        self.sock.close()

    def handle_line(self, line):

        if not line:
            return

        parts = line.split("@", 3)
        msg_type = parts[0]

        if msg_type == "TEXT":

            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]

                self.add_msg(f"{author}: {message}")

        else:
            self.add_msg(line)


win = Window()
win.mainloop()