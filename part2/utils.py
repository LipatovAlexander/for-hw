from statistics import mode
from PIL import Image
import cv2
import numpy as np

emotion_labels = {
    0: 'angry',
    1: 'disgust',
    2: 'fear',
    3: 'happy',
    4: 'sad',
    5: 'surprise',
    6: 'neutral'
}


emojis = {
    'angry': Image.open('emojis/angry.png'),
    'disgust': Image.open('emojis/disgust.png'),
    'fear': Image.open('emojis/fear.png'),
    'happy': Image.open('emojis/happy.png'),
    'sad': Image.open('emojis/sad.png'),
    'surprise': Image.open('emojis/surprise.png'),
    'neutral': Image.open('emojis/neutral.png')
}


offsets = (20, 40)
emotions_window = []
faces_window = []


def draw_emoji(image, coordinates, emotion):
    coordinates = mode_with_window(coordinates, faces_window)
    x, y, width, height = coordinates

    emoji = emojis[emotion]
    emoji = emoji.resize((width, height))

    image_pil = Image.fromarray(image)
    image_pil.paste(emoji, (x, y), emoji)

    image[:, :] = np.asarray(image_pil)[:, :]


def try_process_input(image, coordinates, target_size):
    x, y, width, height = coordinates
    x_off, y_off = offsets
    x1, x2, y1, y2 = x - x_off, x + width + x_off, y - y_off, y + height + y_off
    face = image[y1:y2, x1:x2]
    try:
        face = cv2.resize(face, (target_size))
    except:
        return False

    face = face.astype('float32')
    face = face / 255.0
    face = face - 0.5
    face = face * 2.0
    face = np.expand_dims(face, 0)
    face = np.expand_dims(face, -1)
    return face


def get_emotion(emotion_prediction):
    emotion_probability = np.max(emotion_prediction)
    emotion_label_arg = np.argmax(emotion_prediction)
    emotion_text = emotion_labels[emotion_label_arg]

    emotion_text = mode_with_window(emotion_text, emotions_window)
    return emotion_text, emotion_probability


def mode_with_window(item, window, window_size=10):
    window.append(item)

    if len(window) > window_size:
        window.pop(0)

    try:
        return mode(window)
    except:
        return item
