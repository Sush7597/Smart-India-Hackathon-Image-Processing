# -*- coding: utf-8 -*-
"""Copy of SIh model

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11a8PTuSHJNBv0ceWNldh8n91jzu3d3el
"""

from google.colab import drive
drive.mount('/content/drive/')

import os
os.listdir(os.getcwd()+'/drive/My Drive/Samples')
import sys
sys.setrecursionlimit(1500)

import matplotlib.pyplot as plt
import matplotlib.image as im

as2 = im.imread(os.getcwd()+'/NEU-CLS-64/pa/1.jpg')
plt.figure()
mini = as2.min()
maxi = as2.max()

as1 = (255)/(maxi - mini)*(as2-mini)
plt.figure()
plt.imshow(as2)
plt.show()
plt.imshow(as1)
plt.show()

list_of_x = []
isvisited = np.zeros(as2.shape)
shape_of = np.zeros(as2.shape)
print(as2.shape)

def colorthegraph(x,y):
  if((x > as2.shape[0] or x<0)):
    return 0
  elif(y > as2.shape[1] or y<0):
    return 0
  elif(isvisited[x][y] == 1):
    return 0
  print(x,y)
  isvisited[x][y] = 1
  shape_of[x][y] = curr_num
  sum1 = 0
  if(as2[x+1][y] >= threshold):
    sum1 += colorthegraph(x,y+1)
  if(as2[x][y+1] >= threshold):
    sum1 += colorthegraph(x+1,y)
  if(as2[x-1][y] >= threshold):
    sum1 += colorthegraph(x-1,y)
  if(as2[x][y-1] >= threshold):
    sum1 += colorthegraph(x,y-1)
  if(as2[x+1][y+1] >= threshold):
    sum1 += colorthegraph(x+1,y+1)
  if(as2[x-1][y+1] >= threshold):
     sum1 += colorthegraph(x-1,y+1)
  if(as2[x+1][y-1] >= threshold):
    sum1 += colorthegraph(x+1,y-1)
  if(as2[x-1][y-1] >= threshold):
    sum1 += colorthegraph(x-1,y-1)
  return sum1



curr_num = 1
threshold = 100

for i in range(0,as2.shape[0]):
  for j in range(0,as2.shape[1]):
    if(isvisited[i][j] == 0 ):
      colorthegraph(i,j)
      curr_num += 1
     
    
    
isvisited[:][:]

plt.imshow(as2)

print(curr_num)

plt.imshow(shape_of)