# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 20:46:31 2017

@author: HuXiaotian
"""

from skimage import filters,measure,transform,color
from scipy import misc
import numpy as np
#import matplotlib.pyplot as plt

def captureleaf(im,fill):
    
    imsize = im.shape
    resizefactor = 1
    imsize = (np.floor(imsize[0]/resizefactor),\
              np.floor(imsize[1]/resizefactor),\
              3)
    
    im = transform.resize(im,imsize)
    # fetch the green compenent
    img = im[:,:,1]
    Ithreshold = filters.threshold_otsu(img)
    imgbw = img > Ithreshold
    
    relativethres = 0.1
    
    imgcc,labelnum =  measure.label(imgbw,neighbors = 4, return_num = True)
    areas =  measure.regionprops(imgcc)
    #
    for ind in range(labelnum):
        a = float(areas[ind].area)
        #print(a)
       # print a/imgcc.size
        if a/imgcc.size > relativethres:
        #    print a        
            leafind = ind + 1
            break
    #    
    #
    imgccinv = imgcc.copy()
    ##
    ##
    imgccinv[imgcc == leafind] = 0  
    imgccinv[imgcc != leafind] = 1
    [holes, indnum]  = measure.label(imgccinv,neighbors = 4, return_num = True)
    areas = measure.regionprops(holes)
    #
    for ind in range(indnum):
        a = float(areas[ind].area)
        if a/imgcc.size > relativethres:
            backind = ind + 1
            break
    
    holes[holes == backind] = 0
    imgcc[holes != 0] = leafind
    #
    imleaf = im.copy()
    for i in range(3):
        tmp = imleaf[:,:,i]
        tmp[imgcc!= leafind] = fill
        imleaf[:,:,i] = tmp
        
    return imleaf

def countholes(imleaf):
    
    
    imleafgray = color.rgb2gray(imleaf)
    Ithreshold = filters.threshold_otsu(imleafgray)
    imleafbw = imleafgray < Ithreshold
    del imleafgray
    #
    imleafcc,indnum = measure.label(imleafbw,neighbors = 4, return_num = True)
    areas = measure.regionprops(imleafcc)
    #
    holebound = [30,100]
    #eccentricitythres = 0.5
    
    holenum = 0
    for i in range(indnum):
        a = float(areas[i].area)
        #print(a)
        if a > holebound[0] and a < holebound[1]:
            moment = areas[i].inertia_tensor_eigvals
            roundness = float(moment[0])/float(moment[1])
#            print(a)
#            print(roundness)
            if roundness < 6:
                holenum += 1
    
    return holenum

def countspt(imleaf):
    imy = imleaf[:,:,0]
    imybw = imy > .8
    
    imleafcc,indnum = measure.label(imybw,neighbors = 4, return_num = True)
    areas = measure.regionprops(imleafcc)
    #
    holebound = [30,100]
    #eccentricitythres = 0.5
    
    holenum = 0
    for i in range(indnum):
        a = float(areas[i].area)
        #print(a)
        if a > holebound[0] and a < holebound[1]:
    
            moment = areas[i].inertia_tensor_eigvals
            roundness = float(moment[0]/moment[1])
    #        print(a)
    #        print(roundness)
            if roundness < 6:
                holenum += 1
    
    return holenum
    
    
#im = misc.imread('image2.jpg')
#imleaf = captureleaf(im,0)
##plt.imshow(imleaf)
#print(countholes(imleaf))
#print(countspt(imleaf))
#misc.imsave("image2res.jpg",imleaf)
#plt.imshow(imleaf[:,:,0])
#plt.colorbar()
