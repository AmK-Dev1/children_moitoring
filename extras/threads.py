import cv2
import os
import threading

# Classe pour le thread d'affichage des images d'un dossier
class ThreadAffichageImages(threading.Thread):
    def __init__(self, nom_dossier, chemin_dossier):
        threading.Thread.__init__(self)
        self.nom_dossier = nom_dossier
        self.chemin_dossier = chemin_dossier
        self.show = True
    
    def run(self):
        # Lire la liste des fichiers d'images dans le dossier
        images = os.listdir(self.chemin_dossier)
        
        # Trier les images par ordre alphabétique
        images = sorted(images)
        
        # Ouvrir la première image pour obtenir les dimensions
        premiere_image = cv2.imread(os.path.join(self.chemin_dossier, images[0]))
        hauteur, largeur, _ = premiere_image.shape
        
        # Créer une fenêtre pour le dossier d'images actuel
        cv2.namedWindow(self.nom_dossier, cv2.WINDOW_NORMAL)
        
        # Boucle pour lire et afficher les images en continu
        while self.show:

            for image_name in images:
                # Lire l'image
                image_path = os.path.join(self.chemin_dossier, image_name)
                image = cv2.imread(image_path)
                
                # Redimensionner l'image à la taille de la première image
                image = cv2.resize(image, (largeur, hauteur))

                # Afficher l'image dans la fenêtre correspondante
                cv2.imshow(self.nom_dossier, image)
                
                # Attendre 50 millisecondes (ajuster selon votre préférence)
                if cv2.waitKey(50) & 0xFF == ord('q'):
                    return
                    
