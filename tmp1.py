import cv2
import numpy as np

img = cv2.imread("blue.png")
cv2.imshow("blue", img)
rows, cols, channels = img.shape
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow("blue_to_red_hsv", hsv)
lower_blue = np.array([90, 70, 70])
upper_blue = np.array([110, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
cv2.imshow("blue_to_red_mask", mask)
# 腐蚀膨胀
erode = cv2.erode(mask, None, iterations=1)
dilate = cv2.dilate(erode, None, iterations=1)
for i in range(rows):
    for j in range(cols):
        if dilate[i, j] == 255:  # 像素点为255表示的是白色，我们就是要将白色处的像素点，替换为红色
            img[i, j] = (0, 0, 255)  # 此处替换颜色，为BGR通道，不是RGB通道
# 窗口等待的命令，0表示无限等待
cv2.imshow("red", img)
cv2.waitKey(0)