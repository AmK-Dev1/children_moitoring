import cv2
import yolov5
import os
import random

class_names={
    0:"-0",
    1:"-1",
    2:"adult",
    3:"kid"
    }

model = yolov5.load('data/weights/best.pt', device='cpu')
# set model parameters
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False  # NMS multiple labels per box
model.max_det = 1000  # maximum number of detections per image
model.names = class_names

# Chemins vers les vidéos
video_paths = ["3.mp4"]

# Ouvrir les vidéos
videos = [cv2.VideoCapture(path) for path in video_paths]

# Vérifier si les vidéos sont ouvertes
for video in videos:
    if not video.isOpened():
        print("Impossible d'ouvrir la vidéo.")
        exit()

# Lire les vidéos en boucle
while True:
    frames = []  # Liste pour stocker les frames de chaque vidéo

    # Lire les frames de chaque vidéo
    for video in videos:
        ret, frame = video.read()

        # Si la lecture de la vidéo est terminée, revenir au début
        if not ret:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = video.read()

        result = model(frame)
        frames.append(result.render()[0])

    # Redimensionner les frames pour les afficher sur une seule fenêtre
    resized_frames = [cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2))) for frame in frames]

    # Afficher les frames sur une seule fenêtre
    combined_frame = cv2.hconcat(resized_frames)
    cv2.imshow("Videos", combined_frame)

    # Attendre l'appui sur la touche 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
for video in videos:
    video.release()

cv2.destroyAllWindows()
