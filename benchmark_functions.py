#!usr/env/bin
#-*- coding : utf-8 -*-

## 最適化関数のベンチマーク関数のテスト

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D as a3d
from matplotlib import cm
import numpy as np

def plot_3d(xyz, title):
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_title(title)
    cmap = cm.gist_ncar
    surf = ax.plot_surface(x,y,z, cmap = cmap, alpha = 0.7)
    fig.colorbar(surf)
    if np.sum(np.nanmin(z) == z) == 1:
        minpoint = np.where(np.nanmin(z) == z)
        min1 = minpoint[0].item()
        min2 = minpoint[1].item()
        ax.scatter(x[min1,min2], y[min1,min2], z[min1,min2], color = 'r', s = 20, marker = '*')
        xlines = np.tile(x[min1,min2], 300)
        ylines = np.tile(y[min1,min2], 300)
        zlines = np.linspace(np.nanmin(z), np.max(z), 300)
        ax.plot(xlines,ylines,zlines, color = 'r', lw = 1.5)
        ax.text(x[min1,min2], y[min1,min2], zlines[299], '({:.2f},{:.2f},{:.2f})'.format(x[min1,min2], y[min1,min2], z[min1,min2]), color = 'gray', alpha = 0.7)
    else:
        minpoint = np.where(np.nanmin(z) == z)
        for mp in minpoint:
            min1 = mp[0]
            min2 = mp[1]
            ax.scatter(x[min1,min2], y[min1,min2], z[min1,min2], color = 'r', s = 20, marker = '*')
            xlines = np.tile(x[min1,min2], 300)
            ylines = np.tile(y[min1,min2], 300)
            zlines = np.linspace(np.nanmin(z), np.max(z), 300)
            ax.plot(xlines,ylines,zlines, color = 'r', lw = 1.5)
            ax.text(x[min1,min2], y[min1,min2], zlines[299], '({:.2f},{:.2f},{:.2f})'.format(x[min1,min2], y[min1,min2], z[min1,min2]), color = 'gray', alpha = 0.7)
    plt.savefig('benchmark_functions/'+title+'.png')
    plt.close()

def initialize_xy(data_range_xy, data_sep = 0.01):
    o = np.arange(data_range_xy[0], data_range_xy[1], data_sep)
    return np.meshgrid(o,o)

def main_benchmarks(data_range_xy, data_sep = 0.01, function_type = None):
    benchmarks = ['ackely','sphere','rosenbrock','beale','goldstein_price','booth','bukin_n6','matyas','ThreeHumpCamel','easom','eggholder','mccormick','crossintray','holdertable','styblinski_tang','himmelblau','xinshe_yang']
    if function_type not in benchmarks:
        print('{} : This function type is not available.'.format(function_type))
        return None
    x,y = initialize_xy(data_range_xy, data_sep)
    if function_type == 'ackely':
        z = ackley(x,y)
    elif function_type == 'sphere':
        z =  sphere(x,y)
    elif function_type == 'rosenbrock':
        z =  rosenbrock(x,y)
    elif function_type == 'beale':
        z =  beale(x,y)
    elif function_type == 'goldstein_price':
        z =  goldstein_price(x,y)
    elif function_type == 'booth':
        z =  booth(x,y)
    elif function_type == 'bukin_n6':
        z =  bukin_n6(x,y)
    elif function_type == 'matyas':
        z =  matyas(x,y)
    elif function_type == 'ThreeHumpCamel':
        z =  ThreeHumpCamel(x,y)
    elif function_type == 'easom':
        z =  easom(x,y)
    elif function_type == 'eggholder':
        z =  eggholder(x,y)
    elif function_type == 'mccormick':
        z =  mccormick(x,y)
    elif function_type == 'crossintray':
        z =  crossintray(x,y)
    elif function_type == 'holdertable':
        z =  holdertable(x,y)
    elif function_type == 'styblinski_tang':
        z =  styblinski_tang(x,y)
    elif function_type == 'himmelblau':
        z =  himmelblau(x,y)
    elif function_type == 'xinshe_yang':
        z =  xinshe_yang(x,y)
    plot_3d(z, function_type)

def ackley(x,y):
    a1 = 20 - 20 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2)))
    a2 = np.e - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
    return x,y,a1 + a2

