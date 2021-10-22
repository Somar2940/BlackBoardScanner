## This file is package

import cv2
import numpy as np
from PIL import Image

def trans(inimg):
    def cv2pil(image):
        ''' OpenCV型 -> PIL型 '''
        new_image = image.copy()
        if new_image.ndim == 2:  # モノクロ
            pass
        elif new_image.shape[2] == 3:  # カラー
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
        elif new_image.shape[2] == 4:  # 透過
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
        new_image = Image.fromarray(new_image)
        return new_image

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

    # median filter
    img_med = cv2.medianBlur(inimg, ksize=3)

    # putAlphaChanel
    im_rgb = cv2pil(img_med)
    im_rgba = im_rgb.copy()
    im_rgba.putalpha(255)

    # transparent
    img = pil2cv(im_rgba)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerHSV = (50, 0, 0)
    upperHSV = (110,150, 150)
    img_mask = cv2.inRange(hsv, lowerHSV, upperHSV) # 範囲からマスク画像を作成
    img_bool = cv2.bitwise_not(img, img, mask=img_mask)      # 元画像とマスク画像の演算(背景を白くする)

    # オープニング処理処理
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1)) #フィルタ
    # opening = cv2.morphologyEx(img_bool, cv2.MORPH_OPEN, kernel) #オープニング処理

    return img_bool

    # cv2.imwrite('resultImages/transparent_out_open.png', opening)                      # 画像保存