import cv2
import numpy as np

image1 = cv2.imread('img/BBS_out.jpg',-1)
image2 = cv2.imread('img/BBS_out.jpg',-1)
image3 = cv2.imread('img/BBS_out2.jpg',-1)

height, width = image1.shape[:2]
img_size = (width, height)

# 画像をリサイズする
image1 = cv2.resize(image1, img_size)
image2 = cv2.resize(image2, img_size)
image3 = cv2.resize(image3, img_size)

lowerHSV = (40, 0, 0)
upperHSV = (110,150, 150)
result = list(range(3))

def Chroma(result, img, n):
   hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   mask = cv2.inRange(hsv, (40, 0, 0), (110,150, 150))
   tmp = cv2.bitwise_not(img, img, mask=mask) # 元画像とマスクを合成
   result.append(tmp)
   cv2.imwrite("resultImages/output" + str(n) + ".jpg", tmp)


Chroma(result, image1, 1)
Chroma(result, image2, 2)
Chroma(result, image3, 3)

print(np.count_nonzero(result[0] == result[1]) / image1.size)
print(np.count_nonzero(result[0] == result[2]) / image1.size)
# 1.0
# 0.46696666666666664