from Tkinter import *
from qrtools import QR
import os
import MySQLdb
import string
import random
import tkMessageBox
import pyqrcode
import picamera
import RPi.GPIO as GPIO
import time
from threading import Thread
from multiprocessing import Process
from collections import Counter
import thread
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import urllib
import webbrowser
import PIL


global concur
global curr_usr
curr_usr=""

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False) # for disable warnings in terminal

# time for sensor to settle
SENSOR_SETTLE_TIME = 0.00001

buzzer=21
GPIO.setup(buzzer, GPIO.OUT)

MEASURE_INTERVAL_TIME = 0.015 # time delay to measure (min 15miliseconds)                 

# max distance threshold for sensors to react (in cm)
MAX_DISTANCE_THRESHOLD = 5.0

# Speed of sound at sea level = 343 m/s or 34300 cm/s
MEASURE_REFERENCE = 17150

# list of sensors
sensors = []

# sensor1 with pin configuration
sensor1 = {'ID': 'sensor1', 'TRIG': 5, 'ECHO': 6 }
sensors.append(sensor1) # add to the list
# sensor2 with pin configuration
sensor2 = {'ID': 'sensor2', 'TRIG': 23, 'ECHO': 24 }
sensors.append(sensor2) # add to the list




myDB = MySQLdb.connect(host="sql12.freesqldatabase.com",port=3306,user="sql12247841",passwd="zx7wwysf1f",db="sql12247841")
cHandler = myDB.cursor()
cHandler.execute("SHOW DATABASES")
cHandler.execute("use sql12247841")


#camera = picamera.PiCamera()
#camera.resolution = (800, 600)

def random_generator(size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))

class Concur(threading.Thread):
    def __init__(self, usr):
        threading.Thread.__init__(self)
        self.usr=usr
        print usr
        
        self.iterations = 0
        self.daemon = True  # OK for main to exit even if instance is still running
        self.paused = True  # start out paused
        self.state = threading.Condition()

    def run(self):
        self.resume() # unpause self
        main()

        sen1 =[]
        sen2= []

        i=0

        for y in range(40):
            measure(sensors[i])
            if i==0:
                sen1.append(measure(sensors[i]))
                i=1
            else:
                sen2.append(measure(sensors[i]))
                i=0
        
        print sen1
        print sen2

        data1 = Counter(sen1)
        print data1.most_common()# Returns all unique items and their counts
        avg_sen1 = data1.most_common(1)[0][0]

        data2 = Counter(sen2)
        print data2.most_common()# Returns all unique items and their counts
        avg_sen2 = data2.most_common(1)[0][0]

        print avg_sen1
        print avg_sen2

        dsen1=0
        dsen2=0
        car_theft=0
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()
    
            cval1=measure(sensors[0])
            cval2=measure(sensors[1])

            change1 = abs(avg_sen1-cval1)
            change2 = abs(avg_sen2-cval2)
            print change1
            print change2
    
            if change1<20:
                dsen1=0
            else:
                dsen1+=1

            if change2<20:
                dsen2=0
            else:
                dsen2+=1

            print dsen1
            print dsen2

            if dsen1>5 or dsen2>5:
                print "CAR THEFT!!!!!!"
                car_theft += 1
                print car_theft
            else:
                car_theft = 0

            if car_theft==2:
                print "sending mail"
                
                k = alert_user(self.usr)
                GPIO.output(buzzer, False)


            if car_theft>0:
                theft()
            else:
                not_theft()
            self.iterations += 1



    def resume(self):
        print "resume"
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        print "Paused"
        with self.state:
            self.paused = True  # make self block and wait

    def stop(self):
        print "Stopped"
        with self.state:
            self.stoped= True
            

