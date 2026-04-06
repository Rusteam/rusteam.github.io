---
title: "It’s Possible to Win ML Hackathon if You Ranked 2nd on Leaderboard"
date: 2019-04-24
slug: "win-ml-hackathon"
canonicalURL: "https://medium.com/@rustemgal/its-possible-to-win-ml-hackathon-if-you-ranked-2nd-on-leaderboard-2b82a23474ea"
author: "Rustem G"
---

Even though a high accuracy model is crucial in machine learning, we still have to remember we’re building models for end users.

---

In machine learning, a high accuracy model is a key for success. Nonetheless, models are build for end users. This story will tell you how an end user perspective can add valuable points to succeeding in data science.

#### Intro

A few weeks ago we took part in a machine learning hackathon hosted by [Skoltech research institution](https://www.skoltech.ru/en/). It took place in our amazing hometown Kazan in Russia and lasted almost 2 days. Definitely check out this nice portal about our home region below.

[Visit Tatarstan - The Official Tourist Portal of the Republic of TatarstanWalk Like a Local. 5 Ways to Experience Kazan From the Inside More about the guidebook 100 Visit Tatarstan souvenirs to…visit-tatarstan.com](https://visit-tatarstan.com/en/)

Note: spoilers ahead. We ranked the second on the private leaderboard but we still won it, and I’m going to tell you how.

#### Hackathon Overview

The hackathon had three tracks:

1. Web-based labelling tool for doctors
2. Machine learning algorithm to classify types of epilepsy
3. Open track for any solutions within the AI in Medicine domain

As data scientists, we unsurprisingly picked the second track.

#### Problem Description

The task was two-fold:

1. Build a model that would correctly classify 8 types of epilepsy from brain EEG signals.
2. Build a web-app that inputs a file and spits out a prediction for an end user.

![Table 1. Types of Epilepsy Seizures](https://cdn-images-1.medium.com/max/1200/1*s_AhhPXvsqBoI57JgOJl9Q.png)

**Table 1. Types of Epilepsy Seizures**

There were 2012 observations collected from patients that had suffered an epilepsy seizure. Each observation contained time-based samples and preprocessed using two popular methods. More details on data preprocessing in [this paper](https://arxiv.org/pdf/1902.01012.pdf).

![Figure 1. Raw EEG Signals (tribute to WikiMedia Commons)](https://cdn-images-1.medium.com/max/1200/1*-yc4fZIGnF57oDEogq0tLQ.png)

**Figure 1. Raw EEG Signals (tribute to WikiMedia Commons)**

After preprocessing, we received two files per each observation:

1. 3-dimensional array of shape [Number of Samples, Number of Channels, Number of Frequencies]
2. 2-dimensional array of shape [Number of Samples, Number of Frequencies]

#### Benchmark

The testing protocol was mean weighted F1-score on 5-fold cross-validation split on a file-level, i.e. files are split into five folds, only then they must be parsed, because samples within one file are highly correlated. If you’re wondering how to compute cross-validated F1-weighted score, here’s python code for that:

```
import numpy as np  
from sklearn.metrics import f1_score  
# assuming you have fold-wise true labels and predicted labels   
# as a list of tuples  
val_scores = [f1_score(true_labels, predicted_labels, average=”weighted”) for true_labels,predicted_labels in fold_labels_and_predictions)]  
mean_f1 = np.mean(val_scores)
```

The authors of the paper took eigenvalues of matrices on sample-level and trained various classifiers, among which K-Nearest Neighbors beat other algorithms. They were able to reach 88.4% score using method 1 and 90.7% using method 2.

#### Leaderboard

As for the leaderboard, our local 5-fold CV served as a proxy for the public score. As for the private scores, we would find out them only after demoing our solutions.

However, there was a very important note from the host in the beginning. Teams with highest scores would be ranked not only by private scores, but also by the quality of a web-app.

#### Neural Net

We decided to use a Convolutional Neural Network since many researchers proved it to be a good fit for a seizure detection tasks. Also, we figured that EEG signals collection process is impacted by a topology of placing scanners on a human head. Luckily, the first type of preprocessing provided suitable inputs for 2D convolutions.

#### Architectures

We tried out different backbones for our convnet:

* pretrained Imagenet models (ResNet18, VGG11)
* Imagenet architecture with random weights (also ResNet18, VGG11)
* a simple CNN from scratch

Obviously, models pretrained on Imagenet didn’t perform well as inputs had nothing in common. ResNet and VGG architectures with random weights didn’t outperform a simple convnet as well. I tie this to the fact that spatial dimensions of our input are quite small (20 pixels in height and 24 pixels in width), whereas first convolutional layer of these models have a filter size of 7. We end up with a bunch of lost signal and sometimes with negative output dimensions (as with AlexNet).

That being said, after long-lasting experimentation we settled with this tiny model:

* 3 blocks of convolution, leaky ReLU, batch normalization and max pooling
* 1 block of convolution, leaky ReLU and batch normalization
* 1 fully-connected layer

![Figure 2. Our CNN Architecture](https://cdn-images-1.medium.com/max/1200/1*cj3roffXzxhQaBt8rznVxw.png)

**Figure 2. Our CNN Architecture**

#### Inputs

Since we used a dataset of the method 1 preprocessing, our inputs were of shape [num\_samples, 20, 24], whereas num\_samples could range from 3 to over 100. Thus, we tried different inputs:

* a random window of consecutive samples with window size being equal to 1, 3, 5 and 10
* mean value across all samples, i.e. input shape is [1, 20, 24]
* adding standard deviation, maximum, minimum along with mean
* adding 10-th, 25-th, 50-th, 75-th and 90-th percentiles along with mean

No long talks, a random window didn’t work at all. So, we took average across all samples and training got much more interesting, we reached almost **90%** in our metric. Adding other statistical measures didn’t seem to help, usually our score went down. However, 25-th and 75-th percentiles gave us **1%** boost, and we kept them making our input of shape [3, 20, 24].

#### Training Results

A few iterations and we figured out that *Adam* optimizer with learning rate between *0.002* and *0.005* gave us highest performance adding extra **1%** in the cross-validation scores. Each fold was trained for *40* epochs.

Final local performance was measured as an average over all 5 folds. We hit **92.39%** with one-fold maximum at **93.71%**. After all teams demoed their results, we were on the second place, **1%** behind the leader.

Upon releasing private scores, our performance jumped to **94.5%**. Sadly, we remained **1%** behind.

#### Web App

Now, you should remember that there was one more criterion to winning. Yes, a web application where a doctor can submit a file and get a prediction.

![Table 2. Sample Model Output](https://cdn-images-1.medium.com/max/1200/1*tqNwg1ahzx-OFFrL0ojLsA.png)

Table 2. Sample Model Output

We decided to split efforts to develop a nifty [web application form](https://deepl.herokuapp.com/). Don’t hesitate to download a few example files from our [drive](https://drive.google.com/file/d/13izID-COxJMEefORIZiDObVPyY6qPOo3/view?usp=sharing) to test this form. It’s easy. Just upload one or few files to get predictions for each file. You can also download predictions as a CSV file.

#### Model Interpretability

I hope you’ve spent a minute to check out our app. Provided you have, you should have noticed an unusual chart like the one below.

![Figure 3. Grad-CAM Output Interpretation](https://cdn-images-1.medium.com/max/1200/1*Rra6ty645q7kOer3o_x_fg.png)

**Figure 3. Grad-CAM Output Interpretation**

We recalled that in medicine it’s important not only have a very high precision, but also a succinct explanation. That’s why we spent time to bring [Gradient-weighted Class Activation Mapping](http://gradcam.cloudcv.org/) to give our users a tool to explain why our model makes any of its decisions. Shortly, it uses a class prediction, backpropagated gradients and class activation maps to point out areas of interest on the input.

That’s how we get these two images above. The left one is a heatmap of means across samples a.k.a. input matrix, the right one is output of the Grad-CAM algorithm drawing a doctor’s attention to most influential input values.

#### Winning Solution

Well, that’s whole secret sauce of ours. We blended high accuracy model with a simple yet complete web-app and flavored everything with visual model interpretation. Even though, we were runner-ups in terms of weighted F1-score, the hackathon jury appreciated the fact that we considered how doctors could use this solution most efficiently.

Also, we utilized lessons learnt from a previous hackathon that it was quite important to have a unite team to work on one problem only. We had a good mix of specialties and didn’t waste our limited time and energy on other tasks.

**More about Team**

* I (Rustem Galiullin) — machine learning researcher — worked on a model performance.
* Almaz Melnikov — machine learning engineer — filled our web-app with functionality and integrated our neural net.
* Konstantin Yarushkin — front-end developer — developed a template for our web-app.

![Our smiley faces after winning](https://cdn-images-1.medium.com/max/1200/1*ArJa3yCLyOMHgh-m2X-wJg.jpeg)

Our smiley faces after winning

#### Resources

1. Project web-app <https://deepl.herokuapp.com/>
2. Our gitlab repo <https://gitlab.com/MelnikovAlmaz/epilepticsearch.git>
3. Grad-CAM implementation in pytorch <https://github.com/jacobgil/pytorch-grad-cam>
4. Grad-CAM project <http://gradcam.cloudcv.org/>
5. About Skoltech <https://www.skoltech.ru/en>
