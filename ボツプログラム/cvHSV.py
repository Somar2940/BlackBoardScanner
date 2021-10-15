import cv2
import math
import os
import numpy as np

# 画像のパスを指定
file_path = "img/IMG_0325.JPG"

# 画像が存在するかを確認
if not os.path.exists(file_path):
    print("画像が存在しません。")

# 画像を読み込む
img = cv2.imread(file_path)

# 画像のサイズを変更
height, width = img.shape[:2]
img = cv2.resize(img, (math.floor(width / 2), math.floor(height / 2)))

# HSV形式に変換
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 消去する色をHSV形式で指定
l_green = (0, 0, 0)
h_green = (90, 255, 255)

# 2値化を行う
nichi = cv2.inRange(hsv, l_green, h_green)
nichi = cv2.bitwise_not(nichi)

# 輪郭のみを検出する
cons = cv2.findContours(nichi,
                        cv2.RETR_LIST,
                        cv2.CHAIN_APPROX_NONE)[0]

# 輪郭を描画する
for con in cons:
    # 面積が閾値を超えない場合、輪郭としない
    if cv2.contourArea(con) < 2000:
        continue

    # 描画処理
    cv2.polylines(img, con, True, (255, 0, 0), 5)

cv2.imshow("result", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()