# YouTube Face DataSet Backdoor Detection

This project is a solution for the instructions/challenge mentioned in [CSAW-HackML-2020](https://github.com/csaw-hackml/CSAW-HackML-2020). This is 
a part of the final project for the course ECE-GY 9163 at NYU. 

### Running the prediction on test data.

<hr>

```
python eval.py data/clean_test_data.h5 models/sunglasses_bd_net.h5 models/VAE.h5
```


### Background for the VAE Method

<hr>
Autoencoder is a type of Neural Network that is trained to copy its input to the output.  For example, given an image of a handwritten digit, an autoencoder first encodes the image into a lower dimensional latent representation, then decodes the latent representation back to an image. An autoencoder learns to compress the data to learn only the important features which are needed to predict a valid output successfully. A Variational Autoencoder encodes images belonging to the same class as E1 whereas an autoencoder would have encoded different images of the same class as E1 and E2. The difference arises when we add the mean and the variance dense layers as the innermost layers in our system which keep all the classes (1283) around 0. 


<br>
<br>

We leverage this property of variational autoencoders to make it learn only the features from the clean validation dataset. Then we compare the reconstruction cost of the original training data with the input data. In the case of the poisoned data we see that the reconstruction loss is more than the clean image data. This is because the model learned only the features from the clean data. This makes us distinguish between a poisoned image and a clean image.
We can see in the following images the difference between two sample poisoned images, i.e., sunglasses and eyebrows and their corresponding reconstructed images from the vae model.


The Autoencoder used here is a deep net with 1000 (based on experimentation) latent dimensions and it is trained using the Mean Absolute Error loss function and the Adam optimizer. The determiner for the poisoned (outlier) is a threshold which is chosen on the clean validation data as follows. We take the mean of the loss and then select the threshold as one value above the standard deviation.
<br><br>
```
Reconstruction_Loss_Threshold_X = Mean_X + S.T.D_X
```

This loss value comes out to be roughly in the range of 0.08 - 0.10. When compared with the reconstruction loss for the poisoned data set, we can see that it is distinctively low as mentioned in the table below.

```
Clean Data Threshold - 0.097 
Poisoned Sunglasses - 0.19903521 
Anonymous Data - 0.10617878  
Multi Trigger Sunglasses - 0.19900116 
Multi Trigger Eyebrows - 0.11117971  
Multi Trigger Lipstick - 0.106178075 
```

### References

1. [https://www.tensorflow.org/model_optimization/guide/pruning/pruning_with_keras](https://www.tensorflow.org/model_optimization/guide/pruning/pruning_with_keras)<br>
2. [https://www.tensorflow.org/tutorials/generative/autoencoder](https://www.tensorflow.org/tutorials/generative/autoencoder)<br>
3. [https://blog.keras.io/building-autoencoders-in-keras.html](https://blog.keras.io/building-autoencoders-in-keras.html)<br>
4. [https://blog.paperspace.com/how-to-build-variational-autoencoder-keras](https://blog.paperspace.com/how-to-build-variational-autoencoder-keras)<br>
