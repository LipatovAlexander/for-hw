import cv2
import numpy as np

video = cv2.VideoCapture('video.mp4')
if not video.isOpened():
    print("error opening")

while video.isOpened():
    ret, current_frame = video.read()
    if ret:
        height, width = current_frame.shape[:2]
        pts1 = np.float32([[0, 320], [852, 320], [0, 480], [852, 480]])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        out_frame = cv2.warpPerspective(current_frame, matrix, (width, height))
        cv2.imshow("original", current_frame)
        cv2.imshow("out", out_frame)

        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
    else:
        break

video.release()
cv2.destroyAllWindows()