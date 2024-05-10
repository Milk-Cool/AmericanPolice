import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np

base_options = python.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        continue
    frame = np.fliplr(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image = mp.Image(mp.ImageFormat.SRGB, data=frame)

    detection_result = detector.detect(image)

    if not detection_result.face_landmarks:
        continue
    
    nose_tip = detection_result.face_landmarks[0][197]
    x = nose_tip.x * cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    y = nose_tip.y * cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    c = frame[int(x)][int(y)]
    av = (int(c[0]) + int(c[1]) + int(c[2])) // 3
    if av < 60:
        print("A menace to this society")
    elif av < 100:
        print("Still OK")
    else:
        print("Totally fine")