import cv2 as cv
import numpy as np

#data of image
img_path = 'img/IMG_0325.JPG'
img = cv.imread(img_path)
height,width,channel = img.shape
lowBGR = [71,73,52]
highBGR = [130,121,92]
pixel = np.full((height, width), False)

##generate whiteImage
##img_white = np.ones((height, width, 3), np.uint8) * 255
##img_white.itemset((y,x,0),0)
##img_white.itemset((y,x,1),0)
##img_white.itemset((y,x,2),0)
##cv2.imwrite('./output2.jpg', img_white)


#Access

for y in range(height):
   for x in range(width):
      blue = img.item(y,x,0)
      green = img.item(y,x,1)
      red = img.item(y,x,2)
      if blue >= lowBGR[0] and blue <= highBGR[0] and green >= lowBGR[1] and green <= highBGR[1] and red >= lowBGR[2] and red <= highBGR[2]:
         ##print("座標(%d,%d)は黒板です" % (x,y))
         pixel[y][x] = True