# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1x-Nhmw6PRiF9VmKp0PND6R7w9YsZB0vI
"""

import cv2  #importinf computer vision library
import PIL  # python imaging library
import numpy as np #numerical operations
from matplotlib import pyplot as plt    #visualization library in Python for 2D plots of
from PIL import Image                   #opening, rotating and displaying an image
from matplotlib import image as npimg   #Image read and Image show function

img=Image.open("8.jpeg")
plt.imshow(img)

print(img.format)
print(img.size)
print(img.mode)

img=np.array(img)
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

plt.imshow(gray,cmap='gray')

_,threshold=cv2.threshold(gray,110,255,cv2.THRESH_BINARY_INV)

plt.imshow(threshold, cmap= 'gray')

#Different kernel matrices for morphological operations.
kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(4,4))
kernelo=cv2.getStructuringElement(cv2.MORPH_RECT,(6,6))
kernelc=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

#Dilation on threshold image output

dilated=cv2.dilate(threshold,kernel, iterations=3)

plt.imshow(dilated,cmap='gray')

#connecntion of disjoing edges in the shape.
closed=cv2.morphologyEx(dilated,cv2.MORPH_CLOSE,kernelc, iterations=3)

plt.imshow(closed,cmap='gray')

opening=cv2.morphologyEx(closed,cv2.MORPH_OPEN,kernelo,iterations=2)

thinned = cv2.ximgproc.thinning(opening)
plt.imshow(thinned,cmap='gray')

plt.imshow(opening,cmap='gray')

dilated_t = cv2.dilate(thinned, kernel, iterations=5)

plt.imshow(dilated_t, cmap='gray')

contours, _ = cv2.findContours(dilated_t, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

i=0
#list for storin names of shapes
for contour in contours:

  #here we are ignoring first counter because
  # findcontour function detects whole image as shape
  if i == 0:
      i = 1
      continue

  approx = cv2.approxPolyDP(
      contour, 0.02 * cv2.arcLength(contour, True), True)
  #to draw contours over the image
  cv2.drawContours(img, [contour], 0, (0, 0, 255), 2)

  #centroid of each shape
  M = cv2.moments(contour)
  if M['m00'] != 0.0:
    x = int(M['m10']/M['m00'])
    y = int(M['m01']/M['m00'])

  #put name of shape
  if len(approx) == 3:
     cv2.putText(img,'Triangle',(x,y),
              cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),5)

  elif len(approx) == 4:
      cv2.putText(img,'Rectangle',(x,y),
              cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),5)

  elif len(approx) == 5:
       cv2.putText(img,'Pentagon',(x,y),
              cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),5)

  elif len(approx) == 6:
       cv2.putText(img,'Hexagon',(x,y),
              cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,255),2)

  else:
    cv2.putText(img,'circle',(x,y),
              cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)

plt.imshow(img)