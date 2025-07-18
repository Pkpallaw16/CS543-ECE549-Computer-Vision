## ECE549 / CS543 Computer Vision: Assignment 4

### Instructions 

### Google Colab and Dataset setup
In this assignment you will use [PyTorch](https://pytorch.org/), which is currently one of the most popular
deep learning frameworks and is very easy to pick up. It has a lot of tutorials and an active community answering
questions on its discussion forums. You will be using [Google Colab](https://colab.research.google.com/), a free environment
to run your experiments. Here are instructions on how to get started:

1. Login with your Illinois Google account. Note: you will not have access to starter codes using account outside
the illinois.edu domain.

2. Open [Q1 Starter code](https://colab.research.google.com/drive/1En8AhKA2ZkT5nH4GBGsTR3zvhWtgr8S9) and 
[Q2 Starter code](https://colab.research.google.com/drive/1ubrsqkDfLo2alHupBAkZws4NmzPvSWXO),
click on File in the top left corner and select `Save a copy in Drive`.
This should create a new notebook, and then click on `Runtime → Change Runtime Type → Select GPU as
your hardware accelerator`. Make sure you copy both Q1 and Q2 to your Drive.

3. Follow the instructions in the notebook to finish the setup.

4. Keep in mind that you need to keep your browser window open while running Colab. Colab does not allow
long-running jobs but it should be sufficient for the requirements of this assignment.

### Problems

1. **Implement and improve BaseNet on FashionMNIST [30 pts].** For this part of the assignment, you will be working with
    the [FashionMNIST](https://github.com/zalandoresearch/fashion-mnist) dataset. This dataset consists of 60K 28 × 28 color images from 10 classes. The images in FashionMNIST are in grayscale of size 28 × 28.

    <div align="center"> <img src="fashion-mnist.png" width="50%"> </div>

    1. **Implement BaseNet [5 pts].** Implement the BaseNet with the neural network shown below.
       The starter code for this is in the BaseNet class. After implementing
       the BaseNet class, you can run the code with default settings to get a
       baseline accuracy of around 80% on the validation set. The BaseNet is
       built with following components:
       * Convolutional, i.e. `nn.Conv2d`
       * Pooling, e.g. `nn.MaxPool2d`
       * Fully-connected (linear), i.e. `nn.Linear`
       * Non-linear activations, e.g. `nn.ReLU`
       BaseNet consists of two convolutional modules (conv-relu-maxpool) and
       two linear layers. The precise architecture is defined below:

       | Layer No.   | Layer Type  | Kernel Size | Input Dim   | Output Dim  | Input Channels | Output Channels |
         | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
         | 1 | conv2d | 5 | 28 | 24 | 1 | 6 |
         | 2 | relu | - | 24 | 24 | 6 | 6 |
         | 3 | maxpool2d | 2 | 24 | 12 | 6 | 6 |
         | 4 | conv2d | 5 | 12 | 8 | 6 | 12 |
         | 5 | relu | - | 8 | 8 | 12 | 12 |
         | 6 | maxpool2d | 2 | 8 | 4 | 12 | 12 |
         | 7 | linear | - | 1 | 1 | 192 | 12 |
         | 8 | relu | - | 1 | 1 | 12 | 12 |
         | 9 | linear | - | 1 | 1 | 12 | 10 |

       **In your report, include:** your model by using Python print command
       `print(net)` and final accuracy on the validation set.

    2. **Improve BaseNet [5 pts].** 
       Your goal is to edit the BaseNet class or make new classes for devising
       a more accurate deep net architecture.  In your report, you will need to
       include a table similar to the one above to illustrate your final
       network.
       
       Before you design your own architecture, you should start by getting
       familiar with the BaseNet architecture already provided, the meaning of
       hyper-parameters and the function of each layer. This
       [tutorial](https://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html)
       by PyTorch is helpful for gearing up on using deep nets. Also, see
       Andrej Karpathy's lectures on
       [CNNs](http://cs231n.github.io/convolutional-networks/) and [neural
       network training](http://cs231n.github.io/neural-networks-3/).

       For improving the network, you should consider the following aspects.
       In addition, you can also try out your own ideas. Since Colab makes only
       limited computational resources available, we encourage you to
       rationally limit training time and model size. *Do not simply just copy
       over model architectures from the Internet.*

       * **Data normalization.** Normalizing input data makes training easier
       and more robust. You can normalize the data to made it zero mean and fixed standard
       deviation ($`\sigma = 1`$ is the go-to choice).  You may use
       `transforms.Normalize()` with the right parameters for this data
       normalization. After your edits, make sure that `test_transform` has the
       same data normalization parameters as `train_transform`.
       * **Data augmentation.** Augment the training data using random crops,
       horizontal flips, etc. You may find functions `transforms.RandomCrop()`,
       `transforms.RandomHorizontalFlip()` useful. Remember, you shouldn't
       augment data at test time. You may find the [PyTorch
       tutorial](https://pytorch.org/tutorials/beginner/data_loading_tutorial.html#transforms)
       on transforms useful.
       * **Deeper network.** Experiment by adding more convolutional and fully
       connected layers. Add more convolutional layers with increasing output
       channels and also add more linear (fully convolutional) layers.
       * **Normalization layers.** [Normalization
       layers](https://pytorch.org/docs/master/nn.html#normalization-functions)
       may help reduce overfitting and improve training of the model. Add
       normalization layers after conv layers (`nn.BatchNorm2d`). Add
       normalization layers after linear layers and experiment with inserting
       them before or after ReLU layers (`nn.BatchNorm1d`).

       **In your report, include:** 
       - Your best model. Include final accuracy on validation set, table
         defining your final architecture (similar to the BaseNet table above),
         training loss plot and test accuracy plot for final model
         (auto-generated by the notebook). A reasonable submission with more
         than 85% accuracy will be given full credit for this part.
       - An ablation table, listing all factors that you tried to make
         improvement to your final model as well as the corresponding validation 
         accuracy.

    3. **Secret test set [20 pts].** We also have a secret test set containing 2000 images similar to FashionMNIST. We provide code that loads [test data](https://drive.google.com/file/d/130ssD7hrrDLqQHKVD3luD0tXTedWjC8j/view?usp=share_link) and saves your model predictions to a
       `predictions.npy` file. Submit the prediction for your best model to
       gradescope. If you want, you can also show your scores on the class
       leaderboard, and challenge your classmates to beat you!  
       
       **We will give up to 3pts of extra credits to top-5 entries on the leaderboard!**

       **In your report, include:** Test set accuracy (category-wise and aggregate) 
       for your best model. You can get this from gradescope. A reasonable submission 
       with more than 90% accuracy will be given full credit for this part.


2. **Semantic Segmentation [40 pts].** In this part, you will build your own sementic segmentation on a subset of the [COCO-Stuff ](https://github.com/nightrome/cocostuff). This task comprises of classifying image pixels into the following 6 categories: background, sports, accessory, animal, vehicle, person. We will use the mean average precision (on the soft output) and mean intersection over union (of the hard output) to measure performance. We provide code for computing these metrics. 

    <div align="center">
    <img src="vis_gt.png" width="80%">
    </div>

    **Data.** We have 700 images for training, 100 images for validation, 100 images for testing. Each image is RGB with size 224 x 224. 

   #### Starter Code
   We provide dataset visualization, a dataloader, a basic model (that trains a linear classifier on top of the pixel value at each location) and a simple training cycle.

    **What you need to do:** 
    
    1. **Implement training cycle:** You will need to modify the provided simple training cycle. Make sure you evaluate metrics and loss on the validation set every so often to check for overfitting.

    2. **Build on top of ImageNet pre-trained Model [5 pts]:** Your task is 
         to build on top of a ResNet 18 ([1](#references)) model that has been 
         pre-trained on the ImageNet dataset ([2](#references)) (via
         `models.resnet18(pretrained=True)`). These models are trained to predict the
         1000 ImageNet object classes. To use this model for semantic segmentation, you
         will have to remove the classifier and global average pooling layers, and stack
         on additional layers for semantic segmentation. Note that, ResNet-18 model downsamples the input image by a factor of 32, remeber to upsample your prediction using bilinear
         interpolation. Carefully document the design choices you
         make in your report. Please indicate which hyper parameters you tried, along with
         their performance on the validation set. For reference, our very basic first implementation could achieve a mAP of **0.71** and a mIoU of
         **0.48** under 20 minutes of training of 20 epochs. At the very least your implementation
         should achieve as much accuracy on the validation set, but you may be able to
         do better with more training and hyper-parameters tuning.

         Here are some sample prediction outputs using ResNet-18 model.
       
       <div align="center"> <img src="vis_resnet18.png" width="100%"> </div>


         In your report, include: model architecture, how you implement upsampling, training details and final performance on validation set.


    3. **Improve model performance [5 pts]:** The current model
       simply replaces the final fully connected layer in a ResNet-18 model for
       semantic segmentation. This still has a lot of draw backs. The
       most important factors that causes poor performance is the low output
       resolution. ResNet-18 model for image classification downsamples the input
       image by a factor of 32. In the previous step, we recover the resolution by
       a simple bilinear interpolation layer which upsamples the prediction by 32
       times. In this part, our goal is to explore other choices to generate
       high-resolution predictions and improve segmentation performance:
       * **Atrous (or dilated) convolution.** The concept of atrous convolution 
         (or dilated convolution) is described it the DeepLab paper([3](#references)).
         One way to think about atrous convolution is to think of running the 
         network on shifted versions of the image and weaving the outputs together
         to produce an output at the original spatial resolution. This can be done
         simply by using the `dilataion` arguments in PyTorch. Refer to the paper([3](#references)) and PyTorch documentation for more detail. 

       * **Additional fully convolutional layer.**  
         you can add a fully convolutional decoder that learns to upsample and refine the model output from ResNet-18. Refer to the FCN([5](#references)) and DeepLabv3+([4](#references)) for
         more detail.

        You can implement either of these two choices, or other choices you
        find in other papers to improve the segmentation performance. Please describe the methods you try in your report and report their
        performance.  For reference, our implementation with a dilated ResNet-18 achieves AP **0.74** and IoU **0.52**.
        Our implementation of DeepLabv3
        decoder achieves AP **0.77** and IoU **0.55**. Your best model should achieve
        similar or higher performance. 

        Below is the performance of using dilated convolution in ResNet-18:

         <div align="center"> <img src="vis_resnet18_dilate.png" width="100%"> </div>
      
         Below is the performance of using DeepLabv3:

         <div align="center"> <img src="vis_deeplabv3_resnet18.png" width="100%"> </div>


       **In your report, include:**
         - Your best model an design choice. Include final performance on validation set.
         - An ablation table, listing all factors that you tried to make
         improvement to your final model as well as the validation performance.
         - visualization of model prediction on five of your favorite images from validation set. 


   4. **Secret test set [30 pts].** 
       The starter code produces predictions on the test set, writing to the file `Q2_sseg_predictions.npy`.  Upload the file `Q2_sseg_predictions.npy` for your best model on gradescope to have it graded. If you want, you can also show your scores on the class leaderboard, and challenge your classmates to beat you!  
       
       **We will give up to 4pts of extra credits to top-5 entries on the leaderboard!**

       **In your report, include:** test set accuracy of your best model. 
       You can get this from gradescope. A reasonable submission with average IoU more
      than 0.55 will be given full credit for this part.



#### References
1. Kaiming He et al. Deep residual
learning for image recognition. In CVPR 2016.
2. Jia Deng el al. A
large-scale hierarchical image database. In CVPR 2009.
3.  Liang-Chieh Chen et al. "Semantic image segmentation with deep convolutional nets and fully connected CRFs." ICLR 2015.
4. Liang-Chieh Chen et al. "Encoder-decoder with atrous separable convolution for semantic image segmentation." ECCV 2018.
5. Jonathan Long et al. "Fully convolutional networks for semantic segmentation." CVPR 2015.
