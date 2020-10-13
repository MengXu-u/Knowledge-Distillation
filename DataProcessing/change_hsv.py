# -*- coding=utf-8 -*-
import  cv2
import numpy as np
from matplotlib import pyplot

img=cv2.imread('hw.jpg')
#cv2.imshow('img',img)
rows,cols,channels=img.shape
#H = Hue[0,180) , 
#S = Saturation[0,256) , 
#V = Value[0,256)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
def ch_hue(img_hsv):#改变色调
	hue_num = input("input a num to add the hue:\n")
	turn_green_hsv = img_hsv.copy()
	print (turn_green_hsv[:,:,0])
	turn_green_hsv[:, :, 0] = (turn_green_hsv[:, :, 0]+hue_num) % 180
	turn_green_img = cv2.cvtColor(turn_green_hsv, cv2.COLOR_HSV2BGR)
	cv2.imwrite('turn_green.jpg', turn_green_img)
def ch_value(img_hsv):#改变明度
	value_proportion = input("input a num to multiple the value:\n")
	darker_hsv = img_hsv.copy()
	darker_hsv[:, :, 2] = value_proportion * darker_hsv[:, :, 2]
	darker_img = cv2.cvtColor(darker_hsv, cv2.COLOR_HSV2BGR)
	cv2.imwrite('darker.jpg', darker_img)
def ch_saturation(img_hsv):#改变饱和度
	saturation_proportion = input("input a num to multiple the saturation:\n")
	colorless_hsv = img_hsv.copy()
	colorless_hsv[:, :, 1] = saturation_proportion * colorless_hsv[:, :, 1]
	colorless_img = cv2.cvtColor(colorless_hsv, cv2.COLOR_HSV2BGR)
	cv2.imwrite('colorless.jpg', colorless_img)
def merge_ch_hsv(img_hsv):
	img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float)
	hue_delta = input("hue_delta:(input 0 if not to change)\t")
	sat_mult = input("sat_mult:(input 1 if not to change)\t")
	val_mult = input("val_mult:(input 1 if not to change)\t")
	img_hsv[:, :, 0] = (img_hsv[:, :, 0] + hue_delta) % 180
	img_hsv[:, :, 1] *= sat_mult
	img_hsv[:, :, 2] *= val_mult
	img_hsv[img_hsv > 255] = 255
	merge_img = cv2.cvtColor(np.round(img_hsv).astype(np.uint8), cv2.COLOR_HSV2BGR)
	cv2.imwrite('merge_ch_img.jpg',merge_img)
def histogram_equalization(img):
	print ("saved the histogram_equalization of img")
	img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
	img_hsv[:,:,0]=cv2.equalizeHist(img_hsv[:,:,0])
	img_bgr=cv2.cvtColor(img_hsv,cv2.COLOR_YUV2BGR)
	cv2.imwrite('img_equ.jpg', img_bgr)

#ch_hue(img_hsv)
#ch_value(img_hsv)
#ch_saturation(img_hsv)
merge_ch_hsv(img_hsv)
histogram_equalization(img)
