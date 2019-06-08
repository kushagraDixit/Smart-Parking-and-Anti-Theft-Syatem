from Tkinter import *
from qrtools import QR
import os
import MySQLdb
import string
import random
import tkMessageBox
import pyqrcode


myDB = MySQLdb.connect(host="sql12.freesqldatabase.com",port=3306,user="sql12246690",passwd="pB1RfqMTj9",db="sql12246690")
cHandler = myDB.cursor()
cHandler.execute("SHOW DATABASES")
cHandler.execute("use sql12246690")

def random_generator(size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

class registration:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.resizable(width=False, height=False)
        top.title('Register')
        top.geometry('1280x650') # Size 200, 200
        
        Label(top, text="Name : ", font='Helvetica 20 ').pack()
        self.e1 = Entry(top)
        self.e1.pack(padx=5,ipady=5,ipadx=100)
        Label(top, text="Email : ", font='Helvetica 20 ').pack()
        self.e2 = Entry(top)
        self.e2.pack(padx=5,ipady=5,ipadx=100)
        Label(top, text="Phone : ", font='Helvetica 20 ').pack()
        self.e3 = Entry(top)
        self.e3.pack(padx=5,ipady=5,ipadx=100)
        Label(top, text="Password : ", font='Helvetica 20 ').pack()
        self.e4 = Entry(top)
        self.e4.config(show="*")
        self.e4.pack(padx=5,ipady=5,ipadx=100)
        b = Button(top, text="OK", command=self.ok, font='Helvetica 20 bold', height=1, width=10)
        b.pack(pady=30)
    def ok(self):
        name=self.e1.get()
        email=self.e2.get()
        phone=self.e3.get()
        pwd=self.e4.get()
        idu=random_generator()
        regen=1
        ex=1
        ep=0

        for i in range(len(email)):
            if email[i]=='@':
                ex=0
                break

        for i in range(len(phone)):
           if (not(phone[i].isdigit())):
               ep=1
               break

        print ep
        print ex

        if(ep or ex):
            err = Toplevel()
            err.resizable(width=False,height=False)
            err.title('ERROR!!')
            err.geometry('400x200')
            error = Label(err, text = "Error In Input \n Please Fill The Form Correctly",font='Helvetica 18 bold')
            error.pack(fill="both", expand="yes")
        else:   
            
            while(regen):
                cHandler.execute("SELECT * FROM spatsUsers WHERE idu = '%s'" % (idu))
                res1 = cHandler.fetchall()

                if (res1):
                    regen=1;
                    idu=random_generator()
                else:
                    break

            url = pyqrcode.create('http://uca.edu')
            url.png('qr.png', scale=15)

            cHandler.execute("SELECT * FROM spatsUsers WHERE e_mail = '%s' AND phone_no = '%s'" % (email,phone))
            res2 = cHandler.fetchall()
            if (res2):
                print "details already exist"
            else:
                cHandler.execute("INSERT INTO spatsUsers(name, e_mail, phone_no, password , idu) VALUES(%s,%s,%s,%s,%s)",
                 (name,email,phone,pwd,idu))
                #myDB.commit()
                print "User Registered "
                print idu

        
            a = us_reg(self.top)
            self.top.wait_window(a.ntop)
            self.top.destroy()

class us_reg:
    def __init__(self, parent):
        ntop = self.ntop = Toplevel(parent)
        ntop.resizable(width=False,height=False)
        ntop.geometry('1280x650')
        ntop.title('Registration Successful')
        labelntop1= LabelFrame(ntop)
        labelntop1.pack(fill="both", expand="yes")
        desc = Label(labelntop1, text = "Congrats!! You Have Successfully Signed Up For SPATS! \n Please Take A Picture Of The QR Code That Is Given Below ", font=("Helvetica", 30))
        desc.pack()
        labelntop2= LabelFrame(ntop)
        labelntop2.pack(fill="both", expand="yes")
        widget = Label(labelntop2, compound='top')
        widget.lenna_image_png = PhotoImage(file="qr.png")
        widget['text'] = ""
        widget['image'] = widget.lenna_image_png
        widget.pack()

        btn= Button(ntop, text="OK", command=self.close, font='Helvetica 20 bold', height=1, width=10)
        btn.pack()

    def close(self):
        self.ntop.destroy() 
    

            
class signin:
    def __init__(self, parent):
        ltop = self.ltop = Toplevel(parent)
        ltop.resizable(width=False, height=False)
        ltop.title('Register')
        ltop.geometry('1280x650') # Size 200, 200
        Label(top, text="Value").pack()
        self.e1 = Entry(ltop)
        self.e1.pack(padx=5)
        btn1 = Button(top, text="OK", command=self.ok)
        btn1.pack(pady=5)
    def ok(self):
        print "value is", self.e.get()
        self.top.destroy()


def register():
    d = registration(win)
    win.wait_window(d.top)

def login():
    b = signin(win)
    win.wait_window(a.ltop)

    


win = Tk()
win.resizable(width=False, height=False)

win.title('Smart Parking and Anti Theft System')
win.geometry('1280x650') # Size 200, 200
heading=Label(win, text="Welcome To Smart Parking and Anti-Theft System", pady=25, font='Helvetica 18 bold')
heading.pack()

labelframe1 = LabelFrame(win)
labelframe1.pack(fill="both", expand="yes")
 
left = Label(labelframe1)
left.pack()

button1 = Button(labelframe1, text="PARK MY CAR", height=3, width=50, fg="red", font='Helvetica 15 bold',)
button1.pack()

labelframe2 = LabelFrame(win)
labelframe2.pack(fill="both", expand="yes")
 
button2 = Button(labelframe2, text="RECOVER QR CODE", height=3, width=50, fg="red", font='Helvetica 15 bold', command=login)
button2.pack()

labelframe3 = LabelFrame(win)
labelframe3.pack(fill="both", expand="yes")
 
button3 = Button(labelframe3, text="REGISTER FOR SPATS", height=3, width=50, fg="red", font='Helvetica 15 bold', command= register)
button3.pack()

labelframe4 = LabelFrame(win)
labelframe4.pack(fill="both", expand="yes")
 
button4 = Button(labelframe4, text="ABOUT SPATS", height=3, width=50, fg="red", font='Helvetica 15 bold')
button4.pack()









win.mainloop()

