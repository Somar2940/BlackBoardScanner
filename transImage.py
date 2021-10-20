import cv2
import transparent
import homography

img_path = 'img/IMG_0326.JPG'
img = cv2.imread(img_path)

homoImage = homography.homo(img)
output = transparent.trans(homoImage)

cv2.imwrite('resultImages/trans_out.png', output)