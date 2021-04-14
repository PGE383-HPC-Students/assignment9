#!/usr/bin/env python
# coding: utf-8

# # Assignment 9
# 
# This repository contains the same file `data.dat` from [Assignment 8](https://github.com/PGE383-HPC-Students/assignment8) and Python classes named `StressStrainConverter` and `Toughness` that implement a solution to that assignment.
# 
# You should complete the derived class `Plotter` to create the following plot exactly as shown. 
# 
# ![img](ss_plot_gold.png)
# 
# Specifically you will need to complete the `plot()` function.  Here are couple of hints to get things exactly right.
# 
#  * The gray fill color can be specified using the option `color='0.75'`.
#  
#  * The label in the center uses $\LaTeX$, specifically it uses the `\mathcal{T}` for the cursive T.  It is placed at the $(\varepsilon, \sigma) = (0.25, 60000)$ and uses a font size of `16`.
#  
#  * Don't hard code the value of toughness, but rather compute it, store it as a variable and use that to create the label.
#  
# After you have the tests passing on Github, check back in on the repository on Github and look for a new branch called `create-pull-request/patch` to view the PDF that was automatically generated.  This demonstrates how to include a matplotlib figure in a $\LaTeX$ document and have the math fonts in the figure and in the text match exactly.
# 

# In[3]:


import numpy as np
import linecache
import scipy.integrate



import matplotlib.pyplot as plt

class StressStrainConverter():
    
    def __init__(self, filename):
        
        self.filename = filename
        

    def extract_dimensions(self):

        line = linecache.getline(self.filename, 3).split('=')

        self.width = float(line[1].split('"')[0])

        self.thickness = float(line[2].split('"')[0]) 

        return
    

    def convert_to_true_stress_and_strain(self):
        
        self.extract_dimensions()

        eng_strain, force = np.loadtxt(self.filename, skiprows=5, usecols=(2,3)).T 

        self.true_strain = np.log(1 + eng_strain)

        self.true_stress = force / self.width / self.thickness * (1 + eng_strain)

        return 
    
    
class Toughness(StressStrainConverter):
    
    def compute_toughness_simps(self):
        
        self.convert_to_true_stress_and_strain()
        
        return scipy.integrate.simps(self.true_stress, self.true_strain)
    
    def compute_toughness_trapz(self):
        
        self.convert_to_true_stress_and_strain()
        
        return scipy.integrate.trapz(self.true_stress, self.true_strain)
    
    
class Plotter(Toughness):
    
    def plot(self):
        
        fig, ax = plt.subplots(figsize=(8, 6), dpi=80)
        
        return
    
    def plot_png(self, basename):
        
        self.plot()
        
        plt.savefig('{}.png'.format(basename), bbox_inches='tight')
        
    def plot_pgf(self, basename):
        
        self.plot()
        
        plt.savefig('{}.pgf'.format(basename), bbox_inches='tight')

