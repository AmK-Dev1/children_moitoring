
import cv2
from ultralytics import YOLO
import os
import threading
from playsound import playsound
import time


class Alarm:
    def __init__(self,camera):
        self.camera = camera
        self.thread = None

    def luncher(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread_audio = threading.Thread(target=self.alert)
            self.thread_audio.start()

    def alert(self):
        audio_path = os.path.join("data","sounds","cam3.mp3")
        playsound(audio_path)
        


class System(threading.Thread):

    def __init__(self,camera):
        threading.Thread.__init__(self)
        # model 
        self.camera = camera

        self.model = YOLO("data/weights/YOLOV8Nbest.pt")
        self.model.conf = 0.25  # NMS confidence threshold
        self.model.iou = 0.45  # NMS IoU threshold
        self.alarm = False
        self.alarm_delay = 15000 #15 seconds 
        self.alarm_manager = Alarm(self.camera)


    def run(self):
        path = self.camera['source']
        images = os.listdir(path)
        # Trier les images par ordre alphabétique
        images = sorted(images)

        hauteur = int(self.camera['resolution']['h'])
        largeur = int(self.camera['resolution']['w'])

        cv2.namedWindow(f"Camera {self.camera['id']}",cv2.WINDOW_NORMAL)
        cv2.resizeWindow(f"Camera {self.camera['id']}", largeur, hauteur)
        
        while True:
            for image_name in images:
                # Redimensionner l'image à la résolution
                results = self.model.predict(os.path.join(path , image_name),verbose=False) 
                
                #detect kid 
                if(0 in results[0].boxes.cls and self.camera['risky']==1 and not self.alarm):
                    print('khlat')
                    self.alarm = True
                    self.alarm_manager.luncher()
                    thread = threading.Thread(target=self.initialize_alarm)
                    thread.start()
                    

                    
                    
                image = results[0].plot()

                image = cv2.resize(image, (largeur, hauteur))
                
                cv2.imshow(f"Camera {self.camera['id']}" , image)
                # Attendre 50 millisecondes (ajuster selon votre préférence)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return
    def initialize_alarm(self):
        time.sleep(10)
        self.alarm = False



