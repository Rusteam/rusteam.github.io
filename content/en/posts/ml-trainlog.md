---
title: "Keep a Trainlog for machine learning"
date: 2023-03-31
slug: "ml-trainlog"
canonicalURL: "https://medium.com/@rustemgal/keep-a-trainlog-8ee35553c0bd"
author: "Rustem G"
---

If you’re looking for a way to store a history of model changes, consider keeping a trainlog. Similar to a changelog, a trainlog is a…

---

If you’re looking for a way to store a history of model changes, consider keeping a trainlog. Similar to a changelog, a trainlog is a record of changes made to your model during the training process. This record can help you keep track of what changes were made, when they were made, and the results of those changes. It can also help you identify which changes led to improvements and which changes led to setbacks. I’ll share my own example at the bottom of this article.

I have taken a format and inspiration from [Keep a Changelog](https://keepachangelog.com) and the author’s interview at [The Changelog podcast](https://changelog.com/podcast/127).

#### What is a trainlog?

A trainlog is a *human-readable* record of results and changes to a machine learning model during the model development process. Similar to a changelog, it is a file which contains a curated, chronologically ordered list of notable changes for each iteration of the model development cycle.

#### Why keep a trainlog?

A trainlog can help you get a quick overview previous experiments and generate new ideas for improvement. It can also help you avoid repeating mistakes and build on successful strategies.

#### Who needs a trainlog?

As with a changelog, people do. A trainlog is useful for anyone invested in the development models. This includes data scientists, machine learning engineers, managers, and anyone else involved in the delivery of new models updates.

#### How do I make a good changelog?

1. Provide a short title for each iteration.
2. Records should be personal conclusions from analyzing results rather than a plain statement of facts.
3. Be concise: Record only the most relevant information.
4. Be organized: Use a consistent format and update your trainlog regularly.
5. Be transparent: Provide links to experiment tracking and model registry services to back up results.
6. Be collaborative: Share your trainlog with your team members and encourage feedback and input.

#### Guiding Principles

* Trainlogs are for humans, not machines.
* There should be an entry for every iteration.
* Records should be grouped.
* Conclusions should be linkable.
* The latest version comes first.
* The final date of each iteration is displayed.

#### Types of changes

* `Results` for iteration results.
* `Lessons learnt` for things that didn’t yield any improvement.
* `Ideas` for possible future improvements.
* Code changes can be recorded similar to a changelog (`added`, `changed`, `fixed`, etc.) and might include any notable changes in model architecture and evaluation, hyper-parameters, data or pre-processing techniques.

#### How can I reduce the effort required to maintain a trainlog?

Maintaining a trainlog can be time-consuming, but there are ways to reduce the effort required. Here are some tips:

1. Use automated tools: Consider using automated tools such as MLFlow, TensorBoard, or other experiment tracking tools to store logs your experiments and link to them.
2. Prioritize recording changes that have a significant impact on the model’s performance or that have a major impact on the development process.
3. Integrate your trainlog with your existing development workflow. For example, you could add a step to your code review process to ensure that changes are properly recorded in the trainlog.

By following these tips, you can reduce the effort required to maintain a trainlog while still reaping the benefits of an organized and comprehensive record of your machine learning development process.

---

#### My example

This is an example of training an object detection model on remote sensing imagery.

```
# Trainlog  
  
Inspiration and format from a [keep c changelog](https://keepachangelog.com/en/1.0.0/)  
  
Experiment runs are tracked in [this mlflow experiment](https://<MLFLOW_HOST>/#/experiments/1).  
  
## 2022-08-31, Faster-R-CNN  
  
### Added  
- Export **my_dataset** dataset into _COCO_ format.  
- Train **Faster R-CNN** model with _Detectron2_.  
  
### Results  
- Faster-R-CNN model achieves **AP50 = 0.51** on the val set   
and **AP50 = 0.41** on the test set. [512x512 model](https://<MLFLOW_HOST>/#/experiments/49/runs/4231e18f89814d538cb170d878edaf4b)  
- Best results are achieved by fine-tuning from detectron2 weights,  
although fine-tuning from ImageNet weights yields similar results.  
- Training with Adam optimizer yields better results much faster than SGD.  
- Learning rate between 3e-4 and 1e-4 yields best results.  
  
### Lessons learnt  
- Faster-R-CNN still falls behind YOLOv5.  
- Training from scratch yields worse results than fine-tuning.  
  
### Ideas  
- Try to train with more data augmentation techniques.  
- Try out varying image sizes  
- Use other backbones (lvis, cascade-rcnn, keypoint-rcnn, large-scale jitter).  
- Class-imbalance loss functions (Focal Loss, GHM Loss, etc.).  
- Generate custom anchor boxes  
  
## 2022-08-15, input data pre-processing.  
  
### Added  
- Introduce new speckle filters and pixel stretching methods.  
  
### Improvements  
- Pre-processing `amplitude > refined lee > 10log10` yields best results.  
- Runner-up is `amplitude > rescale > refined lee`.  
- For the **improved lee sigma filter**, best configuration is `amplitude > rescale > improved lee sigma`  
  
### Lessons learnt  
- Improved lee sigma cannot beat refined lee filter, results are on par with the original lee filter.  
- Omitting any pixel stretching (only speckle filter) results in no learning at all.  
  
### Ideas  
- try other model approaches  
  
## 2022-07-25, two-class yolov5  
  
### Changed  
- Generate a dataset with two classes  
- Train yolov5 small, medium and large  
  
### Results  
- yolov5m single-class training reaches **mAP@0.5 = 0.517** (F1=0.54)  
- yolov5s reaches results as good as yolov5m  
- training yolov5m with 2 classes does not outperform  
single-class training in terms of mAP@0.5, but does give a boost to class_one  
with individual **AP@0.5 = 0.539** (F1=0.51)  
  
### Lessons learnt  
- yolov5 large does not outperform yolov5 medium,  
reaching only **mAP@0.5 = 0.285** during similar training tim  
  
### Ideas  
- try out various pre-processing techniques
```

#### Outro

Let me know what you think of my changelog adaptation to a machine learning model development cycle in the comments below.
