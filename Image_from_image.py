#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 15:41:10 2021

@author: max 
"""

import cv2
import os
from PIL import Image
import numpy as np
import copy


os.chdir(PATH_TO_DIRECTORY)         
og_img = cv2.imread("cat4k.jpeg")
og_img= cv2.cvtColor(og_img, cv2.COLOR_BGR2RGB)

filler_img = cv2.imread("pupil.jpg")
filler_img=cv2.cvtColor(filler_img, cv2.COLOR_BGR2RGB)
#cv2 uses Blue Green Red instead of normal RGB

def resize(img,scale):
    return cv2.resize(img,(round(img.shape[1]*scale),round(img.shape[0]*scale)))


resize_filler = resize(filler_img,0.025)  #smaller value means more filler image, but they will be of less quality

def make_com(img,filler):
    """
    Parameters
    ----------
    img : img
        This is the image that will be split into chunks
    filler : img
        This is the smalller image that will be encoded into img

    resizes img so that filler can go evenly into it. 
    """
    width = img.shape[1]%filler.shape[1]
    if width!=0:
        if width/filler.shape[1]>=0.5:
            new_w = img.shape[1] + (filler.shape[1]-width) #filler= width+x
        else:
            new_w = img.shape[1]-width
    else:
        new_w = img.shape[1]
        
    h = img.shape[0]%filler.shape[0]
    if h!=0:
        if h/filler.shape[0]>=0.5:
            new_h = img.shape[0] + (filler.shape[0]-h) 
        else:
            new_h = img.shape[0]-h
    else:
        new_h = img.shape[0]
        
    return cv2.resize(img,(new_w,new_h))

img = make_com(resize(og_img,1),resize_filler)
#this makes it so that the filler image will be able to completely and evenly fit inside the image

#Image.fromarray(img).show() #shows og predit image

def create_img(img,step_r,step_c,alpha):

    for row in range(0,img.shape[0],step_r): #row is really the height
        for col in range(0,img.shape[1],step_c):   #nump array has img as height, width, channels
            filler = img[row:row+step_r, col:col+step_c,:]
            red=   round(filler[:,:,0].sum()  /(step_c*step_r))
            green= round(filler[:,:,1].sum() /(step_c*step_r))
            blue=  round(filler[:,:,2].sum()  /(step_c*step_r))
            
            color_img = filler*[0,0,0] + [red,green,blue]  #makes image the same size and pure color
            color_img = color_img.astype('uint8')  #assuming cv2 will read og_img image as uint8
            
            blend_tmp= cv2.addWeighted(resize_filler, 1-alpha, color_img, alpha, 0) 
        #values closer to one make that image more predominant. 
        #Fifth value is a value added to all pixels. x0 term/y interept
        #alpha changes the likeness it is like the avg value. 
        #so alpha of 1 takes that area and makes it the avg pixel color, ignoring the filler. 
            img[row:row+step_r, col:col+step_c,:] = blend_tmp
            
    return img

step_r = resize_filler.shape[0]
step_c = resize_filler.shape[1]
alpha = 0.75 #this means that it will be 75% the color, 25% the filler


edit_img = create_img(img,step_r,step_c,alpha)

Image.fromarray(edit_img).show()  #shows finished img
cv2.imwrite('final_photo.jpg',cv2.cvtColor(edit_img, cv2.COLOR_RGB2BGR)) #saves photo.
