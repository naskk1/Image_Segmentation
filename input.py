import cv2
# 输入

path_picture = "D:\\task\\1.png"
img = cv2.imread(path_picture,cv2.IMREAD_GRAYSCALE)
cv2.namedWindow("Input")
cv2.imshow("Input", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("D:\\task\\2.png",img)
