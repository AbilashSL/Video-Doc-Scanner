# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 09:10:32 2018

@author: C3-IP
"""

from transform import four_point_transform
from skimage.filters import threshold_adaptive
import numpy as np
import cv2



cap=cv2.VideoCapture(0)
cap.set(3,1080) #set resolution if necessary
cap.set(4,720) #

while(True):
    ret,image=cap.read()
#   
    kernel_sharpening = np.array([[0,-1,0], #sharpening the image for better edges
                              [-1, 4,-1],
                              [0,-1,0]])

    image1 = cv2.filter2D(image, -1, kernel_sharpening)
    image=cv2.add(image,image1) #filtering
#   )
    orig = image.copy() 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    gray = cv2.GaussianBlur(gray, (5, 5), 0) #noise removal
     
    kernel = np.ones((15, 15), np.uint8)
    Opened=cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel) #opening for clear edges
    
    
    
    edged = cv2.Canny(Opened, 75, 200) #detecting edges using canny
    k,l,m=image.shape
   
    cv2.imshow("Edged", edged)
   
    
   
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #finding contours of the image
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    
    MAX_COUNTOUR_AREA = (l - 5) * (k - 5)
    
    maxAreaFound = MAX_COUNTOUR_AREA *0.01
#    finding the closed contours such that they have significant area and four edges
    
    for c in cnts:
       
        peri = cv2.arcLength(c, True)
        approx =cv2.approxPolyDP(c, 0.02 * peri, True)
        Area=cv2.contourArea(approx)
        print(Area)
     
        if len(approx) ==4 and Area > maxAreaFound  : 
            screenCnt = approx
            cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
            warped = four_point_transform(orig, screenCnt.reshape(4, 2)) #making the scanned copy straight
            warped1 = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
            warped1= threshold_adaptive(warped1, 251, offset = 10)
            warped1 = warped1.astype("uint8") * 255
            cv2.imwrite("//destination",warped)
            cv2.imshow("scanned",warped)
            if cv2.waitKey(1) & 0xFF == ord('q'): #press q to exit video
                break
#           
  
    cv2.imshow("scanned", image)
   
    cv2.imshow('Edged',edged)
  
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()