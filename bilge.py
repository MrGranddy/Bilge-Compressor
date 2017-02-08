from scipy.misc.pilutil import imread, imsave
from numpy import zeros, mean, dot, diag, transpose, array, dstack, seterr, rot90
from numpy.linalg import svd
from sys import argv

seterr(all='warn')


def shrink_by_ratio(image, vertical, horizontal):
  """ Description:
            This function shrinks given image by the ratio given
            horizontally and vertically.

      Example:
            shrink_by_ratio(img, 4, 3) will take 4 x 3 matrices from the left
            top corner to the right bottom corner and set the average of the
            values in that matrix as pixels to the new image with the same
            order.

      Args:
            image (numpy.ndarray): The image to be shrinked.

            vertical (int): The ratio of shrinkage vertically.

            horizontal (int): The ratio of shrinkage horizontally.

      Returns:
            temp (numpy.ndarray): The shrinked image. 
  """

  height = len(image)
  width = len(image[0])

  n_height = height // vertical
  n_width = width // horizontal

  img_dim = len(image.shape)

  if img_dim == 2:
    temp = zeros([n_height, n_width], dtype='uint8')
    for row in range(n_height):
      for col in range(n_width):
        temp[row][col] = mean(image[(row * vertical):(row * vertical + vertical),
        (col * horizontal):(col * horizontal + horizontal)])# grayscale
          
  elif img_dim == 3:
    temp = zeros([n_height, n_width, 3], dtype='uint8')
    for row in range(n_height):
      for col in range(n_width):

        temp[row][col][0] = mean(image[(row * vertical):(row * vertical + vertical),
        (col * horizontal):(col * horizontal + horizontal)][:,:,0])# Red channel

        temp[row][col][1] = mean(image[(row * vertical):(row * vertical + vertical),
        (col * horizontal):(col * horizontal + horizontal)][:,:,1])# Green channel

        temp[row][col][2] = mean(image[(row * vertical):(row * vertical + vertical),
        (col * horizontal):(col * horizontal + horizontal)][:,:,2])# Blue channel

  return temp


def grayscale(image):
    """ Description:
            Converts the image to a grayscaled version.

        Args:
            image (numpy.ndarray): The image to be grayscaled. (RGB)

        Returns:
            temp (numpy.ndraray): grayscaled image.

            False: If the operation is not successful
    """

    height = len(image)
    width = len(image[0])

    img_dim = len(image.shape)

    if img_dim is not 2:
      temp = zeros([height, width], dtype = 'uint64')
    else:
      print("Operation wasn't successful, input is already monocolored.")
      return False

    for row in range(height):
      for col in range(width):
        temp[row][col] = mean(image[row][col])

    return temp


def SVD_compressor(image, factor_perc):
    """ Description:
            This function uses singular value decompositon to compress images.

        Args:
            image (numpy.ndarray): The image to be compressed.

            factor_perc (float / int): In singular value decompositon the matrix
            is splitted into 3 matrices U, S and V. U is M x K, S is K x K and
            V is K x N. This argument is used for shrinking K by this percentage.

        Returns:
            temp (numpy.ndraray): grayscaled image.
    """
    height = len(image)
    width = len(image[0])
    
    img_dim = len(image.shape)

    if img_dim is 2:
      U, S, V = svd(image, full_matrices=True)

      if factor_perc is 100:
        return dot(U, dot(diag(S), V))

      else:
        factored_S_len = len(S) * float(factor_perc) // 100

        U = transpose(transpose(U)[0:factored_S_len])
        S = S[0:factored_S_len]
        V = V[0:factored_S_len]

        return dot(U, dot(diag(S), V))

    elif img_dim is 3:
      U_red, S_red, V_red = svd(image[:,:,0], full_matrices=True)
      U_green, S_green, V_green = svd(image[:,:,1], full_matrices=True)
      U_blue, S_blue, V_blue = svd(image[:,:,2], full_matrices=True)

      if factor_perc is 100:
        return dstack((dot(U_red, dot(diag(S_red), V_red)),
                dot(U_green, dot(diag(S_green), V_green)),
                dot(U_blue, dot(diag(S_blue), V_blue))))
      else:
        factored_S_len = len(S_red) * factor_perc // 100

        U_red = transpose(transpose(U_red)[0:factored_S_len])
        S_red = S_red[0:factored_S_len]
        V_red = V_red[0:factored_S_len]
        print("Red")

        U_green = transpose(transpose(U_green)[0:factored_S_len])
        S_green = S_green[0:factored_S_len]
        V_green = V_green[0:factored_S_len]
        print("Green")

        U_blue = transpose(transpose(U_blue)[0:factored_S_len])
        S_blue = S_blue[0:factored_S_len]
        V_blue = V_blue[0:factored_S_len]
        print("Blue")

        return dstack((dot(U_red, dot(diag(S_red), V_red)),
                dot(U_green, dot(diag(S_green), V_green)),
                dot(U_blue, dot(diag(S_blue), V_blue))))

def shrink_by_elimination(image, vertical, horizontal):
  """ Description:
            This function shrinks images by deleting rows and columns.

        Args:
            image (numpy.ndarray): The image to be compressed.

            vertical (int): Vertical shrink ratio.

            horizontal (int): Horizontal shrink ratio.

        Returns:
            temp (numpy.ndraray): Shrinked image.
  """
  height = len(image)
  width = len(image[0])
  new_height = height // vertical
  new_width = width // horizontal
  img_dim = len(image.shape)
  temp = zeros([0], dtype='uint8')

  if img_dim is 3:
    temp = zeros([new_height, new_width, 3], dtype='uint8')
  elif img_dim is 2:
    temp = zeros([new_height, new_width], dtype='uint8')

  for col in range(new_height):
    for row in range(new_width):
  	  temp[col][row] = image[col * vertical][row * horizontal]
  return temp

def self_dot_transpose(image):
  red = dot(image[0], transpose(image[0]))
  green = dot(image[1], transpose(image[1]))
  blue = dot(image[2], transpose(image[2]))
  return dstack((red, green, blue))



def main():
  for i in range(1, 23):
    file_name = str(i)
    img = imread('../ayrik_notlari/' + file_name + ".jpg")
    new_img = shrink_by_elimination(img, 2, 2)
    height = len(new_img)
    width = len(new_img[0])
    if height < width:
  	  new_img = rot90(new_img, k=3)
    imsave('../ayrik_notlari/' + file_name + '_out.jpg', new_img)
    print('Image ' + str(i) + ' is saved...')

if __name__ == '__main__':
  main()


