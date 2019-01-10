import pygame

class AudioPlayer():
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        name = 'BIENVENIDO'
        self.sounds[name] = pygame.mixer.Sound('Sounds/{}.wav'.format(name))

        name = 'POSICIONAR-CARA'
        self.sounds[name] = pygame.mixer.Sound('Sounds/{}.wav'.format(name))

        name = 'COLOCAR-DNI'
        self.sounds[name] = pygame.mixer.Sound('Sounds/{}.wav'.format(name))

        name = 'ENROLAMIENTO-EXITOSO'
        self.sounds[name] = pygame.mixer.Sound('Sounds/{}.wav'.format(name))

        name = 'ROSTRO-NO-DETECTADO'
        self.sounds[name] = pygame.mixer.Sound('Sounds/{}.wav'.format(name))

        name = 'TIEMPO-ESPERA-AGOTADO'
        self.sounds[name] = pygame.mixer.Sound('Sounds/{}.wav'.format(name))

        name = 'COLOCAR-DNI-AUTENTICACION'
        self.sounds[name] = pygame.mixer.Sound('Sounds/{}.wav'.format(name))

        name = 'DNI-NO-CORRESPONDE-AUTENTICACION'
        self.sounds[name] = pygame.mixer.Sound('Sounds/{}.wav'.format(name))

        name = 'AUTENTICACION-EXITOSA'
        self.sounds[name] = pygame.mixer.Sound('Sounds/{}.wav'.format(name))

        name = 'ROSTRO-NO-ENCONTRADO-AUTENTICACION'
        self.sounds[name] = pygame.mixer.Sound('Sounds/{}.wav'.format(name))

        name = 'DNI-QR-INVALIDO'
        self.sounds[name] = pygame.mixer.Sound('Sounds/{}.wav'.format(name))

    def stop(self):
        pygame.mixer.quit()

    def playEnrollWelcome(self):
        self.sounds['BIENVENIDO'].play()

    def playPositionFace(self):
        self.sounds['POSICIONAR-CARA'].play()

    def playReadDNI(self):
        self.sounds['COLOCAR-DNI'].play()

    def playReadDNIWaitTimeExausted(self):
        self.sounds['TIEMPO-ESPERA-AGOTADO'].play()
    
    def playFaceNotDetectedTimeExausted(self):
        self.sounds['ROSTRO-NO-DETECTADO'].play()

    def playEnrollSuccess(self):
        self.sounds['ENROLAMIENTO-EXITOSO'].play()
    
    def playReadDNIAuthenticate(self):
        self.sounds['COLOCAR-DNI-AUTENTICACION'].play()

    def playDNIAuthenticateNotRegistered(self):
        self.sounds['DNI-NO-CORRESPONDE-AUTENTICACION'].play()
    
    def playAuthenticationSucess(self):
        self.sounds['AUTENTICACION-EXITOSA'].play()

    def playFaceNotKnownAuthentication(self):
        self.sounds['ROSTRO-NO-ENCONTRADO-AUTENTICACION'].play()

    def playDNIQrInvalid(self):
        self.sounds['DNI-QR-INVALIDO'].play()



