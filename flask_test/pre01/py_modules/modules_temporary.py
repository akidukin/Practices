#!usr/env/bin py
#-*- encoding : utf-8 -*-

from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class temporary:

    def __init__(self, values):
        self.init = values + 1

    def get_result(self):
        return self.init

class temporary_pict:

    def __init__(self, pict):
        self.init = Image.open(pict).convert('RGB')

    def get_result(self):
        return np.array(self.init)

class temporary_pict02:

    def __init__(self):
        self.x, self.y = np.meshgrid(np.arange(-10,10,0.01),np.arange(-10,10,0.01))
        self.z = self.sphere(self.x, self.y)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def sphere(self,x,y):
        return x**2+y**2

    def plot(self):
        self.ax.plot_surface(self.x, self.y, self.z, cmap = 'RdBu', alpha = 0.5)
        return self.fig

    def plot_point(self, x, y):
        self.ax.plot_surface(self.x, self.y, self.z, cmap = 'RdBu', alpha = 0.5)
        self.ax.scatter(x, y, self.sphere(x,y), cmap = 'g', marker='*')
        return self.fig