class registration:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.resizable(width=False, height=False)
        top.title('Register')
        top.geometry('800x450') # Size 200, 200
        desc = Label(top, text = "Please Enter Your Details to SignUP for SPATS ", font=("Helvetica", 20))
        desc.pack(ipady=30)
        Label(top, text="Name : ", font='Helvetica 10 ').pack()
        self.e1 = Entry(top)
        self.e1.pack(padx=5,ipady=5,ipadx=60)
        Label(top, text="Email : ", font='Helvetica 10 ').pack()
        self.e2 = Entry(top)
        self.e2.pack(padx=5,ipady=5,ipadx=60)
        Label(top, text="Phone : ", font='Helvetica 10 ').pack()
        self.e3 = Entry(top)
        self.e3.pack(padx=5,ipady=5,ipadx=60)
        Label(top, text="Password : ", font='Helvetica 10 ').pack()
        self.e4 = Entry(top)
        self.e4.config(show="*")
        self.e4.pack(padx=5,ipady=5,ipadx=60)
        b = Button(top, text="OK", command=self.ok, font='Helvetica 10 bold', height=1, width=30)
        b.pack(pady=20)
    def ok(self):
        name=self.e1.get()
        email=self.e2.get()
        phone=self.e3.get()
        pwd=self.e4.get()
        idu=random_generator()
        regen=1
        ex=1
        ep=0
        es=0

        for i in range(len(email)):
            if email[i]=='@':
                ex=0
                break

        for i in range(len(phone)):
           if (not(phone[i].isdigit())):
               ep=1
               break

        if (phone=="" or pwd=="" or email=="" or name==""):
            es=1
        print ep
        print ex
        print es

        if(ep or ex or es):
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

            url = pyqrcode.create(idu)
            url.png('qr.png', scale=8)

            cHandler.execute("SELECT * FROM spatsUsers WHERE e_mail = '%s' OR phone_no = '%s'" % (email,phone))
            res2 = cHandler.fetchall()
            if (res2):
                print "details already exist"
                err = Toplevel()
                err.resizable(width=False,height=False)
                err.title('ERROR!!')
                err.geometry('550x200')
                error = Label(err, text = "Your E-mail or Phone is ALready Registered \n Please Click on Recover QR code \n Or Enter Details Correctly ",font='Helvetica 18 bold')
                error.pack(fill="both", expand="yes")
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
        ntop.geometry('800x450')
        ntop.title('Registration Successful')
        labelntop1= LabelFrame(ntop)
        labelntop1.pack(fill="both", expand="yes")
        desc = Label(labelntop1, text = "Congrats!! You Have Successfully Signed Up For SPATS! \n Please Take A Picture Of The QR Code That Is Given Below ", font=("Helvetica", 20))
        desc.pack()
        labelntop2= LabelFrame(ntop)
        labelntop2.pack(fill="both", expand="yes")
        widget = Label(labelntop2, compound='top')
        widget.lenna_image_png = PhotoImage(file="qr.png")
        widget['text'] = ""
        widget['image'] = widget.lenna_image_png
        widget.pack()

        btn= Button(ntop, text="OK", command=self.close, font='Helvetica 10 bold', height=1, width=10)
        btn.pack()

    def close(self):
        self.ntop.destroy() 
    

            
class signin:
    def __init__(self, parent):
        ltop = self.ltop = Toplevel(parent)
        ltop.resizable(width=False, height=False)
        ltop.title('Register')
        ltop.geometry('800x450') # Size 200, 200
        desc = Label(ltop, text = "Please Enter Your Registered Email And Password ", font=("Helvetica", 30))
        desc.pack(ipady=100)
        Label(ltop, text="Email : ", font='Helvetica 20 ').pack()
        self.e1 = Entry(ltop)
        self.e1.pack(padx=5,ipady=5,ipadx=100)
        Label(ltop, text="Password : ", font='Helvetica 20 ').pack()
        self.e2 = Entry(ltop)
        self.e2.config(show="*")
        self.e2.pack(padx=5,ipady=5,ipadx=100)
        btn1 = Button(ltop, text="OK", command=self.ok, font='Helvetica 20 bold', height=1, width=30)
        btn1.pack(pady=40)
    def ok(self):
        email=self.e1.get()
        pwd=self.e2.get()
        ex=True
        ep=False

        for i in range(len(email)):
            if email[i]=='@':
                ex=False
                break
        if pwd=="":
            ep=False

        print ex
        print ep

        if (ep or ex):
            err = Toplevel()
            err.resizable(width=False,height=False)
            err.title('ERROR!!')
            err.geometry('500x300')
            error = Label(err, text = "Email or Password entered is wrong \n Please Enter Valid Email Or Password \n Or Please Register",font='Helvetica 18 bold')
            error.pack(fill="both", expand="yes")
        else:
            cHandler.execute("SELECT * FROM spatsUsers WHERE e_mail = '%s' and password = '%s'" % (email,pwd))
            res1 = cHandler.fetchall()
            print res1
            if(res1):
                idu= res1[0][4]
                name=res1[0][1]
                url = pyqrcode.create(idu)
                url.png('rec.png', scale=15)
                d = us_lg(self.ltop, idu)
                self.ltop.wait_window(d.lgtop)
                self.ltop.destroy()
                
                
            else:
                err = Toplevel()
                err.resizable(width=False,height=False)
                err.title('ERROR!!')
                err.geometry('400x200')
                error = Label(err, text = "Email is Not Registered",font='Helvetica 18 bold')
                error.pack(fill="both", expand="yes")

        

