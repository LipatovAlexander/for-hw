import cv2

img = cv2.imread('hw7.jpg')

cv2.imshow('original',img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Resize an image in OpenCV using different interpolations, and study the differences.

scale_down = 0.6
res_inter_nearest = cv2.resize(img, None, fx=scale_down, fy=scale_down, interpolation=cv2.INTER_NEAREST)
res_inter_linear = cv2.resize(img, None, fx=scale_down, fy=scale_down, interpolation=cv2.INTER_LINEAR)
res_inter_area = cv2.resize(img, None, fx=scale_down, fy=scale_down, interpolation=cv2.INTER_AREA)

cv2.imshow('inter_nearest', res_inter_nearest)
cv2.imshow('inter_linear', res_inter_linear)
cv2.imshow('inter_area', res_inter_area)

cv2.waitKey(0)
cv2.destroyAllWindows()


# Divide the image in patches and saves them to the disk as a patch with serial names

img_copy = img.copy()

img_height = img.shape[0]
img_width = img.shape[1]

patches_count = 2
patch_height = img_height // patches_count
patch_width = img_width // patches_count
x1 = 0
y1 = 0

for y in range(0, img_height, patch_height):
    for x in range(0, img_width, patch_width):
        if (img_height - y) < patch_height or (img_width - x) < patch_width:
            break

        y1 = y + patch_height
        x1 = x + patch_width

        tiles = img_copy[y:y1, x:x1]
        cv2.imwrite('saved_patches/'+'tile'+str(x)+'_'+str(y)+'.jpg', tiles)
        cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)

cv2.imshow('patched', img)
cv2.waitKey(0)
cv2.destroyAllWindows()