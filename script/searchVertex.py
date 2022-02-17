## How to execution this Script
## (ex)$ python3.7 searchVertex.py left
### argv[1] is "direction"

import sys
import io
import time

import csv
import picamera
import RPi.GPIO as GPIO

import cv2
import numpy as np

# モータセットアップ
def degree2float(degree):
    # -90~90
    dc = 2.5 + (12.0-2.5)/180*(degree+90)
    return dc

GPIO.setmode(GPIO.BCM)
PIN = [4, 17] # 4→y方向 17→x方向
servo = []
for i in range(2):
   GPIO.setup(PIN[i], GPIO.OUT)
   servo.append(GPIO.PWM(PIN[i], 50))
   servo[i].start(0.0)

servo[1].ChangeDutyCycle(degree2float(0.0))
time.sleep(0.1)
if sys.argv[1] == "left":
    for degree in range(0, 31):
        servo[1].ChangeDutyCycle(degree2float(degree))
        time.sleep(0.01)
        servo[1].ChangeDutyCycle(0.0)
    servo[1].ChangeDutyCycle(8.891) # 8.891388
elif sys.argv[1] == "right":
    for degree in range(0, -31, -1):
        servo[1].ChangeDutyCycle(degree2float(degree))
        time.sleep(0.01)
        servo[1].ChangeDutyCycle(0.0)
    servo[1].ChangeDutyCycle(5.609) # 5.608611
else:
    pass
time.sleep(1)
servo[1].ChangeDutyCycle(0.0)
servo[1].stop()
GPIO.cleanup()

# 画像パラメータ
CAMERA_WIDTH = 3200
CAMERA_HEIGHT = 2400

# カメラセットアップ
stream = io.BytesIO()
camera = picamera.PiCamera()
camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
camera.capture(stream, format='jpeg')
data = np.fromstring(stream.getvalue(), dtype=np.uint8)
img = cv2.imdecode(data, 1)
height = CAMERA_HEIGHT
width = CAMERA_WIDTH

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# HSV閾値設定
lowerHSV = (50, 0, 0)
upperHSV = (110,150, 150)
bin_img = cv2.inRange(hsv_img, lowerHSV, upperHSV)
## cv2.imwrite('resultImages/slide1.jpg', bin_img)

## クロージング処理
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25)) ## フィルタ
cls_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)
## cv2.imwrite('resultImages/slide2.jpg', cls_img)

## 輪郭を生成
contours, hierarchy = cv2.findContours(cls_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
con = list(filter(lambda x: cv2.contourArea(x) > (height*width/5), contours)) ## 面積閾値設定

## output3 = img.copy()
## output3 = cv2.drawContours(output3, con, -1, (0,255,0), 20)
## cv2.imwrite('resultImages/slide3.jpg', output3)

## 輪郭近似
for i, cnt in enumerate(con):
    ## 輪郭の周囲の長さを計算する。
    arclen = cv2.arcLength(cnt, True)
    ## 輪郭を近似する。
    n = 1
    while True:
        approx_cnt = cv2.approxPolyDP(cnt, epsilon=n * 0.01 * arclen, closed=True)
        if len(approx_cnt) == 4:
            break
        elif len(approx_cnt) < 4:
            n -= -0.8
        else:
            n += 1

## 次元を減らして要素をsort
approx_cnt = np.squeeze(approx_cnt)
## sort後の順番:左上→左下→右上→右下
approx_cnt_sort = approx_cnt[np.argsort(approx_cnt[:, 0])]
if approx_cnt_sort[0][1] > approx_cnt_sort[1][1]:
    approx_cnt_sort = approx_cnt_sort[[1,0,2,3], : ]
if approx_cnt_sort[2][1] > approx_cnt_sort[3][1]:
    approx_cnt_sort = approx_cnt_sort[[0,1,3,2], : ]

## output4 = img.copy()
## output4 = cv2.line(output4, (415, 613), (408, 1780), (0, 255, 0), thickness=30, lineType=cv2.LINE_4, shift=0)
## output4 = cv2.line(output4, (415, 613), (4031, 0), (0, 255, 0), thickness=30, lineType=cv2.LINE_4, shift=0)
## output4 = cv2.line(output4, (4031, 0), (4031, 1488), (0, 255, 0), thickness=30, lineType=cv2.LINE_4, shift=0)
## output4 = cv2.line(output4, (408, 1780), (4031, 1488), (0, 255, 0), thickness=30, lineType=cv2.LINE_4, shift=0)
##cv2.imwrite('resultImages/slide4.jpg', output4)


## 4頂点の座標をcsvファイルとして保存
## print(approx_cnt_sort)
with open('vertices_' + sys.argv[1] + '.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(approx_cnt_sort)
