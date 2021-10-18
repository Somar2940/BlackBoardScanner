import cv2
import numpy as np
from PIL import Image, ImageFilter

#putAlphaChanel
im_rgb = Image.open('img/testBBimg.JPG')
im_rgba = im_rgb.copy()
im_rgba.putalpha(255)

def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


#Transparent
#img = cv2.imread(img_rgba, -1)                       	# -1はAlphaを含んだ形式(0:グレー, 1:カラー)
img = pil2cv(im_rgba)
color_lower = np.array([89, 95, 95, 255])                 # 抽出する色の下限(BGR形式)
color_upper = np.array([182, 188, 194, 255])              # 抽出する色の上限(BGR形式)
img_mask = cv2.inRange(img, color_lower, color_upper)    # 範囲からマスク画像を作成
img_bool = cv2.bitwise_not(img, img, mask=img_mask)      # 元画像とマスク画像の演算(背景を白くする)

#cv2.imwrite('orange_out.png', img_bool)                      # 画像保存
cv2.imshow("output", img_bool)
cv2.waitKey(0)
cv2.destroyAllWindows()