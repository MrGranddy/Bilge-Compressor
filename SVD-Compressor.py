from scipy.misc.pilutil import imread, imsave
import numpy as np

np.seterr(all='warn')

def black_white(image):

    height = len(image)
    width = len(image[0])

    temp = np.zeros([height, width], dtype = 'uint64')

    row = 0
    while row < height:
        col = 0
        while col < width:
            value = 0
            value += image[row][col][0]
            value += image[row][col][1]
            value += image[row][col][2]

            temp[row][col] = value / 3

            col = col + 1
        row = row + 1
    return temp

image = imread('kedi.jpg')

image1 = black_white(image)

u, s, v = np.linalg.svd(image1, full_matrices=1)

factor = 300

sigma = np.zeros([factor], dtype = 'float64')

i = 0
while i < factor:
    sigma[i] = s[i]
    i += 1

u = np.transpose(u)
reducedU = np.zeros([factor, len(u[0])], dtype='float64')

i = 0
while i < factor:
    reducedU[i] = u[i]
    i += 1

reducedU = np.transpose(reducedU)

reducedV = np.zeros([factor, len(v[0])], dtype='float64')

i = 0
while i < factor:
    reducedV[i] = v[i]
    i += 1

compressed = np.dot(reducedU, np.dot(np.diag(sigma), reducedV))

imsave('compressed_factor_300.jpg', compressed)


