from scipy.misc.pilutil import imread, imsave
import numpy as np
from sys import argv

np.seterr(all='warn')

def shrink(image, ratio):

  """ This function shrinks given image by the ratio given horizontally
      and vertically.

      Example: shrink(img, 4) will take 4 x 4 matrices from the left top
               corner to the right bottom corner and set the average value
               of the diagonal to the new image with the same order.

      Args: 
           image (numpy.ndarray): The image to be shrinked.
           ratio (int): The ratio of shrinkage vertically and horizontally.

      Returns:
           temp (numpy.ndarray): The shrinked image. 
  """

  height = len(image)
  width = len(image[0])

  n_height = height // ratio
  n_width = width // ratio

  img_dim = len(image.shape)

  if img_dim == 2:
    temp = np.zeros([n_height, n_width], dtype='uint8')
    for row in range(n_height):
      for col in range(n_width):
        temp[row][col] = mean(image[(row * ratio):(row * ratio + ratio),
        (col * ratio):(col * ratio + ratio)])
          
  elif img_dim == 3:
    temp = np.zeros([n_height, n_width, 3], dtype='uint8')
    for row in range(n_height):
      for col in range(n_width):

        temp[row][col][0] = np.mean(image[(row * ratio):(row * ratio + ratio),
        (col * ratio):(col * ratio + ratio)][:,:,0])

        temp[row][col][1] = np.mean(image[(row * ratio):(row * ratio + ratio),
        (col * ratio):(col * ratio + ratio)][:,:,1])

        temp[row][col][2] = np.mean(image[(row * ratio):(row * ratio + ratio),
        (col * ratio):(col * ratio + ratio)][:,:,2])

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
  imsave('test_output.jpg', shrink(img, int(argv[1])))

if __name__ == '__main__':
  main()


