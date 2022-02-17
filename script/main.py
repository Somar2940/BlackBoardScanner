## How to execution this Script
## (ex)$ python3.7 main.py 5 TE left
### argv[1] is "grade"
### argv[2] is "class"
### argv[3] is "Initial direction of motor"

import sys
import time
import math
import io
import os
from datetime import datetime as dt
import re
import glob
import picamera

import cv2
import numpy as np
import RPi.GPIO as GPIO

import transparent
import homography

# /dev/video0を指定
DEV_ID = 0

# 実行開始時間
START_TIME = time.time()
END_TIME_SECOND = 60 * 20 #(秒)

# imgfileのsort
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

# 画像保存先ディレクトリ作成orリスト読み込み
tdatetime = dt.now()
tstr = tdatetime.strftime('%Y%m%d')
IMG_DIR = "/home/pi/BBSproject/static/mainImg/" + tstr + "/" + sys.argv[1] + "/" + sys.argv[2] + "/"

if not os.path.isdir(IMG_DIR + "left"):
   os.makedirs(IMG_DIR + "left")
   left_imgs = []
else:
   left_imgs = [os.path.basename(r) for r in sorted(glob.glob(IMG_DIR + "left/*.png"), key=natural_keys)]

if not os.path.isdir(IMG_DIR + "right"):
   os.makedirs(IMG_DIR + "right")
   right_imgs = []
else:
   right_imgs = [os.path.basename(r) for r in sorted(glob.glob(IMG_DIR + "right/*.png"), key=natural_keys)]

# 初期のモータ方向
Direction = sys.argv[3]

# カメラセットアップ
CAMERA_WIDTH = 3200
CAMERA_HEIGHT = 2400
stream = io.BytesIO()
camera = picamera.PiCamera()
camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)

# モータセットアップ
GPIO.setmode(GPIO.BCM)
PIN = [4, 17] # 4→y方向 17→x方向
servo = []
for i in range(2):
   GPIO.setup(PIN[i], GPIO.OUT)
   servo.append(GPIO.PWM(PIN[i], 50))
   servo[i].start(0.0)

def degree2float(degree):
   # -90~90
   dc = 2.5 + (12.0-2.5)/180*(degree+90)
   return dc

def servo_angle_x(angle):
   servo[1].ChangeDutyCycle(degree2float(0.0))
   time.sleep(0.1)
   if angle == "left":
      for degree in range(0, 31):
         servo[1].ChangeDutyCycle(degree2float(degree))
         time.sleep(0.01)
         servo[1].ChangeDutyCycle(0.0)
      servo[1].ChangeDutyCycle(8.891) # 8.891388
   elif angle == "right":
      for degree in range(0, -31, -1):
         servo[1].ChangeDutyCycle(degree2float(degree))
         time.sleep(0.01)
         servo[1].ChangeDutyCycle(0.0)
      servo[1].ChangeDutyCycle(5.609) # 5.608611
   else:
      pass
   time.sleep(1.5)
   servo[1].ChangeDutyCycle(0.0)
   

def image_process(direction):
   camera.capture(stream, format='jpeg')
   data = np.fromstring(stream.getvalue(), dtype=np.uint8)
   cap_img = cv2.imdecode(data, 1)
   stream.seek(0)
   stream.truncate()
   homoImage =  homography.homo(cap_img, direction)
   # 左右にmargin
   height, width = homoImage.shape[:2]
   ydst_up = int(height*0.04)
   ydst_un = int(height*0.07)
   xdst = int(width*0.02)
   if direction == "left":
       output = homoImage[ydst_un:(height-ydst_up), xdst:width, :]
   elif direction == "right":
       output = homoImage[ydst_un:(height-ydst_up), 0:(width-xdst), :]
   else:
       output = homoImage[ydst_un:(height-ydst_up), xdst:(width-xdst), :]
   return output 

