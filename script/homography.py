## This file is package

import cv2
import numpy as np
import csv
import math

def homo(img, direction):
   def_height, def_width = img.shape[:2]
   with open('vertices_' + str(direction) + '.csv', 'r') as file:
      reader = csv.reader(file)
      vertices = [ [int(j) for j in i] for i in reader ]

   outputHeight = 1000 #処理後画像の横方向画素数
   def get_distance(x1,y1,x2,y2):
      distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
      return distance

   def get_aspectRatio(array):
      #4つの辺の長さを取得
      height1 = get_distance(array[0][0],array[0][1],array[1][0],array[1][1])
      height2 = get_distance(array[2][0],array[2][1],array[3][0],array[3][1])
      width1 = get_distance(array[0][0],array[0][1],array[2][0],array[2][1])
      width2 = get_distance(array[1][0],array[1][1],array[3][0],array[3][1])

      #平均を計算
      heightRatio = (height1+height2) / 2
      widthRatio = (width1+width2) / 2

      #アスペクト比を少数で取得し返り値として指定
      aspectRatio = widthRatio / heightRatio
      return aspectRatio

   aspectRatio = get_aspectRatio(vertices)
   outputWidth = int(outputHeight*aspectRatio)

   pts1 = np.float32(vertices)
   pts2 = np.float32([[0,0],[0,outputHeight],[outputWidth,0],[outputWidth,outputHeight]])

   M = cv2.getPerspectiveTransform(pts1,pts2) #透視変換の行列を求める
   homoImage = cv2.warpPerspective(img,M,(outputWidth,outputHeight)) #変換行列を用いて画像の透視変換

   return homoImage
