import  threading
from socket import *
from customtkinter import *


class MainWindow(CTk):
   def __init__(self):
       super().__init__()
 #      self.set_window_scaling(1.2)
       self.geometry('600x500')
       self.label = ""
       self.minsize(600, 500)
       self.frame = CTkFrame(self, width=200, height=500)
       self.frame.pack_propagate(False)
       self.frame.configure(width=0)
       self.frame.grid(rowspan=1, column=0,   sticky='nw')
       self.is_show_menu = False
       self.speed_animate_menu = -1.2
       self.frame_width = 0
       self.grid_rowconfigure(0, weight=1)
       self.grid_rowconfigure(1, weight=1)
       self.grid_rowconfigure(2, weight=1)
       self.grid_columnconfigure(0, weight=0)
       self.grid_columnconfigure(1, weight=1)

       self.label = CTkLabel(self.frame, text="Ваш нікнейм")
       self.label.grid(row=0, column=0, padx=90, pady=10, sticky="nw")



       self.label_theme = CTkOptionMenu(self.frame, values=['Темна', 'Світла'], command=self.change_theme)
       self.label_theme.grid(row=0, column=0, padx=60, pady=30, sticky="w")
       self.theme = None


       self.chat_text = CTkTextbox(self, state='disable'  )
       self.chat_text.grid(row=0, column=1, ipadx=200, ipady=30, sticky="news")


       self.message_input = CTkEntry(self, placeholder_text='Введіть повідомлення:')
       self.message_input.grid(row=2, column=1, padx=(0, 40), pady=0, sticky="sew")


       self.send_button = CTkButton(self, text='▶️', width=30, height=30)
       self.send_button.grid(row=2, column=1, padx=0, pady=0, sticky="se")
       self.username = 'User'
       try:
           self.sock = socket(AF_INET, SOCK_STREAM)
           self.sock.connect(('LogikaTalk213', 8080))
           hello = f"TEXT@{self.username}@[SYSTEM] {self.username} приєднався(лась) до чату!\n"
           self.sock.send(hello.encode('utf-8'))
           threading.Thread(target=self.recv_message, daemon=True).start()
       except Exception as e:
           self.add_message(f"Не вдалося підключитися до сервера: {e}")

           self.label = CTkLabel(self.frame, text='Імʼя')
           self.label.grid(row=0, column=0, padx=80, pady=90, sticky="w")
           self.entry = CTkEntry(self.frame)
           self.entry.grid(row=0, column=0, padx=60, pady=50, sticky="w")

   def show_menu(self):
       self.frame.configure(width=self.frame.winfo_width() * self.speed_animate_menu)
       if not self.frame.winfo_width() >= 200 and self.is_show_menu:
           self.after(10, self.show_menu)
       elif self.frame.winfo_width() >= 40 and not self.is_show_menu:

           if self.label and self.entry:
               self.label.destroy()
               self.entry.destroy()

   def change_theme(self, value):
       if value == 'Темна':
           set_appearance_mode('dark')
       else:
           set_appearance_mode('light')

   def add_message(self, text):  # функція яка показу повідомлення від користувача на екран
       self.chat_text.configure(state='normal')
       self.chat_text.insert(END, 'Я: ' + text + '\n')
       self.chat_text.configure(state='disable')

   def send_message(self):  # функція яка считує те що написав користувач і намагається це показати на екрані
       message = self.message_entry.get()
       if message:
           self.add_message(f"{self.username}: {message}")
           data = f"TEXT@{self.username}@{message}\n"
           try:
               self.sock.sendall(data.encode())
           except:
               pass
       self.message_entry.delete(0, END)

   def recv_message(self):
       buffer = ""
       while True:
           try:
               chunk = self.sock.recv(4096)
               if not chunk:
                   break
               buffer += chunk.decode()

               while "\n" in buffer:
                   line, buffer = buffer.split("\n", 1)
                   self.handle_line(line.strip())
           except:
               break
       self.sock.close()

win = MainWindow()
win.mainloop()























