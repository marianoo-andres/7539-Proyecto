import json
import os
import shutil
import pickle
import cv2
class Person:
    def __init__(self, dataString=None, image=None, encoding=None, dirName=None):
        self.valid = True
        if dirName:
            self.loadFromDir(dirName)
        else:
            self.parse(dataString)
            self.image = image
            self.encoding = encoding
    def parse(self, data):
        try:
            data = data.split("@")
            if (data[0] == ''):
                # DNI viejo
                self.dni = data[1].replace(" ","")
                self.surname = data[4]
                self.name = data[5]
                self.birthDate = data[7].replace(" ","")
                self.sex = data[8].replace(" ","")
            else:
                #DNI nuevo
                self.surname = data[1]
                self.name = data[2]
                self.sex = data[3].replace(" ","")
                self.dni = data[4].replace(" ","")
                self.birthDate = data[6].replace(" ","")
            self.valid = True
        except:
            self.valid = False
            

    def loadFromDir(self, dirName):
        dirPath = os.path.join("Database", dirName)
        imagePath = os.path.join(dirPath, "image.png")
        encodingPath = os.path.join(dirPath, "encoding.pickle")
        dataPath = os.path.join(dirPath, "data.json")

        self.image = cv2.imread(imagePath)
        
        with open(encodingPath, 'rb') as f:
            self.encoding = pickle.load(f)

        self.setDataFromJsonFile(dataPath)
        self.valid = True
        
    def setDataFromJsonFile(self, dataPath):
        file = open(dataPath)
        data = json.load(file)
        self.name = data['nombre']
        self.surname = data['apellido']
        self.birthDate = data['fecha_nacimiento']
        self.sex = data['sexo']
        self.dni = data['dni']

    def getJsonString(self):
        dic = {
            "nombre": self.name,
            "apellido": self.surname,
            "fecha_nacimiento": self.birthDate,
            "sexo": self.sex,
            "dni": self.dni
        }
        return json.dumps(dic)
    def __str__(self):
        return self.name + ' ' + self.surname
    def same(self, another):
        if not self.name == another.name:
            print(self.name)
            print(another.name)
            return False
        if not self.surname == another.surname:
            print(self.surname)
            print(another.surname)
            return False
        if not self.dni == another.dni:
            print(self.dni)
            print(another.dni)
            return False
        if not self.birthDate == another.birthDate:
            print(self.birthDate)
            print(another.birthDate)
            return False
        if not self.sex == another.sex:
            print(self.sex)
            print(another.sex)
            return False
        return True 
    def save(self):
        dirPath = os.path.join("Database", self.name + " " + self.surname)
        
        shutil.rmtree(dirPath, ignore_errors=True)

        os.mkdir(dirPath)

        cv2.imwrite(os.path.join(dirPath,"image.png"), self.image)

        file = open(os.path.join(dirPath, "encoding.pickle"), 'wb')
        pickle.dump(self.encoding, file)
        file.close()

        file = open(os.path.join(dirPath, "data.json"), 'w')
        file.write(self.getJsonString())
        file.close()