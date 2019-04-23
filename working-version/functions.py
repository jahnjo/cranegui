import numpy as np
import mantis_parameters as mp


def trans_x(a):
    return np.array([[1., 0, a], [0, 1., 0], [0, 0, 1.]])


def trans_y(b):
    return np.array([[1., 0, 0], [0, 1., b], [0, 0, 1.]])


def trans_z(c):
    return np.array([[1., 0, 0], [0, 1., 0], [0, 0, c]])


def matrix_mult(a):
    result = np.identity(3)
    for i in range(0,len(a)):
        result = np.dot(result,a[i])
    return result


def c_o_m(p,w):
    px_sum = py_sum = pz_sum = total =  0
    for i in range(0,len(p)):
        px_sum = p[i][0]*w[i]+px_sum
        py_sum = p[i][1]*w[i]+py_sum
        pz_sum = p[i][2]*w[i]+pz_sum
        total +=w[i]
    return [px_sum/total,py_sum/total,pz_sum/total,1]


