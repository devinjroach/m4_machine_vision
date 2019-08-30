import numpy as np
import os
import matplotlib.pyplot as plt
import skimage
import cv2
import itertools
import pandas as pd
import sys
import traceback

from skimage import data, color
from skimage import io
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte
from skimage.color import rgb2gray

    
#--------------------------------------------------------------------------------------

#image = cv2.imread('newstage1.bmp',0)
image = cv2.imread('newstage1.jpg',0)

image = cv2.resize(image,(480,360))
output =image.copy()

kernel = np.ones((5,5),np.float32)/25
image = cv2.filter2D(image,-1,kernel)
#image = cv2.medianBlur(image, 5)
#image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
#plt.imshow(image), plt.show()

#set parameters
params = {'minDist': [1, 10, 35, 50], 'param1': [10, 30, 50, 75, 100, 150], 'param2': [1, 5, 40] }

pList = []
for key in params:
    pList.append(params[key])

param_combs = list(itertools.product(*pList))

paramKeys = []
for key in params:
    paramKeys.append(key)

#run each image
param_combs_dict = []
for j in range(len(param_combs)):  
    try:
        print (str(j+1) + '/' + str(len(param_combs)))
        ppZip = zip(paramKeys, param_combs[j])
        param_combs_dict.append(dict(ppZip))
    # detect circles in the image
    #(image, method, dp, minDist, param1 = 100, param2 = 100, minRadius = 0, maxRadius = 0)
    #minDist = minimum distance between the centers of the detected circles. If the parameter is too small, multiple neighbor circles may be falsely detected in addition to a true one. If it is too large, some circles may be missed.
    #param1 = the higher threshold of the two passed to the Canny edge detector
        minDist = param_combs_dict[j]['minDist']
        param1 = param_combs_dict[j]['param1']
        param2 = param_combs_dict[j]['param2']
        #thresh = (image < 100).astype('uint8')
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, minDist, param1, param2)
        #circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, minDist, param1, param2)
        
        #circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 45, 75, 40);

            # ensure at least some circles were found
        if circles is None:
            none = "no circles found"
            print none
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
         
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (255, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                
            #save each image
            
            out = np.hstack([image,output])
            cv2.imwrite('C:\\Users\\Devin Roach\\Dropbox (GaTech)\\177A_BigPrinter\\Devin\\Machine Vision\\Code\\images\\imgmindist'+str(minDist)+'_1param'+str(param1)+ '_2param,'+ str(param2) + '_.jpg',out)
            #plt.imsave('imgmindist'+str(minDist)+'p1_'+str(param1), 'p2_'+ str(param2),np.hstack([image,output]))
        # show the output image
    #cv2.imshow("output", np.hstack([image, output]))
    #cv2.waitKey(0)
    except Exception as e:
        print(e)
        tb = sys.exc_info()[-1]
        print(traceback.extract_tb(tb, limit=1)[-1][1])
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('\n\n\n\nError on Line: ' + str(exc_tb.tb_lineno) + '     Error Information: ' + str(sys.exc_info()[:]))
        
