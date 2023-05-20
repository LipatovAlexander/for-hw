from statistics import mode
from PIL import Image
import cv2
import numpy as np

emotions = {
    0: 'angry',
    1: 'disgust',
    2: 'fear',
    3: 'happy',
    4: 'sad',
    5: 'surprise',
    6: 'neutral'
}


emojis = {
    'angry': Image.open('emojis/angry/angry.png'),
    'so_angry': Image.open('emojis/angry/so_angry.png'),
    'super_angry': Image.open('emojis/angry/super_angry.png'),
    'disgust': Image.open('emojis/disgust/disgust.png'),
    'so_disgust': Image.open('emojis/disgust/so_disgust.png'),
    'super_disgust': Image.open('emojis/disgust/super_disgust.png'),
    'fear': Image.open('emojis/fear/fear.png'),
    'so_fear': Image.open('emojis/fear/so_fear.png'),
    'super_fear': Image.open('emojis/fear/super_fear.png'),
    'happy': Image.open('emojis/happy/happy.png'),
    'so_happy': Image.open('emojis/happy/so_happy.png'),
    'super_happy': Image.open('emojis/happy/super_happy.png'),
    'sad': Image.open('emojis/sad/sad.png'),
    'so_sad': Image.open('emojis/sad/so_sad.png'),
    'super_sad': Image.open('emojis/sad/super_sad.png'),
    'surprise': Image.open('emojis/surprise/surprise.png'),
    'so_surprise': Image.open('emojis/surprise/so_surprise.png'),
    'super_surprise': Image.open('emojis/surprise/super_surprise.png'),
    'neutral': Image.open('emojis/neutral/neutral.png'),
    'so_neutral': Image.open('emojis/neutral/so_neutral.png'),
    'super_neutral': Image.open('emojis/neutral/super_neutral.png')
}


offsets = (20, 40)
emotions_window = []
faces_window = []


def get_emoji(emotion, probability):
    if probability > 0.8:
        emotion = 'super_' + emotion
    elif probability > 0.5:
        emotion = 'so_' + emotion

    return emojis[emotion]


def draw_emoji(image, coordinates, emotion, emotion_probability):
    coordinates = mode_with_window(coordinates, faces_window)
    x, y, width, height = coordinates

    emoji = get_emoji(emotion, emotion_probability)
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
    emotion_arg = np.argmax(emotion_prediction)
    emotion_text = emotions[emotion_arg]

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
