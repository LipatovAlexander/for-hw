import cv2
import numpy as np
from utils import hsv2rgb, cart2pol, points_in_circle

window_name = 'HSV Color Palette'
color_window_name = 'Selected color'
win_height = 300
win_width = 300
circle_center_x = 150
circle_center_y = 150
circle_radius = 140

selected_h = 0
selected_s = 0
selected_v = 0

color_img = np.zeros((200, 200, 3), np.uint8)
img = np.zeros((win_height,win_width,3), np.uint8)

def get_HSV(x, y):
    s, h = cart2pol(x - circle_center_x, circle_center_y - y)
    s = min(s, circle_radius) * (100 / circle_radius)
    s, h = round(s), round(h)
    return h, s, selected_v

def draw_palette():
    global selected_v
    for x, y in points_in_circle(circle_radius, circle_center_x, circle_center_y):
        if x == 265 and y == 75:
            pass
        h, s, v = get_HSV(x, y)
        r, g, b = hsv2rgb(h, s, selected_v)
        img[y, x] = [b, g, r]
        cv2.imshow(window_name, img)


def draw_color():
    r, g, b = hsv2rgb(selected_h, selected_s, selected_v)
    color_img[:] = [b, g, r]
    cv2.imshow(color_window_name, color_img)


def print_color():
    print("HSV: ({}, {}, {})".format(selected_h, selected_s, selected_v))
    r, g, b = hsv2rgb(selected_h, selected_s, selected_v)
    print("RGB: ({}, {}, {})".format(r, g, b))


def on_mouseclick(event, x, y, flags, param):
    global selected_h, selected_s, selected_v
    if event == cv2.EVENT_LBUTTONDBLCLK:
        selected_h, selected_s, v = get_HSV(x, y)
        draw_color()
        print_color()


def on_trackbar(x):
    global selected_v
    selected_v = x
    draw_palette()
    draw_color()


cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('S', window_name, 100, 100, on_trackbar)
cv2.setMouseCallback(window_name, on_mouseclick)
draw_palette()

cv2.waitKey(0)
cv2.destroyAllWindows()