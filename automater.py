from tkinter import Tk, Entry, Label, Button
from win32gui import FindWindow, SetForegroundWindow
from win32com.client import Dispatch
from pyautogui import typewrite, press
from time import sleep
from os.path import exists


def init():
    if(not exists('radio.daemon')):
        statusLbl.configure(text='Status: No data found !', fg='red')
        return open('radio.daemon', 'w').close()
    foo = open('radio.daemon', 'r')
    data = foo.readlines()
    foo.close()
    if(len(data)):
        titleFound = False
        passwordFound = False
        for line in data:
            if('pg=' in line):
                titleFound = True
                title.insert(0, line.split('pg=')[1].split('\n')[0])
                if(not title.get()):
                    titleFound = False
            if('pd=' in line):
                passwordFound = True
                password.insert(0, line.split('pd=')[1].split('\n')[0])
                if(not password.get()):
                    passwordFound = False
        msg = 'Status: '
        if(not titleFound):
            msg += 'program title'
        if(not passwordFound):
            if(not titleFound):
                msg += ' and '
            msg += 'passoword'
        msg += ' not found !'
        if(not titleFound or not passwordFound):
            return statusLbl.configure(text=msg, fg='red')
    else:
        statusLbl.configure(text='Status: No data found !', fg='red')


def save():
    if(not title.get() or not password.get()):
        return statusLbl.configure(text='Status: Title and Password must not be empty !', fg='red')
    foo = open('radio.daemon', 'w')
    foo.write('pg='+title.get()+'\npd='+password.get())
    foo.close()
    statusLbl.configure(text='Status: Data saved !', fg='green')


def unlock():
    try:
        shell = Dispatch("WScript.Shell")
        shell.SendKeys('%')
        hwnd = FindWindow(None, title.get())
        if(not hwnd):
            return statusLbl.configure(text='Status: The program is not running !', fg='red')
        SetForegroundWindow(hwnd)
        sleep(1)
        typewrite(password.get())
        press('enter')
        statusLbl.configure(text='Status: Unlocked !', fg='green')
    except Exception as e:
        statusLbl.configure(text='Status: '+str(e), fg='red')


window = Tk()

titleLbl = Label(window, text='Program Title')
titleLbl.place(x=0, y=0, width=100)

title = Entry()
title.place(x=100, y=0, width=300)

saveBtn = Button(window, text="Save", command=save, width=10, height=4)
saveBtn.place(x=410, y=0)

passwordLbl = Label(window, text='Password')
passwordLbl.place(x=0, y=40, width=100)

password = Entry(show='*')
password.place(x=100, y=40, width=300)

unlockBtn = Button(window, text="Unlock", command=unlock, width=50, height=3)
unlockBtn.place(x=50, y=90)

statusLbl = Label(window, text='Status: OK', font=20, fg='green')
statusLbl.place(x=100, y=170)

init()

window.title('Automater'+(' for '+title.get() if title.get() else ''))
window.geometry("500x200+10+10")
window.resizable(0, 0)


window.mainloop()