def sphere(x,y):
    return x,y,x**2 + y**2

def rosenbrock(x,y):
    return x,y,100 * (y - x**2)**2 + (x-1)**2

def beale(x,y):
    a1 = (1.5 - x + (x*y))**2
    a2 = (2.25 - x + (x*(y**2)))**2
    a3 = (2.625 - x + (x*(y**3)))**2
    return x, y, a1 + a2 + a3

def goldstein_price(x,y):
    a1 = 1 + (x+y+1)**2 * (19-14*x+3*x**2 - 14*y + 6*x*y + 3*y**2)
    a2 = 30 + (2 * x - 3 * y) ** 2 * (18 - 32*x + 12 * x**2 + 48 * y - 36*x*y + 27*y**2)
    return x, y, a1*a2

def booth(x,y):
    a1 = (x + 2 * y - 7)**2
    a2 = (2*x + y - 5)**2
    return x, y, a1 + a2

def bukin_n6(x,y):
    a1 = 100 * np.sqrt(np.abs(y - 0.01 * x**2))
    a2 = 0.01 * np.abs(x + 10)
    return x, y, a1 + a2

def matyas(x,y):
    a1 = 0.26 * (x**2 + y**2)
    a2 = 0.48 * x * y
    return x,y,a1-a2

def ThreeHumpCamel(x,y):
    a1 = 2 * x**2 - 1.05 * x**4 + x**6/6 + x*y + y**2
    return x, y, a1

def easom(x,y):
    a1 = np.cos(x) * np.cos(y)
    a2 = np.exp(- ((x-np.pi)**2 + (y - np.pi)**2))
    return x, y, -1 * a1 * a2

def eggholder(x,y):
    a1 = -(y + 47) * np.sin(np.sqrt(np.abs(x/2 + (y + 47))))
    a2 = -x * np.sin(np.sqrt(np.abs(x - (y + 47))))
    return x, y, a1 + a2

def mccormick(x,y):
    a1 = np.sin(x+y) + (x - y)**2 - 1.5 * x + 2.5 * y + 1
    return x, y, a1

def crossintray(x,y):
    a1 = - 0.0001
    a2 = np.abs(np.sin(x) * np.sin(y) * np.exp(np.abs(100 - np.sqrt(x**2 + y**2)/np.pi)) + 1) ** 0.1
    return x, y, a1 * a2

def holdertable(x,y):
    a1 = -1 * np.abs(np.sin(x) * np.cos(y) * np.exp(np.abs(1 - np.sqrt(x**2 + y**2)/np.pi)))
    return x, y, a1

def styblinski_tang(x,y):
    a1 = (x ** 4 - 16 * x ** 2 + 5 * x)
    a2 = (y ** 4 - 16 * y ** 2 + 5 * y)
    return x, y, (a1 + a2) / 2

def himmelblau(x,y):
    a1 = (x**2 + y - 11) ** 2
    a2 = (x + y**2 - 7) **2
    return x, y, a1+a2

def xinshe_yang(x,y):
    a1 = (np.abs(x) + np.abs(y)) * np.exp(-1 * (np.sin(x**2) + np.sin(y**2)))
    return x, y, a1

if __name__=='__main__':
    settings = [
                ['ackely',(-5.12,5.12),0.01]
                ,['sphere',(-5,5),0.01]
                ,['rosenbrock',(-5,5),0.01]
                ,['beale',(-4.5,4.5),0.01]
                ,['goldstein_price',(-2,2),0.01]
                ,['booth',(-10,10),0.01]
                ,['bukin_n6',(-15,3),0.01]
                ,['matyas',(-10,10),0.01]
                ,['ThreeHumpCamel',(-5,5),0.01]
                ,['easom',(-5,5),0.01]
                ,['eggholder',(-512,512),1]
                ,['mccormick',(-3,4),0.01]
                ,['crossintray',(-10,10),0.01]
                ,['holdertable',(-10,10),0.01]
                ,['styblinski_tang',(-5,5),0.01]
                ,['himmelblau',(-5,5),0.01]
                ]
    for bench in settings:
        print(bench)
        main_benchmarks(bench[1], bench[2], bench[0])