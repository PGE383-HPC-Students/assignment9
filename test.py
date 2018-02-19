#!/usr/bin/env python

from assignment9 import Plotter

import skimage
import skimage.measure
import skimage.transform
import cv2

def test_plot():
    
    p = Plotter('data_1.dat')
    p.plot_png('ss_plot')
    
    gold_image = cv2.imread('ss_plot_gold.png')
    test_image = cv2.imread('ss_plot.png')
    
    test_image_resized = skimage.transform.resize(test_image, 
                                                  (gold_image.shape[0], gold_image.shape[1]), 
                                                  mode='constant')
    
    ssim = skimage.measure.compare_ssim(skimage.img_as_float(gold_image), test_image_resized, multichannel=True)
    assert ssim >= 0.9