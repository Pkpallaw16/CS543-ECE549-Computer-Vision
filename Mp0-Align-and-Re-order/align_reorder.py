import os
import imageio
import numpy as np
from absl import flags, app
import reorder
import sys

FLAGS = flags.FLAGS
flags.DEFINE_string('test_name_hard', 'hard_almastatue', 
                    'what set of shreads to load')


def load_imgs(name):
    file_names = os.listdir(os.path.join('shredded-images', name))
    file_names.sort()
    Is = []
    for f in file_names:
        I = imageio.v2.imread(os.path.join('shredded-images', name, f))
        Is.append(I)
    return Is
def distance_(ig1,ig2):
    dist=[]
    ig1_mean=ig1.mean(axis=1)
    ig2_mean=ig2.mean(axis=1)
    std_ig1=ig1.std(axis=1)
    std_ig2=ig2.std(axis=1)
    for pt in range(ig1.shape[0]):
        ig1_=(ig1[pt,:,:]-ig1_mean[pt,:])/(std_ig1[pt,:])
        ig2_ = (ig2[pt, :, :] - ig2_mean[pt, :]) / (std_ig2[pt, :])
        s=ig1_*ig2_
        dist.append(s.sum())
    return dist

def solve(Is):
    '''
    :param Is: list of N images
    :return order: order list of N images
    :return offsets: offset list of N ordered images
    '''
    # order = [0, 24, 2, 9, 6, 16, 3, 5, 19, 7, 1, 21, 10, 11, 25, 15, 14, 13, 4,
    #          18, 23, 20, 17, 22, 8, 12]
    # offsets = [120, 3, 27, 37, 58, 23, 55, 67, 53, 16, 35, 84, 2, 33, 121, 67,
    #            53, 79, 60, 61, 18, 101, 104, 0, 108, 98]

    # We are returning the order and offsets that will work for 
    # hard_almastatue, you need to write code that works in general for any given
    # Is. Use the solution for hard_almastatue to understand the format for
    # what you need to return
    n_stripes = len(Is)
    distances = -np.inf*np.ones((n_stripes, n_stripes))
    max_ht = max([image.shape[0] for image in Is])
    offsets_mat = -np.inf*np.ones((n_stripes, n_stripes))
    max_slide=int(0.20*max_ht)
    for i in range(n_stripes):
        image1=Is[i][:,0,:]
        for j in range(n_stripes):
            if i == j:
                continue
            image2 = Is[j][:,-1,:]
            h1= image1.shape[0]
            h2= image2.shape[0]
            dist=[]
            offsets=[]
            slide_image1=np.zeros([max_slide*2+1,max_ht,3])
            slide_image2=np.zeros([max_slide*2+1,max_ht,3])
            count=0
            for k in range(-max_slide, max_slide + 1):
                offsets.append(k)
                if k >= 0:
                    base_im=min(image2.shape[0],h1-k)
                    slide_image1[count,:base_im,:]=image1[k:base_im+k]
                    slide_image2[count, :base_im, :] = image2[:base_im]
                else:
                    k=abs(k)
                    base_im=min(image1.shape[0],h2-k)
                    slide_image1[count, :base_im, :] = image1[:base_im ]
                    slide_image2[count, :base_im, :] = image2[k:base_im + k]
                count+=1

            dist = distance_(slide_image1,slide_image2)
            distances[i,j] = max(dist)
            offsets_mat[i,j]=offsets[np.argmax(dist)]
    index=np.arange(n_stripes)
    order=[0]
    for i in range(n_stripes-1):
        dis1=np.max(distances[0,1:])
        dis2=np.max(distances[1:,0])
        if dis1>dis2:
            idx = np.argmax(distances[0,1:]) + 1
            order.insert(0,index[idx])
            distances[0,:]=distances[idx,:]
            distances=np.delete(distances,idx,0)
            distances = np.delete(distances, idx, 1)
            index = np.delete(index, idx, 0)
        else:
            idx = np.argmax(distances[1:,0]) + 1
            order.append(index[idx])
            distances[:,0] = distances[:,idx]
            distances = np.delete(distances, idx, 0)
            distances = np.delete(distances, idx, 1)
            index = np.delete(index, idx, 0)
    offset=[0]
    for n in range(0,len(order)-1):
        image_bf=order[n]
        image_af=order[n+1]
        img1_img2=int(offsets_mat[image_af,image_bf])
        if img1_img2>0:
            offset.append(offset[n]-img1_img2)
        else:
            offset.append(offset[n]+abs(img1_img2))
    start=abs(min(offset))
    offset=[value +start for value in offset]
    return order, offset


def composite(Is, order, offsets):
    Is = [Is[o] for o in order]
    strip_width = 1
    W = np.sum([I.shape[1] for I in Is]) + len(Is) * strip_width
    H = np.max([I.shape[0] + o for I, o in zip(Is, offsets)])
    H = int(H)
    W = int(W)
    I_out = np.ones((H, W, 3), dtype=np.uint8) * 255
    w = 0
    for I, o in zip(Is, offsets):
        I_out[o:o + I.shape[0], w:w + I.shape[1], :] = I
        w = w + I.shape[1] + strip_width
    return I_out

def main(_):
    Is = load_imgs(FLAGS.test_name_hard)
    order, offsets = solve(Is)
    I = composite(Is, order, offsets)
    import matplotlib.pyplot as plt
    plt.imshow(I)
    plt.show()

if __name__ == '__main__':
    app.run(main)
