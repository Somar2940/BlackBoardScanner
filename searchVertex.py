import cv2
import numpy as np
import csv

img_path = 'img/IMG_0653.JPG'
img = cv2.imread(img_path)
height, width = img.shape[:2]

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# HSV閾値設定
lowerHSV = (50, 0, 0)
upperHSV = (110,150, 150)
bin_img = cv2.inRange(hsv_img, lowerHSV, upperHSV)

# クロージング処理
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25)) #フィルタ
cls_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)

# 輪郭を生成
contours, hierarchy = cv2.findContours(cls_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
con = list(filter(lambda x: cv2.contourArea(x) > (height*width/5), contours)) #面積閾値設定

# 輪郭近似
approx_contours = []
for i, cnt in enumerate(con):
    # 輪郭の周囲の長さを計算する。
    arclen = cv2.arcLength(cnt, True)
    # 輪郭を近似する。
    n = 1
    while True:
        approx_cnt = cv2.approxPolyDP(cnt, epsilon=n * 0.01 * arclen, closed=True)
        n += 1
        if len(approx_cnt) == 4:
            break
        if len(approx_cnt) < 4:
            n -= 0.4

# 次元を減らして要素をsort
approx_cnt = np.squeeze(approx_cnt)

# sort後の順番:左上→左下→右上→右下
approx_cnt_sort = approx_cnt[np.argsort(approx_cnt[:, 0])]
if approx_cnt_sort[0][1] > approx_cnt_sort[1][1]:
    approx_cnt_sort = approx_cnt_sort[[1,0,2,3], : ]
if approx_cnt_sort[2][1] > approx_cnt_sort[3][1]:
    approx_cnt_sort = approx_cnt_sort[[0,1,3,2], : ]


# 4頂点の座標をcsvファイルとして保存
# print(approx_cnt_sort)
with open('vertices.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(approx_cnt_sort)