class us_lg:
    def __init__(self, parent, usr):
        lgtop = self.lgtop = Toplevel(parent)
        lgtop.resizable(width=False,height=False)
        lgtop.geometry('800x450')
        lgtop.title(' Registration Successful')
        labellgtop1= LabelFrame(lgtop)
        labellgtop1.pack(fill="both", expand="yes")
        res4 = cHandler.execute("SELECT * FROM spatsUsers WHERE idu = '%s' LIMIT 1" % (usr))
        res4 = cHandler.fetchall()
        print res4
        name=res4[0][0]
        msg = "WELCOME !! "+name+ "\n Your QR code for Parking is Given Below \n Please take a Picture for Future Refrernce"
        desc = Label(labellgtop1, text = msg, font=("Helvetica", 30))
        desc.pack()
        labellgtop2= LabelFrame(lgtop)
        labellgtop2.pack(fill="both", expand="yes")
        widget = Label(labellgtop2, compound='top')
        widget.lenna_image_png = PhotoImage(file="rec.png")
        widget['text'] = ""
        widget['image'] = widget.lenna_image_png
        widget.pack()

        btn= Button(lgtop, text="OK", command=self.close, font='Helvetica 20 bold', height=1, width=10)
        btn.pack()

    def close(self):
        self.lgtop.destroy()

class system:
    def __init__(self, parent):

        sytop = self.sytop = Toplevel(parent)
        sytop.resizable(width=False, height=False)
        sytop.title('SPATS')
        sytop.geometry('800x450') # Size 200, 200
        
        
        self.idu = camera_decode()
        self.concur = Concur(self.idu)
        print self.idu
        if not(self.idu==""):
            curr_usr=self.idu
            print curr_usr
            print self.idu
            res2 = cHandler.execute("SELECT * FROM spatsUsers WHERE idu = '%s' LIMIT 1" % (self.idu))
            res2 = cHandler.fetchall()
            print res2
            if(res2): 
                name = res2[0][0]
                print name
                msg = "WELCOME!! " + name + "\nYour Vehicle is Now Safely Parked With Us \nYou will be alerted via your email and phone if there is a theft detected"
                labelsytop1 = Label(sytop, text= msg, font='Helvetica 30')
                labelsytop1.pack(ipady=30)
                self.btnsytop=Button(sytop, text="Park", command=self.do, font='Helvetica 20 bold', height=1, width=10)
                self.btnsytop.pack(pady=30)
                

                

                
            else:
                msg="Could't match user with the QR code \n Please Show Correct QR Code!!"
                labelsytop1 = Label(sytop, text= msg, font='Helvetica 25')
                labelsytop1.pack()
                btnsytop=Button(sytop, text="Close", command=self.cl, font='Helvetica 18 ')
                btnsytop.pack()
        else:
            self.sytop.destroy()
            err = Toplevel()
            err.resizable(width=False,height=False)
            err.title('ERROR!!')
            err.geometry('400x200')
            error = Label(err, text = "Could not Detect The QR code!! \nPlease Try Again!! ",font='Helvetica 18 bold')
            error.pack(fill="both", expand="yes")
            btn1= Button(err, text="Close", font='Helvetica 18', command = err.destroy)
            btn1.pack()
            
    def cl(self):
        self.sytop.destroy()
        


    def ok(self):
        self.wait()
        del(self.concur)
        self.sytop.destroy()

    def do(self):
        self.btnsytop.forget()
        self.btnsytop1=Button(self.sytop, text="Chekout", command=self.cout, font='Helvetica 20 bold', height=1, width=10)
        self.btnsytop1.pack(pady=30)
                
        self.concur.start()

    def wait(self):
        self.concur.pause()

    def restart(self):
        self.concur.resume()

    def stop(self):
        self.concur.stop()

    def cout(self):
        coidu = camera_decode()
        print coidu
        if (not(coidu=="")):
            if (coidu==self.idu):
                self.wait()
                del(self.concur)
                self.sytop.destroy()
                self.sytop.destroy()
                curr_usr=""
                #tkMessageBox.showinfo("Thankyou For Using Our Services !! ")
                err = Toplevel(win)
                err.resizable(width=False,height=False)
                err.title('ThankYou')
                err.geometry('500x300')
                error = Label(err, text = "Thankyou For Using Our Services !! ",font='Helvetica 18 bold')
                error.pack(fill="both", expand="yes")
                btn1= Button(err, text="Close", font='Helvetica 18', command = err.destroy)
                btn1.pack()
            else:
                self.wait()
                err = Toplevel(win)
                err.resizable(width=False,height=False)
                err.title('ThankYou')
                err.geometry('400x200')
                error = Label(err, text = "Please Show Correct QR Code ",font='Helvetica 18 bold')
                error.pack(fill="both", expand="yes")
                btn1= Button(err, text="Close", font='Helvetica 18', command = err.destroy)
                btn1.pack()
                self.restart()
            
        else:
            self.sytop.destroy(win)
            err = Toplevel()
            err.resizable(width=False,height=False)
            err.title('ERROR!!')
            err.geometry('400x200')
            error = Label(err, text = "Could not Detect The QR code!! \nPlease Try Again!! ",font='Helvetica 18 bold')
            error.pack(fill="both", expand="yes")
            btn1= Button(err, text="Close", font='Helvetica 18', command = err.destroy)
            btn1.pack()
            
        






