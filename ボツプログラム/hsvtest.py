import numpy as np
import cv2 as cv

img_path = 'img/IMG_0325.JPG'
img = cv.imread(img_path)
height,width,channel = img.shape
lowHSV = [85,0,0]
highHSV = [100,100,50]
pixel = np.full((height, width), False)

#generate whiteImage
img_white = np.ones((height, width, 3), np.uint8) * 255


def hsv_to_rgb(h, s, v):
    bgr = cv.cvtColor(np.array([[[h, s, v]]], dtype=np.uint8), cv.COLOR_HSV2BGR)[0][0]
    return (bgr[2], bgr[1], bgr[0])


def rgb_to_hsv(r, g, b):
    hsv = cv.cvtColor(np.array([[[b, g, r]]], dtype=np.uint8), cv.COLOR_BGR2HSV)[0][0]
    return (hsv[0], hsv[1], hsv[2])


for y in range(height):
   for x in range(width):
      blue = img.item(y,x,0)
      green = img.item(y,x,1)
      red = img.item(y,x,2)
      hue, saturation, brightness = rgb_to_hsv(red, green, blue)
      #print(str(hue) + "," + str(saturation) + "," + str(brightness))
      if lowHSV[0] <= hue and hue <= highHSV[0] and lowHSV[1] <= saturation and saturation <= highHSV[1]:
         img_white.itemset((y,x,0),0)
         img_white.itemset((y,x,1),0)
         img_white.itemset((y,x,2),0)
   print(str(y) + "/" + str(height))
cv.imwrite('./hsvtest_out.jpg', img_white)