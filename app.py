## How to execution this Script
## (ex)$ python3.7 5 TE left
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

# 画像パラメータ
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# 実行開始時間
START_TIME = time.time()
END_TIME_SECOND = 60 * 90 #(秒)

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

def servo_angle_x(angle):
   if angle == "left":
      servo[1].ChangeDutyCycle(8.891) # 8.891388
   elif angle == "right":
      servo[1].ChangeDutyCycle(5.609) # 5.608611
   else:
      pass
   time.sleep(0.5)

def image_process():
   camera.capture(stream, format='jpeg')
   data = np.fromstring(stream.getvalue(), dtype=np.uint8)
   img = cv2.imdecode(data, 1)
   homo_image = homography.homo(img)
   return homo_image

def match_ratio_calc(img1, img2):
   gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
   gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
   img_hist_1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
   img_hist_2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
   return cv2.compareHist(img_hist_1, img_hist_2, 0)

# main
cap_img_count = 0
final_break_flag = False
while True:
   break_flag = False
   servo_angle_x(angle = Direction)

   while True:
      output1_img = image_process()
      time.sleep(5)
      output2_img = image_process()
      # 人がいるか
      match_ratio = match_ratio_calc(output1_img, output2_img)
      if match_ratio >= 0.95: #閾値
         trans_img = transparent(output2_img)
         # 黒板になにか書かれているか
         image_size = trans_img.size / 4
         text_pixel_count = cv2.countNonZero(trans_img[:,:,3])
         text_pixel_ratio = (text_pixel_count/image_size)
         if text_pixel_ratio >= 0.015:
            break_flag = True
         else:
            pass
      else:
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
         cv2.imwrite(IMG_DIR + "left/" + new_filename)
         left_imgs.append(new_filename)
      elif (Direction == "right"):
         new_filename = str(len(right_imgs)+1)
         cv2.imwrite(IMG_DIR + "right/" + new_filename)
         right_imgs.append(new_filename)
   else:
      # リストから前回の画像を取得
      if Direction == "left":
         before_img = cv2.imread(IMG_DIR + "left/" + str(left_imgs[-1]))
         if match_ratio_calc(before_img, trans_img) >= 0.95:
            new_filename = str(len(left_imgs)+1)
            cv2.imwrite(IMG_DIR + "left/" + new_filename)
            left_imgs.append(new_filename)
         else:
            time.sleep(10)
      elif Direction == "right":
         before_img = cv2.imread(IMG_DIR + "right/" + str(right_imgs[-1]))
         if match_ratio_calc(before_img, trans_img) >= 0.95:
            new_filename = str(len(right_imgs)+1)
            cv2.imwrite(IMG_DIR + "right/" + new_filename)
            right_imgs.append(new_filename)
         else:
            time.sleep(10)

   if (time.time() - START_TIME) > (END_TIME_SECOND):
      break

   # 現在のサーボの向きを反転して保存
   if Direction == "left":
      Direction = "right"
   elif Direction == "right":
      Direction == "left"

   cap_img_count = cap_img_count + 1