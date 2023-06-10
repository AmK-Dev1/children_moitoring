from playsound import playsound

class Alarm:
    def __init__(self,camera):
        self.camera = camera
        
    def alert(self):
        playsound(f'data/sounds/cam{self.camera["id"]}.mp3')
