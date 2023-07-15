from PIL import Image
import cv2
import numpy as np

path_picture = "D:\\task\\1.png"
img = cv2.imread(path_picture, cv2.IMREAD_COLOR)
cv2.imshow("test", img)
cv2.waitKey(0)

img_array = np.array(img)
shape = img_array.shape
# print(type(shape)) # <class 'tuple'>
# 这里的shape表示图片的一个维度，以元组的方式进行存储

#print(img_array.shape)
# 这句话的意思是将像素点全部存储在一个数组中（numpy.ndarray)

height = shape[0]
width = shape[1]
# 得到这张照片的长度和宽度,其中height表示行数，width表示列数

dst_rgb = np.zeros((height, width, 3))
# 意思是建立一个0的三维数组，分别存储它的B,G,R像素
# 但是还可以通过dst[height,width]访问这个点的RGB

for h in range(0, height):
    for w in range(0, width):
        dst_rgb[h, w] = img_array[h, w]
# 这段话的意思是将图片中的RGB的像素抠出来进行存储


def trans(r, g, b):
    index = r*0.2989+g*0.5870+b*0.1140
    return index
# 这段话的意思是将RGB的值换算成为灰度


dst_gery = np.zeros((height, width))
# 开辟一个存储灰度的二维数组

for h in range(0, height):
    for w in range(0, width):
        b = dst_rgb[h, w, 0]
        g = dst_rgb[h, w, 1]
        r = dst_rgb[h, w, 2]
        dst_gery[h, w] = trans(r, g, b)
# 这段话的意思是调用函数进行灰度存储
print(dst_gery)
