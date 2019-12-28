#!usr/env/bin py
#-*- coding : utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D as a3d
from matplotlib import cm
import matplotlib.animation as animation

def sphere_grad(x1, x2):
    ## x1の偏微分
    x1_grad = 2 * x1
    ## x2の偏微分
    x2_grad = 2 * x2
    return x1_grad, x2_grad

def losenbrock_grad(x1,x2):
    x1_grad = -400 * x1 * (x2 + x1**2) - 2 + 2 * x1
    x2_grad = 200 * (x2 - x1**2)
    return x1_grad, x2_grad

def StyblinskiTang_grad(x1,x2):
    x1_grad = 2 * x1**3 - 16 * x1 + (5/2)
    x2_grad = 2 * x2**3 - 16 * x2 + (5/2)
    return x1_grad, x2_grad

def shpere_f(x1,x2):
    return x1**2 + x2**2

def losenbrock_f(x1,x2):
    return 100 * (x2 - x1**2)**2 + (x1-1)**2

def StyblinskiTang_f(x1,x2):
    a1 = (x1**4 - 16 * x1**2 + 5 * x1) / 2
    a2 = (x2**4 - 16 * x2**2 + 5 * x2) / 2
    return a1 + a2

def initialize_xy(data_range_xy, data_sep = 0.01):
    o = np.arange(data_range_xy[0], data_range_xy[1], data_sep)
    return np.meshgrid(o,o)

