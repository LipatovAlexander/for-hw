import cv2
import utils
from keras.models import load_model

ORIGINAL_WINDOW = 'Original'
OUTPUT_WINDOW = 'Output'

face_cascade = cv2.CascadeClassifier(
    './models/haarcascade_frontalface_default.xml')
emotion_classifier = load_model('./models/emotion_model.hdf5')
emotion_classifier_input_size = emotion_classifier.input_shape[1:3]

cv2.namedWindow(ORIGINAL_WINDOW)
cv2.namedWindow(OUTPUT_WINDOW)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, bgr_image = cap.read()
    cv2.imshow(ORIGINAL_WINDOW, bgr_image)

    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

    faces = face_cascade.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    for face_coordinates in faces:
        face = utils.try_process_input(
            gray_image, face_coordinates, emotion_classifier_input_size)

        if face is False:
            continue

        emotion_prediction = emotion_classifier.predict(face)
        emotion, emotion_probability = utils.get_emotion(emotion_prediction)

        utils.draw_emoji(rgb_image, face_coordinates, emotion)

    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.imshow(OUTPUT_WINDOW, bgr_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
