from tkinter import *
from tkinter import filedialog as fd
import os
import logging
cur_dir= os.getcwd()
folder_dataset = cur_dir+ '/dataset/'
from tkinter import messagebox

from bot import Bot
class MyWindow:
    def __init__(self, win):

        self.file_input = cur_dir+ '/dataset/input.txt'
        self.folder_output = cur_dir+ '/dataset/'+ 'output/'

        self.lb_note = Label(win, text='NOTE:  OUTPUT FOLDER!', bg="white", fg="red", font=("Arial", 11))

        self.lb_file_input= Label(win, text='Folder Dataset (default: ' + self.file_input + ')', bg="black", fg="white",
                          font=("Arial", 10))
        self.lb_text_file_input= Label(win, text='Dataset: (default: ' + self.file_input + ')', font=("Arial", 10))
        self.bt_file_input = Button(text='Select input.txt', bg="gray", fg="blue", command=self.callback_file_input)

        self.lb_folder_output = Label(win, text='Folder output (default: ' + self.folder_output + ')', bg="black", fg="white",font=("Arial", 10))
        self.lb_text_folder_output= Label(win, text='Output: (default: ' + self.folder_output + ')', font=("Arial", 10))

        self.bt_folder_output = Button(text='Select folder output', bg="gray", fg="blue",
                                        command=self.callback_folder_output)
        self.lb_note.place(x=0, y=10)
        self.lb_file_input.place(x=100, y=50)
        self.bt_file_input.place(x=800, y=50)
        self.lb_text_file_input.place(x=130, y=80)
        self.lb_folder_output.place(x=100, y=120)
        self.bt_folder_output.place(x=800, y=120)
        self.lb_text_folder_output.place(x=130, y=150)

        self.user_login='123023951000'
        self.password_login='iejuc6'
        self.number_thread=1
        self.link_login='https://system.reins.jp/login/main/KG/GKG001200'
        self.link_search='https://system.reins.jp/main/BK/GBK001200'

        self.lb_user_login = Label(win, text='user login: ')
        self.et_user_login = Entry(win, bd=2, foreground="red")
        self.lb_password_login = Label(win, text='password : ')
        self.et_password_login = Entry(win, bd=2, foreground="red")
        self.lb_number_thread = Label(win, text='number threads: ')
        self.et_number_thread = Entry(win, bd=2, foreground="red")
        self.lb_link_login = Label(win, text='link login: ')
        self.et_link_login = Entry(win, bd=2, foreground="red")
        self.lb_link_search = Label(win, text='link search: ')
        self.et_link_search = Entry(win, bd=2, foreground="red")
        self.et_user_login.insert(END, str(self.user_login))
        self.et_password_login.insert(END, str(self.password_login))

        self.et_number_thread.insert(END, str(self.number_thread))
        self.et_link_login.insert(END, str(self.link_login))
        self.et_link_search.insert(END, str(self.link_search))




        self.lb_user_login.place(x=130, y=190)
        self.et_user_login.place(x=305, y=190)
        self.lb_password_login.place(x=480, y=190)
        self.et_password_login.place(x=655, y=190)

        self.lb_number_thread.place(x=130, y=230)
        self.et_number_thread.place(x=305, y=230)
        self.lb_link_login.place(x=480, y=230)
        self.et_link_login.place(x=655, y=230)
        self.lb_link_search.place(x=480, y=270)
        self.et_link_search.place(x=655, y=270)
        self.b1 = Button(win, text='LOGIN', bg="green", fg="white", command=self.login)
        self.b2 = Button(win, text='RUN', bg="red", fg="white", command=self.run)
        self.b1.place(x=370, y=310)
        self.b2.place(x=440, y=310)
        self.list_bot=[]
        self.bot=None

    def login(self):
        if not os.path.exists(self.folder_output):
            os.makedirs(self.folder_output)
        self.user_login=str(self.et_user_login.get())
        self.password_login = str(self.et_password_login.get())
        self.link_login = str(self.et_link_login.get())
        self.link_search = str(self.et_link_search.get())

        if self.bot is None:
            self.bot = Bot(username=self.user_login, password=self.password_login, link_login=self.link_login,
                      link_search=self.link_search,output_folder=self.folder_output)
            self.list_bot.append(self.bot)

        self.bot.login()


    def run(self):
        try:
            if not os.path.exists(self.folder_output):
                os.makedirs(self.folder_output)
            if self.bot is None:
                self.user_login = str(self.et_user_login.get())
                self.password_login = str(self.et_password_login.get())
                self.link_login = str(self.et_link_login.get())
                self.link_search = str(self.et_link_search.get())
                self.bot = Bot(username=self.user_login, password=self.password_login, link_login=self.link_login,
                               link_search=self.link_search,output_folder=self.folder_output)
                self.list_bot.append(self.bot)

            if self.bot.check_login() is False:
                messagebox.showerror(title="ERROR", message="PLEASE LOGIN BEFORE RUN!")
            else:
                txt_file = open(self.file_input, encoding="utf8")
                Lines = txt_file.readlines()
                for line in Lines:
                    search_text = line.replace("\n","")
                    if not os.path.exists(self.folder_output+'/'+search_text):
                        os.makedirs(self.folder_output+'/'+search_text)
                    self.bot.run_to_page_file(search_text)
                messagebox.showinfo(title="DONE", message="DONE ALL!")

        except Exception as e:
            logging.debug(str(e))
            logging.debug("ERROR run_in_thread")

    # def run(self):
    #     executor = ThreadPoolExecutor(1)
    #     executor.submit(self.run_in_thread())

    def callback_file_input(self):
        try:
            self.file_input = fd.askopenfilename(filetypes=[("TXT files", "*.txt")])
            self.lb_text_file_input.configure(text=str('Dataset: ' + self.file_input ))
        except Exception as e:
            logging.debug(str(e))
            logging.debug("ERROR callback_folder_dataset")

    def callback_folder_output(self):
        try:
            self.folder_output = fd.askdirectory()
            self.lb_text_folder_output.configure(text=str('Output: ' + self.folder_output ))
        except Exception as e:
            logging.debug(str(e))
            logging.debug("ERROR callback_folder_output")


window = Tk()

mywin = MyWindow(window)

window.title('CONVERT IMAGE TO VIDEO')
window.geometry("1300x600+10+10")
window.mainloop()
