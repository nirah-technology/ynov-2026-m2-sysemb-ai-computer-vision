# Importation du wrapper d'OpenCV.
import cv2
import numpy as np
from time import sleep

class ComputerVision():
    def discover_opencv(self):

        # On charge une image, et on garde la couleur, ou on la mets en nuance de gris.
        image =cv2.imread('moi.jpeg', cv2.IMREAD_GRAYSCALE)

        # On redimenssionne l'image -> scale.
        zoom = 0.5
        image = cv2.resize(image, (0, 0), fx=zoom, fy=zoom)

        # On pivote l'image
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # On flip l'image
        image = cv2.flip(image, -1)

        # On enregistre l'image.
        cv2.imwrite('moi_zoom_50_gray.jpeg', image)


        # On affiche l'image dans une fenetre.
        cv2.imshow('Photo', image)

        # On laisse la fenetre ouverte indéfiniement
        cv2.waitKey(0)

        # On détruit toutes les fenetres.
        cv2.destroyAllWindows()

    def understand_images_fundamentals(self):
        image = cv2.imread('moi.jpeg', cv2.IMREAD_UNCHANGED)
        mini_image = image[500:700, 600:900]
        image[100:300, 650:950] = mini_image
        cv2.imshow('Photo', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def discover_video_capture(self):
        # capture = cv2.VideoCapture(0)             # Caméra
        capture = cv2.VideoCapture("poussins.mp4")  # Vidéo

        width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # print(capture.get(cv2.CAP_PROP_FRAME_COUNT))

        while True:

            sleep(0.02)     # Pause pour réduire le FPS
            ret, frame = capture.read()

            # Réinitialiser la vidéo au début
            if not ret:
                capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            black_image = np.zeros(frame.shape, np.uint8)

            # On affiche le flux vidéo de la caméra
            # cv2.imshow('Video', frame)
            
            zoom = 0.5
            small_frame = cv2.resize(frame, (0, 0), fx=zoom, fy=zoom)


            black_image[0:int(height//2), 0:int(width//2)] = small_frame
            black_image[0:int(height//2), int(width//2):] = cv2.flip(small_frame, 1)
            black_image[int(height//2):, :int(width//2)] = cv2.flip(small_frame, 0)
            black_image[int(height//2):, int(width//2):] = cv2.flip(small_frame, -2)


            cv2.imshow('Video', black_image)

            if (cv2.waitKey(1) in [ord('q')]):
                break
    
        capture.release()
        cv2.destroyAllWindows()