def Mobility_calc(img1, img2, img3):
   gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
   gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
   gray3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
   diff1 = cv2.absdiff(gray1, gray2)
   diff2 = cv2.absdiff(gray2, gray3)
   diff_and = cv2.bitwise_and(diff1, diff2)
   _, diff_wb = cv2.threshold(diff_and, 30, 255, cv2.THRESH_BINARY)
   diff = cv2.medianBlur(diff_wb, 5)
   cnt = cv2.countNonZero(diff)
   return cnt

def match_ratio_calc(img1, img2):
   gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
   gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
   hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
   hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
   match_ratio = cv2.compareHist(hist1, hist2, 0)
   return match_ratio

# main
cap_img_count = 0
final_break_flag = False
while True:
   break_flag = False
   servo_angle_x(angle = Direction)

   while True:
      scan_img1 = image_process(Direction)
      time.sleep(0.3)
      scan_img2 = image_process(Direction)
      time.sleep(0.3)
      scan_img3 = image_process(Direction)
      print('point "one"')
      # 人がいないか
      mobility = Mobility_calc(scan_img1, scan_img2, scan_img3)
      print(mobility)
      if mobility <= 50: #閾値
         print('point "three"')
         trans_img = transparent.trans(scan_img3)
         # 黒板になにか書かれているか
         image_size = trans_img.size / 4
         text_pixel_count = cv2.countNonZero(trans_img[:,:,3])
         text_pixel_ratio = (text_pixel_count/image_size)
         print("text_pixel_ratio:" + str(text_pixel_ratio))
         if text_pixel_ratio >= 0.01:
            break_flag = True
            print('point "four"')
         else:
            pass
      else:
         print('point "two"')
         pass

      # while break point
      if break_flag:
         break

      # もう一度カメラ撮影からやり直し
      time.sleep(10)
      if (time.time() - START_TIME) > (END_TIME_SECOND):
         final_break_flag = True
         break

   if final_break_flag:
      break

   # 新しい画像か
   if cap_img_count <= 1:
      if (Direction == "left"):
         new_filename = str(len(left_imgs)+1) + ".png"
         cv2.imwrite(IMG_DIR + "left/" + new_filename, scan_img3)
         print(IMG_DIR + "left/" + new_filename)
         left_imgs.append(new_filename)
      elif (Direction == "right"):
         new_filename = str(len(right_imgs)+1) + ".png"
         print(IMG_DIR + "right/" + new_filename)
         cv2.imwrite(IMG_DIR + "right/" + new_filename, scan_img3)
         right_imgs.append(new_filename)
   else:
      # リストから前回の画像を取得
      if Direction == "left":
         before_img = cv2.imread(IMG_DIR + "left/" + str(left_imgs[-1]))
         if match_ratio_calc(before_img, trans_img) >= 0.95:
            print(match_ratio_calc(before_img, trans_img))
            new_filename = str(len(left_imgs)+1) + ".png"
            cv2.imwrite(IMG_DIR + "left/" + new_filename, scan_img3)
            print(IMG_DIR + "left/" + new_filename)
            left_imgs.append(new_filename)
         else:
            time.sleep(10)
            print('point "six" of left')
      elif Direction == "right":
         before_img = cv2.imread(IMG_DIR + "right/" + str(right_imgs[-1]))
         if match_ratio_calc(before_img, trans_img) >= 0.95:
            print(match_ratio_calc(before_img, trans_img))
            new_filename = str(len(right_imgs)+1) + ".png"
            cv2.imwrite(IMG_DIR + "right/" + new_filename, scan_img3)
            print(IMG_DIR + "right/" + new_filename)
            right_imgs.append(new_filename)
         else:
            time.sleep(10)
            print('point "six" of right')

   if (time.time() - START_TIME) > (END_TIME_SECOND):
      break

   # 現在のサーボの向きを反転して保存
   if Direction == "left":
      Direction = "right"
   elif Direction == "right":
      Direction = "left"

   cap_img_count = cap_img_count + 1

servo[1].stop()
GPIO.cleanup()
