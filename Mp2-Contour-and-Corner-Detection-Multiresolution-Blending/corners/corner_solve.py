import numpy as np
import scipy
from scipy import signal
import cv2

# def non_max_suppression(harris_response, window_size=3):
#     """
#     Applies non-maximum suppression to the Harris corner response image.
#     """
#     harris_response = harris_response.copy()  # Make a copy of the response image to avoid modifying the original.
#     # Set all values below the threshold to zero.
#     #harris_response[harris_response < threshold] = 0
#     # Get the coordinates of the non-zero elements in the response image.
#     coords = np.argwhere(harris_response)
#     # Set up a window around each coordinate.
#     window_half_size = (window_size - 1) // 2
#     for r, c in coords:
#         window = harris_response[max(r - window_half_size, 0):r + window_half_size + 1,
#                                  max(c - window_half_size, 0):c + window_half_size + 1]
#         # Check if the current pixel is the maximum in its neighborhood.
#         if harris_response[r, c] == window.max():
#             continue  # Keep this pixel as a corner.
#         else:
#             harris_response[r, c] = 0  # Suppress this pixel.
#     return harris_response
def non_max_suppression(response, w_size=3):
    """
    Applies non-maximum suppression to the Harris corner response image.
    """
    harris_res = response.copy()

    # Get the coordinates of the non-zero elements in the response image.
    for h in range(0, response.shape[0]):
      for w in range(0, response.shape[1]):
          for i in range(max(0, h - w_size), min(h + w_size + 1, response.shape[0])):
              for j in range(max(0, w - w_size), min(w + w_size + 1, response.shape[1])):
                  if response[i, j] > response[h, w]:
                      harris_res[h, w] = 0
    return harris_res    
def image_derivative(image,dir):
    derivative_filter=np.array([[-1,0,1]])
    if dir==0:
        img_derivative=signal.convolve2d(image,derivative_filter,mode='same',boundary="symm")
    else:
        img_derivative=signal.convolve2d(image,derivative_filter.T,mode='same',boundary="symm")
    return img_derivative
def gauss_fil_conv(img):
    img = scipy.ndimage.gaussian_filter(img, 0.55, order=0, output=None, mode='reflect')
    return img    
def compute_corners(I):
  # Currently this code proudces a dummy corners and a dummy corner response
  # map, just to illustrate how the code works. Your task will be to fill this
  # in with code that actually implements the Harris corner detector. You
  # should return the corner response map, and the non-max suppressed corners.
  # Input:
  #   I: input image, H x W x 3 BGR image
  # Output:
  #   response: H x W response map in uint8 format
  #   corners: H x W map in uint8 format _after_ non-max suppression. Each
  #   pixel stores the score for being a corner. Non-max suppressed pixels
  #   should have a low / zero-score.
  alpha = 0.04
  gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY ) #cv2.cvtColor(I,)
  gray=gray/255.0
  Ix = image_derivative(gray, 0)
  Iy = image_derivative(gray, 1)
  Ix_sq=Ix**2
  Iy_sq=Iy**2
  Ixy=Ix*Iy
  gauss_fil_Ix=gauss_fil_conv(Ix_sq)
  gauss_fil_Iy=gauss_fil_conv(Iy_sq)
  gauss_fil_Ixy=gauss_fil_conv(Ixy)
  response = gauss_fil_Ix*gauss_fil_Iy - gauss_fil_Ixy**2 - alpha*(gauss_fil_Ix + gauss_fil_Iy)**2
  response = response / response.max() * 255
  corners=non_max_suppression(response)
  corners = corners.astype(np.uint8)                                         
  response = response.astype(np.uint8)
  return response, corners

  #scipy rankfilter
  
