import numpy as np
import cv2
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from skimage.filters import difference_of_gaussians, window, gaussian

def normalize_img(image):
    return (((image - np.min(image)) / (np.max(image) - np.min(image)))*255.0).astype('uint8')

def blend(image1, image2, mask):

    initial_sigma = 10
    sigma1=[0,1,2,4,8,16]
    sigma2=[1,2,4,8,16,32]
    # 
    laplacian_images_image1=[]
    laplacian_images_image2=[]
    # difference of gaussian stack for image1
    for i in range(len(sigma1)):
      laplacian_images_image1.append(difference_of_gaussians(image1,initial_sigma*sigma1[i],initial_sigma*sigma2[i],mode='reflect'))
    
    # difference of gaussian stack for image2
    for i in range(len(sigma1)):
      laplacian_images_image2.append(difference_of_gaussians(image2,initial_sigma*sigma1[i],initial_sigma*sigma2[i],mode='reflect'))
     
    # mask
    masks=[]
    for i in range(len(sigma2)):
      masks.append(gaussian(mask,initial_sigma*sigma2[i],multichannel=True))

    # Blending
    out_images=[]
    for i in range(len(masks)):
      out_images.append(laplacian_images_image1[i]*masks[i]+(1-masks[i])*laplacian_images_image2[i])
    Blended_image=out_images[0]
    for i in range(1,len(out_images)):
      Blended_image+=out_images[i]   
    Blended_image = normalize_img(Blended_image)

    return Blended_image
