# Code from Saurabh Gupta
import cv2
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import numpy as np
from absl import app, flags

from blend_mine_solve import blend

FLAGS = flags.FLAGS
flags.DEFINE_string('im1', 'fish.jpeg', 'image 1')
flags.DEFINE_string('im2', 'dog.jpeg', 'image 2')
flags.DEFINE_string('mask', 'mask1.png', 'mask image')
flags.DEFINE_string('out_name', 'output1.png', 'output image name')

def main(_):
  I1 = cv2.imread(FLAGS.im1)
  I2 = cv2.imread(FLAGS.im2)
  I1=cv2.resize(I1, (3000, 3000))
  I2=cv2.resize(I2, (3000, 3000))
  print(I1.shape)
  print(I2.shape)
  mask = cv2.imread(FLAGS.mask)
  mask=cv2.resize(mask, (3000, 3000))
  print(mask.shape)
  out = blend(I2, I1, mask)
  # save image
  cv2.imwrite(FLAGS.out_name, out)

if __name__ == '__main__':
  app.run(main)
