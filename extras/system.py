
import json
import cv2 
import PIL
import numpy
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

class System:

    def __init__(self):
        self.config = json.load(open('config.json'))['config']
        self.cameras = self.config['cameras']
        self.output_queues = []
        self.video_paths = [camera['source'] for camera in self.cameras]
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

                # Redimensionner les frames pour les afficher sur une seule fenêtre
                resized_frame = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2))) 
                # put text 
                cv2.putText(img=resized_frame , text=f"camera : {cap['camera']['id']}",org=(250,25),fontFace=cv2.FONT_HERSHEY_SIMPLEX ,fontScale=1, color=(0,255,0), thickness=2)
                if(cap['camera']['risky'] == 1):
                    cv2.putText(img=resized_frame , text=f"risky area",org=(250,50),fontFace=cv2.FONT_HERSHEY_SIMPLEX ,fontScale=1, color=(0,0,255), thickness=2)
                cv2.imshow(window_name, resized_frame)

            # Attendre l'appui sur la touche 'q' pour quitter
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Libérer les ressources
        for cap in caps:
            cap['cap'].release()

        cv2.destroyAllWindows()
