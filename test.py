#!/usr/bin/env python

import unittest
import nbconvert
import os

import skimage
import skimage.measure
import skimage.transform
import cv2
import warnings

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


with open("assignment9.ipynb") as f:
    exporter = nbconvert.PythonExporter()
    python_file, _ = exporter.from_file(f)


with open("assignment9.py", "w") as f:
    f.write(python_file)


from assignment9 import Plotter

class TestSolution(unittest.TestCase):
    
    def test_plot(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            p = Plotter('data.dat')
            p.plot_png('ss_plot')

            gold_image = cv2.imread('ss_plot_gold.png')
            test_image = cv2.imread('ss_plot.png')

            test_image_resized = skimage.transform.resize(test_image, 
                                                          (gold_image.shape[0], gold_image.shape[1]), 
                                                          mode='constant')

            ssim = skimage.measure.compare_ssim(skimage.img_as_float(gold_image), test_image_resized, multichannel=True)
            assert ssim >= 0.75

if __name__ == '__main__':
            unittest.main()
