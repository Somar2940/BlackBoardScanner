import numpy as np
from PIL import Image

#imageValues
img_path = 'img/IMG_0325.JPG'
img = Image.open(img_path)
img = img.convert("HSV")
height = img.height
width = img.width
data = img.getdata()
value = list(data)

#Settings
lowHSV = [85,0,0]
highHSV = [100,100,50]

#debug
print(height)
#print(value[1])


im = Image.new("HSV", (width, height))

#黒板ピクセル探索
tmpvalue = ((0,0,0))

listvalue = list(value)

length = len(value)
for i in range(length):
   if value[i][0] >= lowHSV[0] and value[i][0] <= lowHSV[0] and value[i][1] >= lowHSV[0] and value[i][1] <= lowHSV[1] and value[i][2] >= lowHSV[2] and value[i][2] <= lowHSV[2]:
      tmpvalue = tmpvalue + (1, 1, 1)
   #else:
      #tmpvalue = tmpvalue + (1, 128, 128)
   #print(str(i) + "/" + str(length))

#tuplevalue = tuple(tmpvalue)
im.putdata(value)
#print(value)
#im.show()
