# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YvnijZjVN-7oMarw9dxloBt_K7N1I_uS
"""

from google.colab import drive
drive.mount('/content/drive')

import os
os.listdir(os.getcwd()+'/drive/My Drive/Samples')

import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
im = cv2.imread(os.getcwd()+'/drive/My Drive/Samples/'+'img6.jpg')
imf = im.copy()
plt.imshow(im)

def canny(im):
  edged = cv2.Canny(im, 10, 250)

  #applying closing function 
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
  closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

  #finding_contours 
  (_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    cv2.drawContours(im, [approx], -1, (255, 255, 255), 2)

  pts = np.argwhere(edged>0)
  y1,x1 = pts.min(axis=0)
  y2,x2 = pts.max(axis=0)
  imf1 = imf.copy()
  ## crop the region
  cropped = imf1[y1:y2, x1:x2]
  cv2.imwrite("cropped.jpg", cropped)
  plt.imshow(cropped)

canny(imf)

def bgremove(img):
  BLUR = 21
  CANNY_THRESH_1 = 10
  CANNY_THRESH_2 = 250
  MASK_DILATE_ITER = 10
  MASK_ERODE_ITER = 10
  MASK_COLOR = (255.0,255.0,255.0) # In BGR format

  #-- Read image -----------------------------------------------------------------------
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

  #-- Edge detection -------------------------------------------------------------------
  edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
  edges = cv2.dilate(edges, None)
  edges = cv2.erode(edges, None)

  #-- Find contours in edges, sort by area ---------------------------------------------
  contour_info = []
  _, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
  for c in contours:
      contour_info.append((
          c,
          cv2.isContourConvex(c),
          cv2.contourArea(c),
      ))
  contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
  max_contour = contour_info[0]

  #-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
  # Mask is black, polygon is white
  mask = np.zeros(edges.shape)
  cv2.fillConvexPoly(mask, max_contour[0], (255))

  #-- Smooth mask, then blur it --------------------------------------------------------
  mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
  mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
  mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
  mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

  #-- Blend masked img into MASK_COLOR background --------------------------------------
  mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
  img         = img.astype('float32') / 255.0                 #  for easy blending

  masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
  masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 

#   plt.imshow(masked)

  
  
  c_red, c_green, c_blue = cv2.split(img)

  # merge with mask got on one of a previous steps
  img_a = cv2.merge((c_red, c_green, c_blue, mask.astype('float32') / 255.0))

  # show on screen (optional in jupiter)
#   %matplotlib inline
  plt.imshow(img_a)

def backgremove(im1 , i):
  BLUR = 21
  CANNY_THRESH_1 = 10
  CANNY_THRESH_2 = 250
  MASK_DILATE_ITER = 10
  MASK_ERODE_ITER = 10
  MASK_COLOR = (255.0,255.0,255.0) # In BGR format
  img = np.asarray(im1)
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
  edges = cv2.dilate(edges, None)
  edges = cv2.erode(edges, None)
  contour_info = []
  _, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
  for c in contours:
      contour_info.append((
          c,
          cv2.isContourConvex(c),
          cv2.contourArea(c),
      ))
  contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
  max_contour = contour_info[0]
  mask = np.zeros(edges.shape)
  cv2.fillConvexPoly(mask, max_contour[0], (255))
  mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
  mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
  mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
  mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

  
  mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
  img         = img.astype('float32') / 255.0                 # for easy blending

  masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
  masked = (masked * 255).astype('uint8')     
    
  c_red, c_green, c_blue = cv2.split(img)
  img_a = cv2.merge((c_red, c_green, c_blue, mask.astype('float32') / 255.0))
  
  x = 80 
  y = 250
  w = 420
  h = 110 
  crop_img = img_a[y:y+h, x:x+w]
  
#   %matplotlib inline
  path = os.getcwd()+'/drive/My Drive/Samples/';
  plt.imsave(os.path.join(path , 'final' + str(i) + '.png'), crop_img)
  plt.imshow(crop_img)

backgremove(im , 9)



cropimg = cv2.imread(os.getcwd()+'/drive/My Drive/Samples/'+'final9.png')










#plt.imshow(cropimg)

from PIL import Image
i = 1;
for image in os.listdir(os.getcwd()+'/drive/My Drive/Samples'):
  img = cv2.imread(os.path.join(os.getcwd()+'/drive/My Drive/Samples',image))
  #backgremove(img,i)
  i = i + 1

#smoothing of the image
def smoothing():
  kernel = np.ones((5,5),np.float32)/25
  dst = cv2.filter2D(cropimg,-1,kernel)
  plt.imshow(dst)

smoothing()

#To Decease 50% noise
def median():
  median = cv2.medianBlur(cropimg,5)
  plt.imshow(median)
  
median()

#GrayScale
def grayscale():
  image = cv2.cvtColor(cropimg,cv2.COLOR_BGR2GRAY)
  plt.imshow(image)

grayscale()

#mask
def mask():
      hsv = cv2.cvtColor(cropimg, cv2.COLOR_BGR2HSV)
      lblue = np.array([30 , 30, 30])
      ublue = np.array([200 , 180 , 180])
      mask = cv2.inRange(hsv, lblue, ublue)
      res = cv2.bitwise_and(cropimg,cropimg, mask= mask)
      plt.imshow(res)

mask()

def histogram():
  # creating a Histograms Equalization 
  # of a image using cv2.equalizeHist() 
  cropimg1 = cv2.cvtColor(cropimg,cv2.COLOR_BGR2GRAY) # or convert
  equ = cv2.equalizeHist(cropimg1) 
  plt.imshow(equ) 

histogram()

cropimg1 = cv2.cvtColor(cropimg,cv2.COLOR_BGR2GRAY) # or convert
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(cropimg1)
plt.imshow(cl1)

gamma = 2.5 # Gamma < 1 ~ Dark  ;  Gamma > 1 ~ Bright

gamma_correction = ((cropimg/255) ** (1/gamma)) 
plt.figure(figsize = (5,5))
plt.imshow(gamma_correction)

plt.imshow(cropimg)