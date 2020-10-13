#coding:utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def img2gray(img):
    GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_BINARY_INV)
    ret, thresh3 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_TRUNC)
    ret, thresh4 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_TOZERO)
    ret, thresh5 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_TOZERO_INV)
    titles = ['Gray Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
    images = [GrayImage, thresh1, thresh2, thresh3, thresh4, thresh5]
    for i in xrange(6):
        plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    # plt.show()
    return thresh2

def draw_round(img,max_radius,min_radius):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图像
    plt.subplot(121), plt.imshow(gray, 'gray')
    plt.xticks([]), plt.yticks([])
    circles1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=1, minRadius=min_radius, maxRadius=max_radius)
    if circles1 is None:
        print "pass~ thowned image~"
    else :
        print "222"
        circles_real = circles1
        circles = circles_real[0, :, :]  # 提取为二维
        circles = np.uint16(np.around(circles))  # 四舍五入，取整
        for i in circles[:]:
            cv2.circle(img, (i[0], i[1]), i[2], (255, 0, 0), 1)  # 画圆
            # cv2.circle(img, (i[0], i[1]), 2, (255, 0, 255), 10)  # 画圆心
            # 圆心坐标（i[0],i[1]）
            # 半径 i[2]
            # 第三个参数，颜色数组。第四个参数，线宽。
        plt.subplot(122), plt.imshow(img)
        plt.xticks([]), plt.yticks([])
        cv2.imshow('img',img)
        cv2.waitKey(0)
def draw_cut_round(img,max_radius,min_radius):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图像
    plt.subplot(121), plt.imshow(gray, 'gray')
    plt.xticks([]), plt.yticks([])
    circles1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=1, minRadius=min_radius, maxRadius=max_radius)
    if circles1 is None:
        print "pass~ thowned image~"
    else :
        print "222"
        circles_real = circles1
        circles = circles_real[0, :, :]  # 提取为二维
        circles = np.uint16(np.around(circles))  # 四舍五入，取整
        #print circles
        for i in circles[:]:
            cv2.circle(img, (i[0], i[1]), i[2], (255, 0, 0), 1)  # 画圆
            # cv2.circle(img, (i[0], i[1]), 2, (255, 0, 255), 10)  # 画圆心
            # 圆心坐标（i[0],i[1]）
            # 半径 i[2]
            # 第三个参数，颜色数组。第四个参数，线宽。
            img_deal(img,i[0],i[1],i[2])
def img_deal(img,x,y,d):
    # cv2.IMREAD_COLOR，读取BGR通道数值，即彩色通道，该参数为函数默认值
    # cv2.IMREAD_UNCHANGED，读取透明（alpha）通道数值
    # cv2.IMREAD_ANYDEPTH，读取灰色图，返回矩阵是两维的
    #img = cv2.imread(input_img, cv2.IMREAD_UNCHANGED)
    rows, cols, channel = img.shape

    # 创建一张4通道的新图片，包含透明通道，初始化是透明的
    img_new = np.zeros((rows,cols,4),np.uint8)
    img_new[:,:,0:3] = img[:,:,0:3]

    # 创建一张单通道的图片，设置最大内接圆为不透明，注意圆心的坐标设置，cols是x坐标，rows是y坐标
    img_circle = np.zeros((rows,cols,1),np.uint8)
    img_circle[:,:,:] = 0  # 设置为全透明
    img_circle = cv2.circle(img_circle,(x,y),d,(255),-1) # 设置最大内接圆为不透明

    # 图片融合
    img_new[:,:,3] = img_circle[:,:,0]

    # 保存图片
    # datadir = 'p19_cut'
    # cv2.imwrite(datadir+img, img_new)
    # cv2.imencode('.jpg', img)[1].tofile('./9.jpg')  # 保存到另外的位置

    # 显示图片，调用opencv展示
    # cv2.imshow("img_new", img_new)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 显示图片，调用matplotlib.pyplot展示
    plt.subplot(121), plt.imshow(img_convert(img), cmap='gray'), plt.title('IMG')
    plt.subplot(122), plt.imshow(img_convert(img_new), cmap='gray'), plt.title('IMG_NEW')
    # plt.plot(), plt.imshow(img_convert(img_new), cmap='gray'), plt.title('IMG_NEW')
    plt.show()
def img_convert(cv2_img):
    # 灰度图片直接返回
    if len(cv2_img.shape) == 2:
        return cv2_img
    # 3通道的BGR图片
    elif len(cv2_img.shape) == 3 and cv2_img.shape[2] == 3:
        b, g, r = cv2.split(cv2_img)
        return cv2.merge((r, g, b))
    # 4通道的BGR图片
    elif len(cv2_img.shape) == 3 and cv2_img.shape[2] == 4:
        b, g, r, a = cv2.split(cv2_img)
        return cv2.merge((r, g, b, a))
    # 未知图片格式
    else:
        return cv2_img


datadir = 'p19'
for i in os.listdir(datadir):
    img_path = os.path.join(datadir, i)
    print img_path
    img_rgb = cv2.imread(img_path)
    max_radius = max((img_rgb.shape)[0], (img_rgb.shape)[1])
    min_radius = int(0.25 * min((img_rgb.shape)[0], (img_rgb.shape)[1]))
    img_gray_1 = img2gray(img_rgb)
    img_gray = cv2.cvtColor(img_gray_1,cv2.COLOR_GRAY2RGB)
    #draw_round(img_gray,max_radius,min_radius)  # 使用灰度图画圆
    #draw_round(img_rgb,max_radius,min_radius)  # 使用rgb图画圆
    draw_cut_round(img_gray,max_radius,min_radius)  # 使用灰度图画圆并裁剪
    #draw_cut_round(img_rgb, max_radius, min_radius)  # 使用rgb图画圆并裁剪




# img = cv2.imread('./p19/p19_206.jpg')
# print (img.shape)[0]
# print (img.shape)[1]
# max = max((img.shape)[0],(img.shape)[1])
# min = int(0.25*min((img.shape)[0],(img.shape)[1]))
# draw_round(img,max,min)


