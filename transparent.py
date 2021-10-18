import cv2
import numpy as np

lowerRGB = (95,95,89)
upperRGB = (194,188,182)

img = cv2.imread('img/IMG_0636.jpg',-1)
rgba = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

img_mask = cv2.inRange(img, lowerRGB, upperRGB)    # 範囲からマスク画像を作成
img_bool = cv2.bitwise_not(img, img, mask=img_mask)      # 元画像とマスク画像の演算(背景を白くする)

cv2.imwrite("resultImages/out_transparent.png", img_bool)