# Importation du wrapper d'OpenCV.
import cv2
import numpy as np
from time import sleep
from json import load

class ComputerVision():
    def discover_opencv(self):

        # On charge une image, et on garde la couleur, ou on la mets en nuance de gris.
        image = cv2.imread('moi.jpeg', cv2.IMREAD_GRAYSCALE)

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

    def discover_lines_and_shapes_and_text(self):
        image = cv2.imread('moi.jpeg', cv2.IMREAD_UNCHANGED)
        height, width, _ = image.shape

        image = cv2.line(image, (0,0), (width, height), (0,0,255), 5)
        image = cv2.line(image, (width,0), (0, height), (0,0,255), 5)
        image = cv2.line(image, (width//2, 0), (width//2, height), (0,0,255), 5)
        image = cv2.line(image, (0, height//2), (width, height//2), (0,0,255), 5)

        image = cv2.circle(image, (width//2, height//2), 50, (0, 255, 255), 10)
        image = cv2.circle(image, (width//2, height//2), height//2, (0, 255, 255), 10)
        image = cv2.circle(image, (width//2, height//2), width//2, (0, 255, 255), 10)

        margin = 20
        image = cv2.rectangle(image, (margin, margin), (width-margin, height-margin), (255,255,0), 20)

        font = cv2.FONT_HERSHEY_PLAIN
        image = cv2.putText(image, "Nicolas METIVIER", (10, height), font, 4, (255,255,255), 5, cv2.LINE_AA)

        cv2.imshow("""Photo""", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def discover_colors_detectors(self):
        capture = cv2.VideoCapture("poussins.mp4")

        while True:
            ret, frame = capture.read()

            # Réinitialiser la vidéo au début
            if not ret:
                capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            # ...
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            with open("color-threshold.json", "r") as file:
                color_threshold = load(file)

            upper_threshold = np.array([color_threshold["red"]["upper"], color_threshold["green"]["upper"], color_threshold["blue"]["upper"]]) # R, G, B
            lower_threshold = np.array([color_threshold["red"]["lower"], color_threshold["green"]["lower"], color_threshold["blue"]["lower"]]) # R, G, B

            mask = cv2.inRange(hsv_frame, lower_threshold, upper_threshold)
            filtered_frame = cv2.bitwise_and(frame, frame, mask=mask)


            cv2.imshow("Orignal Frame", frame)
            cv2.imshow("HSV Frame", hsv_frame)
            cv2.imshow("Yellow Mask",mask)
            cv2.imshow("Filtered Frame",filtered_frame)

            if (cv2.waitKey(1) == ord('q')):
                break
        capture.release()
        cv2.destroyAllWindows()

    def discover_corner_detection(self):
        image = cv2.imread('chessboard.jpg')
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray_image, 180, 0.005, 7)
        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(image, (int(x), int(y)), 10, (0,0,255), 3)

        # for index_1 in range(len(corners)):
        #     for index_2 in range(index_1 + 1, len(corners)):
        #         corner_1 = tuple(map(lambda x : int(x), corners[index_1][0]))
        #         corner_2 = tuple(map(lambda x : int(x), corners[index_2][0]))
        #         line_color = tuple(map(lambda x: int(x), np.random.randint(0, 255, size=3)))
        #         cv2.line(image, corner_1, corner_2, line_color, 1)

        
        cv2.imshow("Corners", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def rotate(self, image, angle):
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_image = cv2.warpAffine(image, matrix, (width, height))
        return rotated_image

    def discover_template_matching(self):
        f1_image = cv2.imread('formule1.png')
        capot_image = cv2.imread('capot-f1.png')

        # capot_image = cv2.resize(capot_image, (0,0), fx=2, fy=2)
        # capot_image = self.rotate(capot_image, 180)

        height, width = capot_image.shape[:2]
        methods = [
            cv2.TM_CCOEFF,  cv2.TM_CCOEFF_NORMED,
            cv2.TM_CCORR,   cv2.TM_CCORR_NORMED,
            cv2.TM_SQDIFF,  cv2.TM_SQDIFF_NORMED
        ]
        for method in methods:
            f1_image_copy = f1_image.copy()
            result = cv2.matchTemplate(f1_image_copy, capot_image, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                location = min_loc
            else:
                location = max_loc
            
            bottom_right = (location[0] + width, location[1] + height)
            cv2.rectangle(f1_image_copy, location, bottom_right, (255,255,0), 5)
            cv2.imshow("F1", f1_image_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def discover_orb(self):
        f1_image = cv2.imread('formule1.png')
        capot_image = cv2.imread('capot-f1.png')

        # gray_f1_image = cv2.cvtColor(f1_image, cv2.COLOR_BGR2GRAY)
        # gray_capot_image = cv2.cvtColor(capot_image, cv2.COLOR_BGR2GRAY)

        orb = cv2.ORB.create(nfeatures=78*65)
        keypoints_capot, descriptors_capot = orb.detectAndCompute(capot_image, None)
        keypoints_f1, descriptors_f1 = orb.detectAndCompute(f1_image, None)
        brut_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = brut_force.match(descriptors_capot, descriptors_f1)
        matches = sorted(matches, key=lambda x: x.distance)
        print(len(matches))

        result_image = cv2.drawMatches(capot_image, keypoints_capot, f1_image, keypoints_f1, matches[:10], None, cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow("Matches", result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def detect_contours(self, gray_image, threshold1=50, threshold2=100):
        edges = cv2.Canny(gray_image, threshold1, threshold2)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def discover_find_outlines(self):

        capture = cv2.VideoCapture("circulation.mp4")

        while True:

            _, image = capture.read()

            if not _:
                capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            # black_background = np.zeros(image.shape, np.uint8)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            contours = self.detect_contours(gray_image)

            for contour in contours:
                cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
            
            zoom = 0.3
            image = cv2.resize(image, (0, 0), fx=zoom, fy=zoom)

            cv2.imshow("Contours", image)
            

            if (cv2.waitKey(1) == ord('q')):
                break
        capture.release()
        cv2.destroyAllWindows()

    def discorver_geometric_shapes(self):
        capture = cv2.VideoCapture("circulation.mp4")
        while True:
            ret, frame = capture.read()

            if not ret:
                capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            contours = self.detect_contours(gray_frame)
            for contour in contours:
                is_closed = True # cv2.isContourConvex(contour)
                perimeter = cv2.arcLength(contour, is_closed)
                approx = cv2.approxPolyDP(contour, 0.04 * perimeter, is_closed)
                points = len(approx)
                shape_name = "Inconnu"

                width = cv2.boundingRect(contour)[2]
                height = cv2.boundingRect(contour)[3]

                if points == 3:
                    shape_name = "Triangle"
                elif points == 4:
                    ration = width / height
                    if ration >= 0.95 and ration <= 1.05:
                        shape_name = "Carré"
                    else:
                        shape_name = "Rectangle"

                elif points == 8:
                    shape_name = "Octogone"
                
                elif points > 8:
                    area = cv2.contourArea(contour)
                    circularity = (4 * np.pi * area) / (perimeter ** 2)
                    if circularity > 0.85:
                        shape_name = "Cercle"
                    elif circularity > 0.75:
                        shape_name = "Ellipse"

                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

                cv2.putText(frame, shape_name, (contour[0][0][0] - 5, contour[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            cv2.imshow("Contours", frame)
            if (cv2.waitKey(1) == ord('q')):
                break
        capture.release()
        cv2.destroyAllWindows()

    def discover_tracker_kcf(self):
        # 1. Chargement de la vidéo et du template (la voiture à chercher)
        capture = cv2.VideoCapture("circulation.mp4")
        
        # On charge l'image de la voiture (en couleur BGR normale, pas HSV pour le template matching)
        template = cv2.imread('red-card.png')
        
        # Il est crucial que le template soit à la même échelle que la voiture dans la vidéo.
        # Si besoin, applique le même zoom ou redimensionne-le :
        # template = cv2.resize(template, (largeur, hauteur))
        
        h_temp, w_temp = template.shape[:2]

        # 2. Initialisation du tracker KCF
        tracker = cv2.TrackerKCF.create()
        tracker_initialized = False
        zoom = 0.4
        
        # Seuil de confiance pour le template matching (0.7 = 70% de ressemblance minimum)
        THRESHOLD = 0.7 

        while True:
            has_frame, capture_image = capture.read()

            if not has_frame:
                capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                tracker = cv2.TrackerKCF.create()
                tracker_initialized = False
                continue
        
            capture_image = cv2.resize(capture_image, (0, 0), fx=zoom, fy=zoom)

            if not tracker_initialized:
                # --- PHASE DE RECHERCHE PAR TEMPLATE MATCHING (3 premières secondes) ---
                
                # On applique l'algorithme de correspondance
                result = cv2.matchTemplate(capture_image, template, cv2.TM_CCOEFF_NORMED)
                
                # On récupère le score maximum et sa position
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                # Si le score de ressemblance dépasse notre seuil, on considère qu'on a trouvé la voiture
                if max_val > THRESHOLD:
                    x, y = max_loc
                    bbox = (x, y, w_temp, h_temp) # La taille de la box est celle du template
                    
                    # Initialisation du KCF sur la zone trouvée
                    tracker.init(capture_image, bbox)
                    tracker_initialized = True
                else:
                    cv2.putText(capture_image, "Recherche de la voiture (Template)...", (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            else:
                # --- PHASE DE TRACKING KCF ---
                ok, bbox = tracker.update(capture_image)

                if ok:
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    cv2.rectangle(capture_image, p1, p2, (0, 0, 255), 3)
                    cv2.putText(capture_image, "TRACKING", (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                else:
                    cv2.putText(capture_image, "Cible perdue !", (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    tracker_initialized = False
                    tracker = cv2.TrackerKCF.create()

            cv2.imshow("Surveillance", capture_image)

            if cv2.waitKey(1) in [ord('q'), 27]:
                break

        capture.release()
        cv2.destroyAllWindows()
    