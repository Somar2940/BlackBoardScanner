import cv2
import numpy as np

image1 = cv2.imread('img/IMG_0653.jpg',-1)
image2 = cv2.imread('img/IMG_0653.jpg',-1)
image3 = cv2.imread('img/IMG_0654.jpg',-1)

height, width = image1.shape[:2]
img_size = (width, height)

# 画像をリサイズする
image1 = cv2.resize(image1, img_size)
image2 = cv2.resize(image2, img_size)
image3 = cv2.resize(image3, img_size)

image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
image3_gray = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)

# 画像をヒストグラム化する
image1_hist = cv2.calcHist([image1_gray], [0], None, [256], [0, 256])
image2_hist = cv2.calcHist([image2_gray], [0], None, [256], [0, 256])
image3_hist = cv2.calcHist([image3_gray], [0], None, [256], [0, 256])

# ヒストグラムした画像を比較
print(cv2.compareHist(image1_hist, image2_hist, 0))
print(cv2.compareHist(image1_hist, image3_hist, 0))

# 1.0
# 0.936233972590098