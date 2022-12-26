import cv2

img_map = cv2.imread('map.png')


def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img_map, (x, y), 3, (255, 255, 0), -1)
        if 'mouseX' in globals() and 'mouseY' in globals():
            cv2.line(img_map, (mouseX, mouseY), (x, y), (255, 255, 0), thickness=3, lineType=cv2.LINE_AA)
        cv2.imshow('map', img_map)
        mouseX, mouseY = x, y


cv2.imshow('map', img_map)
cv2.setMouseCallback('map', draw_circle)

cv2.waitKey(0)
cv2.destroyAllWindows()