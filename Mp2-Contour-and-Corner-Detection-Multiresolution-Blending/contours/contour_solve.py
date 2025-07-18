import numpy as np
from scipy import signal
import cv2
from scipy import ndimage
from scipy import signal
import math
def smoothing(image, sigma, dirrection):
    w = 7
    t = (((w - 1)/2)-0.5)/sigma
    smoothed = ndimage.gaussian_filter(image, sigma,truncate=t)
    derivative=np.array([[-1,0,1]])
    if dirrection==0:
        smoothed_edge=signal.convolve2d(smoothed,derivative,mode='same',boundary="symm")
    else:
        smoothed_edge=signal.convolve2d(smoothed,derivative.T,mode='same',boundary="symm")
    return smoothed_edge
# def NMS(img, grad_x,grad_y):
#     grad_mag = np.sqrt(grad_x**2 + grad_y**2)
#     grad_orient = np.arctan2(grad_y, grad_x) * (180 / np.pi)
#     nms = np.zeros_like(img)
#     M, N = nms.shape
#     for i in range(1,M-1):
#         for j in range(1,N-1):
#             mag1=255
#             mag2=255
#             if grad_orient[i, j] >= -22.5 and grad_orient[i, j] < 22.5:
#                 # Edge is in the horizontal direction
#                 mag1 = grad_mag[i, j+1]
#                 mag2 = grad_mag[i, j-1]
#             elif grad_orient[i, j] >= 22.5 and grad_orient[i, j] < 67.5:
#                 # Edge is in the diagonal direction
#                 mag1 = grad_mag[i+1, j-1]
#                 mag2 = grad_mag[i-1, j+1]
#             elif grad_orient[i, j] >= 67.5 and grad_orient[i, j] <= 90.0 or grad_orient[i, j] < -67.5 and grad_orient[i, j] >= -90.0:
#                 # Edge is in the vertical direction
#                 mag1 = grad_mag[i+1, j]
#                 mag2 = grad_mag[i-1, j]
#             else:
#                 # Edge is in the other diagonal direction
#                 mag1 = grad_mag[i-1, j-1]
#                 mag2 = grad_mag[i+1, j+1]
#             if grad_mag[i, j] >= mag1 and grad_mag[i, j] >= mag2:
#                 nms[i, j] = grad_mag[i, j]
#             else:
#                 nms[i, j] = 0    
#     return nms 
def NMS(img, grad_x,grad_y,sigma):
  """Returns the norm of dx and dy as the edge response function."""
  
  """ Derivative Gaussian Filter """
  grad_mag = np.sqrt(grad_x**2 + grad_y**2)
  grad_mag = grad_mag / np.max(grad_mag)
  grad_orient = np.arctan2(grad_y, grad_x) 
  grad_orient[grad_orient < 0] += math.pi
  grad_orient = grad_orient*180/math.pi
  nms = np.zeros_like(img)
  

  """ Non-maximum Suppression """
  threshold = 0
  for y in range(1, grad_mag.shape[0]-1):
      for x in range(1, grad_mag.shape[1]-1):
          if grad_mag[y][x] > threshold:
              angle = grad_orient[y][x]
              if (0 <= angle < 45):
                  w = abs(grad_y[y][x])/abs(grad_x[y][x])
                  p = w * grad_mag[y-1][x-1] + (1-w) * grad_mag[y][x-1]
                  r = w * grad_mag[y+1][x+1] + (1-w) * grad_mag[y][x+1]

              elif (45 <= angle <= 90):
                  w = abs(grad_x[y][x])/abs(grad_y[y][x])
                  p = w * grad_mag[y-1][x-1] + (1-w) * grad_mag[y-1][x]
                  r = w * grad_mag[y+1][x+1] + (1-w) * grad_mag[y+1][x]

              elif (90 < angle < 135):
                  w = abs(grad_x[y][x])/abs(grad_y[y][x])
                  p = w * grad_mag[y-1][x+1] + (1-w) * grad_mag[y-1][x]
                  r = w * grad_mag[y+1][x-1] + (1-w) * grad_mag[y+1][x]

              elif (135 <= angle <= 180):
                  w = abs(grad_y[y][x])/abs(grad_x[y][x])
                  p = w * grad_mag[y-1][x+1] + (1-w) * grad_mag[y][x+1]
                  r = w * grad_mag[y+1][x-1] + (1-w) * grad_mag[y][x-1]
              if grad_mag[y][x] >= p and grad_mag[y][x] >= r:
                  nms[y][x] = grad_mag[y][x]
                  continue
              else:
                  #grad_mag[y][x] = 0
                  nms[y][x] = 0
  return nms
def bells_and_whistles(input, dirrection): 
    fil = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1]]) #For bells and whistle 1
    #fil = np.array([[1, 1, 1, 1, 0, 1, 1, 1, 1]]) #For bells and whistle 2
    filters = [np.dot(fil.T, fil), np.array([[-1, 0, 1.]])]
    if dirrection:
        filters = [filter.T for filter in filters]
    for filter in filters:
        input = signal.convolve2d(input, filter, mode='same', boundary='symm')
    return input       
def compute_edges_dxdy(I):
  """Returns the norm of dx and dy as the edge response function."""
  I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
  I = I.astype(np.float32)/255.
  sigma = 20
  dx = smoothing(I, sigma, 0)
  dy = smoothing(I, sigma, 1)
  # dx = bells_and_whistles(I, 0)
  # dy = bells_and_whistles(I, 1)
  mag = NMS(I,dx,dy,sigma)
  mag = mag / mag.max() * 255
  mag = np.clip(mag, 0, 255)
  mag = mag.astype(np.uint8)
  return mag
  