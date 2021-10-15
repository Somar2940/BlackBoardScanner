import cv2
import numpy as np

image1 = cv2.imread('img/IMG_0326.JPG')
image2 = cv2.imread('img/IMG_0326.JPG')
image3 = cv2.imread('img/IMG_0327.JPG')

height, width = image1.shape[:2]
img_size = (height, width)

# 画像をリサイズする
image1 = cv2.resize(image1, img_size)
image2 = cv2.resize(image2, img_size)
image3 = cv2.resize(image3, img_size)

print(np.count_nonzero(image1 == image2) / image1.size)
print(np.count_nonzero(image1 == image3) / image1.size)
# 1.0
# 0.46696666666666664