def initPins():
    if len(sensors) > 0:
        for sensor in sensors:
            #Sensor's echo pins shoud be in
            GPIO.setup( sensor['ECHO'], GPIO.IN );

            #Sensor's trig pins should be out
            GPIO.setup( sensor['TRIG'], GPIO.OUT );

        

def measure(sensor):
    print "Measurement started for " + sensor['ID'] + ", Ctrl+z to cancle the measurement";

    GPIO.output( sensor['TRIG'], GPIO.LOW);

    time.sleep(MEASURE_INTERVAL_TIME); #DELAY

    GPIO.output(sensor['TRIG'], GPIO.HIGH);

    time.sleep(SENSOR_SETTLE_TIME);

    GPIO.output(sensor['TRIG'], GPIO.LOW);

    while GPIO.input(sensor['ECHO']) == 0:
        pulse_start = time.time();

    while GPIO.input(sensor['ECHO']) == 1:
         pulse_end = time.time();

    pulse_duration = pulse_end - pulse_start;

    distance = pulse_duration * MEASURE_REFERENCE;
    distanceRound = round(distance, 2);

    print "Distance of sensor "+ sensor['ID'] + " : ", distanceRound, "cm";
    return int(distance)

def main():
    initPins()

def theft():
    GPIO.output(buzzer, True)

def not_theft():
    GPIO.output(buzzer, False)

def alert_user(curr_usr):
    print curr_usr
    if(not(curr_usr=="")):
        ####Photo
        camera = picamera.PiCamera()

        camera.start_preview()
        camera.vflip = False
        camera.hflip = False
        camera.brightness = 60
        camera.capture('thief.png')
        time.sleep(1)
        camera.stop_preview()
        camera.close()
        
        
        ####Mail
        res3 = cHandler.execute("SELECT * FROM spatsUsers WHERE idu = '%s' LIMIT 1" % (curr_usr))
        res3 = cHandler.fetchall()
        mail=res3[0][1]
        ph=res3[0][2]
        email_user = 'spatsuser@gmail.com'
        email_password = 'thisisspats'
        email_send = mail

        subject = 'THEFT ALERT!!!'

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = 'A Theft has been observed from our system. Please see the Photo attched below'
        msg.attach(MIMEText(body,'plain'))

        filename='thief.png'
        attachment  =open(filename,'rb')

        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= "+filename)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email_user,email_password)


        server.sendmail(email_user,email_send,text)
        server.quit()

        print "E-mail successfully sent"

        #####SMS

        mobile_no=9289635554
        password='01shri1100'
        message='Dear SPATS user \nA Theft has been observed by Our System Please view the Picture attched with the mail to be assured!! '
        destination_no=ph
        api_key='ashriu7vRCdAHb0s1mfX'


        urllib.urlopen('https://smsapi.engineeringtgr.com/send/?Mobile='+str(mobile_no)+'&Password='+(password)+'&Message='+message+'&To='+str(destination_no)+'&Key='+api_key)
        print 'Mesage sent'
        return 'Mesage sent'
    else:
        print "No Logged in user Found"
        return "No Logged in user Found"



            

