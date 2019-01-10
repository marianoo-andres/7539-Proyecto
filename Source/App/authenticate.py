from tkinter import *
import queue
import datetime
import time
import threading
import os
import json
from PIL import ImageTk
from Authenticator import Authenticator
from AudioPlayer import AudioPlayer
from Person import Person
class AuthenticateFaceThread(threading.Thread):
    def __init__(self, authenticator, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.authenticator = authenticator
    def run(self):
        person = self.authenticator.authenticateFace()
        if person:
            event = "AutenticacionTerminada"
        else:
            event = "DeteccionTiempoAgotado"
        self.queue.put([event, person])

class ReadDniThread(threading.Thread):
    def __init__(self, authenticator, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.authenticator = authenticator
    def run(self):
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
            person = Person(dataString=data)

        os.remove(os.path.join("Temp",fileName))


        if not person.valid:
            event = "LecturaDNIQrInvalido"
            self.queue.put([event])
        else:
            faceMatchesDNI = self.authenticator.authenticate(data)
            event = "LecturaDNITerminada"
            self.queue.put([event, faceMatchesDNI])

class App:
    def __init__(self):
        #Tkinter
        self.root = Tk()
        self.audioPlayer = AudioPlayer()
        self.initWindow()
        self.queue = queue.Queue()
        self.authenticator = Authenticator()
        self.startAuthentication()
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
        print(eventList)
        if eventString == "AutenticacionTerminada":
            personAuthenticated = eventList[1]
            if personAuthenticated == "Unknown":
                self.audioPlayer.playFaceNotKnownAuthentication()
                self.labelMessage.set("Rostro desconocido.\nDebe enrolarse previamente")
                self.root.after(10000, self.restart)     
            else:
                self.audioPlayer.playReadDNIAuthenticate()
                self.labelMessage.set("Bienvenido\n{} {}\n\nColoque su DNI por favor".format(personAuthenticated.name, personAuthenticated.surname))
                self.readDNI()
        elif eventString == "LecturaDNIEsperaAgotada":
            self.labelMessage.set("Tiempo de espera agotado")
            self.audioPlayer.playReadDNIWaitTimeExausted()
            self.root.after(10000, self.restart)
        elif eventString == "LecturaDNITerminada":
            faceMatchesDNI = eventList[1]
            if faceMatchesDNI:
                self.audioPlayer.playAuthenticationSucess()
                self.labelMessage.set("Autenticación exitosa!")
                self.root.after(10000, self.restart)
            else:
                self.audioPlayer.playDNIAuthenticateNotRegistered()
                self.labelMessage.set("El DNI colocado no corresponde con el registrado")
                self.root.after(10000, self.restart)

        elif eventString == "DeteccionTiempoAgotado":
            self.labelMessage.set("No se ha detectado un rostro")
            self.audioPlayer.playFaceNotDetectedTimeExausted()
            self.root.after(10000, self.restart) 
        
        elif eventString == "LecturaDNIQrInvalido":
            self.labelMessage.set("El código QR es inválido")
            self.audioPlayer.playDNIQrInvalid()
            self.root.after(10000, self.restart) 

    def authenticateFace(self):
        AuthenticateFaceThread(self.authenticator, self.queue).start() 

    def readDNI(self):
        ReadDniThread(self.authenticator, self.queue).start() 

    def restart(self):
        from py_session import py_session
        py_session()
        self.labelMessage.set("Por favor posicionate mirando\nde frente a la cámara")
        self.audioPlayer.playPositionFace()
        self.authenticator.init()
        self.startAuthentication()

    def startAuthentication(self):
        self.root.after(5000, self.authenticateFace)
        self.onEvent()

    def initWindow(self):
        self.root.title("AUTENTICACIÓN")
        self.root.configure(background='#C8919C')
        self.root.attributes("-fullscreen", True)

        self.labelMessage = StringVar()
        self.labelMessage.set("Por favor posicionate mirando\nde frente a la cámara")
        self.audioPlayer.playPositionFace()
        label = Label(self.root, textvariable=self.labelMessage, font=("Arial", 50, "bold"), justify=CENTER, anchor=W)
        label.configure(background='#C8919C')
        label.pack()

app = App()
