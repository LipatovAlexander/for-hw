import cv2
import numpy as np

# Warp an image with a mouse clicking and rotate it with a perspective transformation

img_warp = cv2.imread('cards.jpg')


def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img_warp, (x, y), 3, (255, 255, 0), -1)
        mouseX, mouseY = x, y


cv2.imshow('img_warp', img_warp)
cv2.setMouseCallback('img_warp', draw_circle)

while 1:
    cv2.imshow('img_warp', img_warp)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break

    if k == ord('1'):
        x1 = mouseX, mouseY
        print(x1)
    if k == ord('2'):
        x2 = mouseX, mouseY
        print(x2)
    if k == ord('3'):
        x3 = mouseX, mouseY
        print(x3)
    if k == ord('4'):
        x4 = mouseX, mouseY
        print(x4)
    if k == ord('5'):
        width, height = 250, 350
        pts1 = np.float32([[x1], [x2], [x3], [x4]])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        img_output = cv2.warpPerspective(img_warp, matrix, (width, height))
        cv2.imshow('output', img_output)

cv2.waitKey(0)
cv2.destroyAllWindows()