def register():
    d = registration(win)
    win.wait_window(d.top)

def login():
    b = signin(win)
    win.wait_window(b.ltop)

def start_system():
    tkMessageBox.showinfo("Welcome to SPATS", "Please Show Your QR code Identity to The camera")
    e = system(win)
    win.wait_window(e.sytop)
    
def camera_decode():
    camera = picamera.PiCamera()
    camera.resolution = (800, 600)
    try:
        count = 0
        camera.start_preview()
        camera.brightness = 60
        while True :
            camera.capture('pic.png')
            count+=1
            print count
            myCode = QR(filename="pic.png")
            if myCode.decode():
                print "Decoder working"
                user = str(myCode.data)
                camera.stop_preview()
                camera.close()
                return user
                break;
            else:
                user = ""
                os.remove("pic.png")
                #camera = picamera.PiCamera()

            time.sleep(1)
        
            if count>10:
                print "Could not detect QR code"
                user=""
                camera.stop_preview() 
                break;
       
        
    except:
        user=""
        print "error"
        camera.close()


    return user

def about():
    webbrowser.open_new("http://spats.000webhostapp.com/")

def gone():
    win.destroy()
    

#concur = Concur()

win = Tk()
win.resizable(width=False, height=False)
#win.overrideredirect(True)
win.title('Smart Parking and Anti Theft System')
win.geometry('800x450') # Size 200, 200
heading=Label(win, text="Welcome To Smart Parking and Anti-Theft System", pady=15, font='Helvetica 18 bold')
heading.pack()

labelframe1 = LabelFrame(win)
labelframe1.pack(fill="both", expand="yes")
 
left = Label(labelframe1)
left.pack()

button1 = Button(labelframe1, text="PARK MY CAR", height=2, width=20, fg="red", font='Helvetica 15 bold', command = start_system)
button1.pack(side=LEFT)
wid1 = Label(labelframe1, compound='top', height=125, width=125)
img1=PhotoImage(file="parking.png")
wid1.config(image=img1)
wid1.pack(side=LEFT,padx=5,pady=0)

labelframe2 = LabelFrame(win)
labelframe2.pack(fill="both", expand="yes")
 
button2 = Button(labelframe2, text="RECOVER QR CODE", height=2, width=20, fg="red", font='Helvetica 15 bold', command=login)
button2.pack(side=LEFT)
wid2 = Label(labelframe2, compound='top', height=125, width=125)
img2=PhotoImage(file="recovery.png")
wid2.config(image=img2)
wid2.pack(side=LEFT,padx=5)

 
button3 = Button(labelframe1, text="REGISTER FOR SPATS", height=2, width=20, fg="red", font='Helvetica 15 bold', command= register)
button3.pack(side=RIGHT)
wid3 = Label(labelframe1, compound='top', height=125, width=125)
img3=PhotoImage(file="new_user.png")
wid3.config(image=img3)
wid3.pack(side=RIGHT,padx=5)

 
button4 = Button(labelframe2, text="ABOUT SPATS", height=2, width=20, fg="red", font='Helvetica 15 bold', command=about)
button4.pack(side=RIGHT)
wid4 = Label(labelframe2, compound='top', height=125, width=125)
img4=PhotoImage(file="info.png")
wid4.config(image=img4)
wid4.pack(side=RIGHT,padx=5)

labelframe3 = LabelFrame(win)
labelframe3.pack(fill="both", expand="yes")
button5 = Button(labelframe3, text="EXIT", height=1, width=10, fg="red", font='Helvetica 15 bold', command=gone)
button5.pack()

win.mainloop()