class optimizer_visualize:

    def __init__(self, function_type, epoch = 1000):
        self.epoch = epoch
        self.function_type = function_type
        if function_type == 'sphere':
            self.use_bench_func = shpere_f
            self.use_bench_grad = sphere_grad
            self.init_x, self.init_y = initialize_xy((-10,10),0.005)
        elif function_type == 'losenbrock':
            self.use_bench_func = losenbrock_f
            self.use_bench_grad = losenbrock_grad
            self.init_x, self.init_y = initialize_xy((-10,10),0.005)
        elif function_type == 'styblinskitang':
            self.use_bench_func = StyblinskiTang_f
            self.use_bench_grad = StyblinskiTang_grad
            self.init_x, self.init_y = initialize_xy((-5,5),0.005)
        else:
            print('This function is not available.')

        self.init_set = {}
        self.init_set['sgd'] = {}
        self.init_set['sgd']['lr'] = 0.05

        self.init_set['momentum_sgd'] = {}
        self.init_set['momentum_sgd']['alpha'] = 0.9
        self.init_set['momentum_sgd']['n'] = 0.01
        self.init_set['momentum_sgd']['preb_w1'] = 0
        self.init_set['momentum_sgd']['preb_w2'] = 0

        self.init_set['rmsprop'] = {}
        self.init_set['rmsprop']['h_x1'] = 0
        self.init_set['rmsprop']['h_x2'] = 0
        self.init_set['rmsprop']['n_x1'] = 0
        self.init_set['rmsprop']['n_x2'] = 0
        self.init_set['rmsprop']['e'] = 10**-8
        self.init_set['rmsprop']['n0'] = 0.01
        self.init_set['rmsprop']['alpha'] = 0.99

        self.init_set['adagrad'] = {}
        self.init_set['adagrad']['e'] = 10**-8
        self.init_set['adagrad']['x1_h'] = 10**-8
        self.init_set['adagrad']['x2_h'] = 10**-8
        self.init_set['adagrad']['n0'] = 0.001

        self.init_set['adadelta'] = {}
        self.init_set['adadelta']['v_x1'] = 0
        self.init_set['adadelta']['u_x1'] = 0
        self.init_set['adadelta']['v_x2'] = 0
        self.init_set['adadelta']['u_x2'] = 0
        self.init_set['adadelta']['p'] = 0.95

    def sgd(self, x1, x2, x1_grad, x2_grad):
        sgd_x1_t = x1 - self.init_set['sgd']['lr'] * x1_grad
        sgd_x2_t = x2 - self.init_set['sgd']['lr'] * x2_grad
        return sgd_x1_t, sgd_x2_t

    def momentumsgd(self, x1, x2, x1_grad, x2_grad):
        self.init_set['momentum_sgd']['preb_w1'] = x1 - (1- self.init_set['momentum_sgd']['alpha'])*self.init_set['momentum_sgd']['n'] * x1_grad + self.init_set['momentum_sgd']['alpha'] * self.init_set['momentum_sgd']['preb_w1']
        self.init_set['momentum_sgd']['preb_w2'] = x2 - (1- self.init_set['momentum_sgd']['alpha'])*self.init_set['momentum_sgd']['n'] * x2_grad + self.init_set['momentum_sgd']['alpha'] * self.init_set['momentum_sgd']['preb_w2']
        return self.init_set['momentum_sgd']['preb_w1'], self.init_set['momentum_sgd']['preb_w2']

    def adagrad(self, x1, x2, x1_grad, x2_grad):
        self.init_set['adagrad']['x1_h'] = self.init_set['adagrad']['x1_h'] + x1_grad**2
        adagrad_x1_nt = self.init_set['adagrad']['n0'] / (np.sqrt(self.init_set['adagrad']['x1_h']) + self.init_set['adagrad']['e'])
        adagrad_x1 = x1 - adagrad_x1_nt * x1_grad

        self.init_set['adagrad']['x2_h'] = self.init_set['adagrad']['x2_h'] + x2_grad**2
        adagrad_x2_nt = self.init_set['adagrad']['n0'] / (np.sqrt(self.init_set['adagrad']['x2_h']) + self.init_set['adagrad']['e'])
        adagrad_x2 = x2 - adagrad_x2_nt * x2_grad

        return adagrad_x1, adagrad_x2

    def rmsprop(self, x1, x2, x1_grad, x2_grad):
        self.init_set['rmsprop']['h_x1'] = self.init_set['rmsprop']['alpha'] * self.init_set['rmsprop']['h_x1'] + (1-self.init_set['rmsprop']['alpha']) * x1_grad**2
        self.init_set['rmsprop']['n_x1'] = self.init_set['rmsprop']['n0'] / (self.init_set['rmsprop']['h_x1'] + self.init_set['rmsprop']['e'])
        rmsprop_x1 = x1 - self.init_set['rmsprop']['n_x1'] * x1_grad

        self.init_set['rmsprop']['h_x2'] = self.init_set['rmsprop']['alpha'] * self.init_set['rmsprop']['h_x2'] + (1-self.init_set['rmsprop']['alpha']) * x2_grad**2
        self.init_set['rmsprop']['n_x2'] = self.init_set['rmsprop']['n0'] / (self.init_set['rmsprop']['h_x2'] + self.init_set['rmsprop']['e'])
        rmsprop_x2 = x2 - self.init_set['rmsprop']['n_x2'] * x2_grad

        return rmsprop_x1, rmsprop_x2

    def main_next_x(self,x1,x2,function_type):
        x1_grad, x2_grad = self.use_bench_grad(x1, x2)
        if function_type == 'sgd':
            x1t, x2t = self.sgd(x1,x2,x1_grad,x2_grad)
        elif function_type == 'momentum_sgd':
            x1t, x2t = self.momentumsgd(x1,x2,x1_grad,x2_grad)
        elif function_type == 'adagrad':
            x1t, x2t = self.adagrad(x1,x2,x1_grad,x2_grad)
        elif function_type == 'rmsprop':
            x1t, x2t = self.rmsprop(x1,x2,x1_grad,x2_grad)
        return x1t, x2t

op = optimizer_visualize(function_type = 'styblinskitang')
plot_x = op.init_x
plot_y = op.init_y
plot_z = op.use_bench_func(plot_x,plot_y)
fig = plt.figure()
ax = fig.gca(projection='3d')
cmap = cm.gist_earth
surf = ax.plot_surface(plot_x,plot_y,plot_z, cmap = cmap, alpha = 0.4)
fig.colorbar(surf)

for f,c in [('sgd', 'red'),('momentum_sgd','blue'),('adagrad', 'green'),('rmsprop','orange')]:
    print(f)
    x1_hist = []
    x2_hist = []
    z_hist = []
    x1 = np.max(plot_x)
    x2 = np.min(plot_y)
    for i in range(2500):
        try:
            z = op.use_bench_func(x1,x2)
            x1_hist.append(x1)
            x2_hist.append(x2)
            z_hist.append(z)
            x1,x2 = op.main_next_x(x1, x2, f)
        except:
            continue
    ax.plot(x1_hist, x2_hist, z_hist, color = c, marker = '*', lw = 1, label = f)
ax.set_ylim(np.min(plot_y), np.max(plot_y))
ax.set_xlim(np.min(plot_x), np.max(plot_x))
ax.set_zlim(np.min(plot_z), np.max(plot_z))
ax.legend()
plt.savefig('benchmark_functions/styblinskitang_optim.png')