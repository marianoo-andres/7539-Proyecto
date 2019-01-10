from tkinter import *
import queue
import datetime
import time
import threading
from Enroller import Enroller
import os
import json
from PIL import ImageTk, Image
from AudioPlayer import AudioPlayer
from Person import Person
class TakePictureThread(threading.Thread):
    def __init__(self, enroller, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.enroller = enroller
    def run(self):
        print("Detectando rostro...")
        faceDetected = self.enroller.setFace()
        if faceDetected:
            event = "DeteccionTerminada"
        else:
            event = "DeteccionTiempoAgotado"
        self.queue.put([event])

class ReadDniThread(threading.Thread):
    def __init__(self, enroller, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.enroller = enroller
    def run(self):
        print("Esperando DNI...")
        fileName = "data.txt"
        startTime = time.time()
        maxWaitInSeconds = 30
        while fileName not in os.listdir("Temp"):
            waitTime = time.time() - startTime
            if waitTime > maxWaitInSeconds:
                # Se agotó el tiempo de espera de colocación del DNI
                event = "LecturaDNIEsperaAgotada"
                self.queue.put([event])
                return
            time.sleep(1)
        with open(os.path.join("Temp",fileName)) as f:
            data = f.read().replace("\n", "")
            print(data)
            person = Person(dataString=data)

        os.remove(os.path.join("Temp",fileName))

        if not person.valid:
            event = "LecturaDNIQrInvalido"
        else:
            self.enroller.enroll(data)
            event = "LecturaDNITerminada"
        self.queue.put([event, person])

class App:
    def __init__(self):
        #Tkinter
        self.root = Tk()

        self.initWindow()

        self.queue = queue.Queue()
        self.enroller = Enroller()

        self.audioPlayer = AudioPlayer()
        self.audioPlayer.playEnrollWelcome()
        
        #Blocked from here
        self.root.mainloop()



    def onEvent(self):
        try:
            event = self.queue.get(0)
            self.processEvent(event)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.onEvent)

    def processEvent(self, eventList):
        eventString = eventList[0]
        if eventString == "DeteccionTerminada":
            self.labelMessage.set("Por favor coloque el código QR\ndel DNI en el lector")
            self.audioPlayer.playReadDNI()
            self.readDNI()
        elif eventString == "LecturaDNITerminada":
            person = eventList[1]
            self.labelMessage.set("El enrolamiento ha sido exisitoso!\n\n{}\n{}\n{}\n{}".format(
                person.name + " " + person.surname, person.dni, person.sex, person.birthDate
            ))
            self.audioPlayer.playEnrollSuccess()
            self.root.after(10000, self.restart)
        elif eventString == "LecturaDNIEsperaAgotada":
            self.labelMessage.set("Tiempo de espera agotado")
            self.audioPlayer.playReadDNIWaitTimeExausted()
            self.root.after(10000, self.restart)
        elif eventString == "DeteccionTiempoAgotado":
            self.labelMessage.set("No se ha detectado un rostro")
            self.audioPlayer.playFaceNotDetectedTimeExausted()
            self.root.after(10000, self.restart)  

        elif eventString == "LecturaDNIQrInvalido":
            self.labelMessage.set("El código QR es inválido")
            self.audioPlayer.playDNIQrInvalid()
            self.root.after(10000, self.restart)  

    def takePicture(self):
        TakePictureThread(self.enroller, self.queue).start() 

    def readDNI(self):
        ReadDniThread(self.enroller, self.queue).start() 

    def restart(self):
        from py_session import py_session
        py_session()
        self.buttonImage = ImageTk.PhotoImage(file = 'comenzar2.png')
        self.button = Button(self.root, image=self.buttonImage, command=self.startEnroll)
        self.button.pack(expand=0.5)
        self.labelMessage.set("Bienvenido al proceso de enrolamiento")
        self.audioPlayer.playEnrollWelcome()
        self.enroller.init()

    def startEnroll(self):
        self.button.destroy()
        self.labelMessage.set("Por favor posicionate mirando\nde frente a la cámara")
        self.audioPlayer.playPositionFace()
        self.root.after(5000, self.takePicture)
        self.onEvent()

    def initWindow(self):
        self.root.title("ENROLAMIENTO")
        self.root.configure(background='#c1e1ec')
        self.root.attributes("-fullscreen", True)


        #self.background = ImageTk.PhotoImage(file = 'bg.jpg')
        #self.bgLabel = Label(self.root, image=self.background)
        #self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        self.labelMessage = StringVar()
        self.labelMessage.set("Bienvenido al proceso de enrolamiento")
        label = Label(self.root, textvariable=self.labelMessage, font=("Arial", 50, "bold"), justify=CENTER, anchor=W)
        label.configure(background='#c1e1ec')
        label.pack()

        self.buttonImage = ImageTk.PhotoImage(file = 'comenzar2.png')
        self.button = Button(self.root, image=self.buttonImage, command=self.startEnroll)
        self.button.pack(expand=0.5)


app = App()

