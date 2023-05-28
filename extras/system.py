
import json
import cv2 
import PIL
import numpy
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from ultralytics import YOLO
import supervision as sv

class System:

    def __init__(self):
        self.config = json.load(open('config.json'))['config']
        self.cameras = self.config['cameras']
        self.output_queues = []
        self.video_paths = [camera['source'] for camera in self.cameras]
        self.model = YOLO("data/weights/YOLOV8best.pt")
        self.box_annotator = sv.BoxAnnotator(
                                            thickness=2,
                                            text_thickness=2,
                                            text_scale=1
                                        )
        print('system')
    
    def main(self):
        
        # Ouvrir les vidéos
        caps = []
        windows = []
        for camera in self.cameras:
            cap = cv2.VideoCapture(camera['source'])
            window_name = f"camera - {camera['id']}" 
            caps.append({"cap":cap,"camera":camera})

            windows.append(window_name)
            cv2.namedWindow(window_name)

        # Lire les vidéos en boucle
        while True:
            for cap, window_name in zip(caps, windows):
                ret, frame = cap['cap'].read()

                # Si la lecture de la vidéo est terminée, revenir au début
                if not ret:
                    cap['cap'].set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = cap['cap'].read()

                frame = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2))) 
                # predict results : 
                result = self.model(frame, agnostic_nms=True)[0]
                detections = sv.Detections.from_yolov8(result)
                frame = self.box_annotator.annotate(
                        scene=frame, 
                        detections=detections, 
                        labels=""
                        ) 
                
                # Redimensionner les frames pour les afficher sur une seule fenêtre
                #frame = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2))) 
                
                # put text 
                cv2.putText(img=frame , text=f"camera : {cap['camera']['id']}",org=(250,25),fontFace=cv2.FONT_HERSHEY_SIMPLEX ,fontScale=1, color=(0,255,0), thickness=2)
                if(cap['camera']['risky'] == 1):
                    cv2.putText(img=frame , text=f"risky area",org=(250,50),fontFace=cv2.FONT_HERSHEY_SIMPLEX ,fontScale=1, color=(0,0,255), thickness=2)
                cv2.imshow(window_name,frame)

            # Attendre l'appui sur la touche 'q' pour quitter
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Libérer les ressources
        for cap in caps:
            cap['cap'].release()

        cv2.destroyAllWindows()
