import numpy as np
from scipy import signal
import cv2
from scipy import ndimage
from scipy import signal
import math
def smoothing(image, sigma, direction):
    w = 7
    t = (((w - 1)/2)-0.5)/sigma
    smoothed = ndimage.gaussian_filter(image, sigma,truncate=t)
    derivative=np.array([[-1,0,1]])
    if direction==0:
        smoothed_edge=signal.convolve2d(smoothed,derivative,mode='same',boundary="symm")
    else:
        smoothed_edge=signal.convolve2d(smoothed,derivative.T,mode='same',boundary="symm")
    return smoothed_edge
def compute_edges_dxdy(I):
  """Returns the norm of dx and dy as the edge response function."""
  I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
  I = I.astype(np.float32)/255.
  sigma = 20
  dx = smoothing(I, sigma, 0)
  dy = smoothing(I, sigma, 1)
  mag = np.sqrt(dx**2 + dy**2)
  mag = mag * 255.
  mag = np.clip(mag, 0, 255)
  mag = mag.astype(np.uint8)
  return mag
