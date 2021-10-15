import cv2 as cv
import numpy as np

#data of image
img_file = 'img/IMG_0325.JPG'
img = cv.imread(img_file, cv.IMREAD_COLOR)
img_copy = img.copy()
height,width,channel = img.shape
lowBGR = [71,73,52]
highBGR = [130,121,92]
##pixel = np.full((imgSizey, imgSizex), False)

##generate whiteImage
img_white = np.ones((height, width, 3), np.uint8) * 255
##img_white.itemset((y,x,0),0)
##img_white.itemset((y,x,1),0)
##img_white.itemset((y,x,2),0)


#Access
img[(img[:,:,0]>=71) & (img[:,:,0]<=130) & (img[:,:,1]>=73) & (img[:,:,1]<=121) & (img[:,:,2]>=52) & (img[:,:,2]<=92)] = 0
img[~((img[:,:,0]==0) & (img[:,:,1]==0) & (img[:,:,2]==0))] = 255
img_gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
retval, dst = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
# 輪郭を抽出
dst, contours, hierarchy = cv.findContours(dst, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# この時点での状態をデバッグ出力
dst = cv.imread(img_copy, cv.IMREAD_COLOR)
dst = cv.drawContours(dst, contours, -1, (0, 0, 255, 255), 2, cv.LINE_AA)
cv.imwrite('debug_1.png', dst)
##cv.imwrite('./output3.jpg', img)