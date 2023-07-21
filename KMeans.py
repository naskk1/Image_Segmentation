import cv2
import numpy as np
def K_means(filename):
    # 读取图像
    src = cv2.imread(filename)

    # 获取图像的宽度、高度和维数
    width = src.shape[1]
    height = src.shape[0]
    dims = src.shape[2]

    # 定义颜色表
    colorTab = [
        (0,0,0),
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (0, 255, 255),
        (255, 0, 255),
        (255,255,2550),
        (125,125,125),
        (125,0,125),
        (125,125,0)
    ]

    # 将图像像素点转换为样本数据
    sampleCount = width * height
    clusterCount = 5               #参数设置
    points = np.zeros((sampleCount, dims), dtype=np.float32)
    index = 0
    for row in range(height):
        for col in range(width):
         index = row * width + col
         bgr = src[row, col]
         points[index, 0] = int(bgr[0]) # b
         points[index, 1] = int(bgr[1]) # g
         points[index, 2] = int(bgr[2]) # r

    # 调用Kmeans函数进行聚类
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, labels, centers = cv2.kmeans(points, clusterCount, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # 显示图像分割结果
    result = np.zeros(src.shape, dtype=src.dtype)
    index1 = 0
    for row in range(height):
     for col in range(width):
            index1 = row * width + col
            label = labels[index1]
            result[row, col] = colorTab[label[0]]

    pathname=filename.split('.')[0]+'_result.png'
    cv2.imwrite(pathname,result)

'''
cv2.namedWindow("Image Segmentation", cv2.WINDOW_FREERATIO)
cv2.imshow("Input", src)
cv2.imshow("Result", result)
cv2.waitKey(0)
'''
