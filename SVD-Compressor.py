from scipy.misc.pilutil import imread, imsave
import numpy as np

np.seterr(all='warn')


def shrink(image, vertical, horizontal):

    height = len(image)
    width = len(image[0])

    n_height = height // vertical
    n_width = width // horizontal

    temp = np.zeros([n_height, n_width, 3], dtype='uint64')

    row = 0
    while row < n_height - 1:
        col = 0
        while col < n_width - 1:
            temp[row][col] = image[row * vertical][col * horizontal]
            col += 1
        row += 1
    return temp
# Takes 3 dimensional array as input


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

            col += 1
        row += 1
    return temp
# Returns a 2 dimensional output


def compressor(image, factor):

    image1 = black_white(image)

    u, s, v = np.linalg.svd(image1, full_matrices=1)

    sigma = np.zeros([factor], dtype='float64')

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

    return compressed
# Compresses only inputs with 2 dimension

i = 1
while i < 64:
    img = imread(str(i) + '.jpg')
    cmp = compressor(shrink(img, 2, 2), 250)
    imsave(str(i) + '_output.jpg', cmp)
    print('Compressed ' + str(i) + '...')
    i += 1


