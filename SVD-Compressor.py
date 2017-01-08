from scipy.misc.pilutil import imread, imsave, copy
import numpy as np

np.seterr(all='warn')

def shrink(image, vertical, horizontal):

""" This function shrinks given image by the ratio given horizontally
    and vertically.

    Example: shrink(img, 5, 3) will take 5 x 3 matrices from the left top
             corner to the right bottom corner and set their average value
             to a new image with the same order.

    Args: 
         image (numpy.ndarray): The image to be shrinked.
         vertical (int): Vertical shrinking ratio.
         horizontal (int): Horizontal shrinking ratio.

    Returns:
         temp (numpy.ndarray): The shrinked image."""

  height = len(image)
  width = len(imagee[0])

  n_height = height // vertical
  n_width = width // horizontal

  img_dim = len(image.shape)

  if img_dim == 2:
    temp = np.zeros([n_height, n_width], dtype='uint8')
    for row in range(height - (height % vertical)):
      for col in range(width - (width % horizontal)):
      	temp[row // vertical][col // horizontal] += image[row][col]
      	if not (row + 1) % vertical and not col % horizontal:
      	  temp[(row + 1) // vertical][col // horizontal] /= horizontal * vertical
          
  elif img_dim == 3:
  	temp = np.zeros([n_height, n_width, 4], dtype='uint8')
    for row in range(height - (height % vertical)):
      for col in range(width - (width % horizontal)):
        for clr in range(4):
      	  temp[row // vertical][col // horizontal][clr] += image[row][col][clr]
      	if not (row + 1) % vertical and not col % horizontal:
          for clr in range(4):
      	    temp[(row + 1) // vertical][col // horizontal][clr] /= horizontal * vertical

  return temp



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

def main():
  img = imread('test.jpg')
  imsave('test_output.jpg', shrink(img, 4, 4))

if __name__ == '__main__':
  main()


