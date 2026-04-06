---
title: "YOLOv8, EfficientDet, Faster R-CNN or YOLOv5 for remote sensing"
date: 2023-05-02
slug: "object-detection-remote-sensing"
canonicalURL: "https://medium.com/@rustemgal/yolov8-efficientdet-faster-r-cnn-or-yolov5-for-remote-sensing-12487c40ef68"
author: "Rustem G"
---

Remote sensing with Synthetic Aperture Radar (SAR) data has become an essential tool for monitoring and understanding changes in the…

---

Remote sensing with Synthetic Aperture Radar (SAR) data has become an essential tool for monitoring and understanding changes in the Earth’s surface. Object detection with SAR data involves detecting and localizing objects of interest such as buildings, vehicles, and ships. In recent years, deep learning-based approaches have shown remarkable success in object detection with SAR data. In this article, we compare the performance of four popular architectures — YOLOv8, EfficientDet, Faster R-CNN, and YOLOv5 — for object detection with SAR data.

#### **Evaluation setup**

The evaluation of the object detection architectures was performed on an internal dataset that includes several classes. The dataset was used for both training and evaluation, and the [mean average precision](https://blog.roboflow.com/mean-average-precision/) with IoU threshold of 0.5 (mAP@50) metric was used to compare the performance of the different algorithms. The dataset included a range of objects that are commonly found in remote sensing applications, such as vehicles and constructed objects.

The original data was a collection of large tif images which were tiled into 1024 tiles and SAR despeckling filters were applied in order to make objects more vivid. This yielded over 7k image samples and over 12k bounding boxes.

#### **Results**

```
|   Architecture     | mAP@50 | GPU Latency|  
| -------------------| ------ | -----------|  
| YOLOv8             | 0.62   | 1.3ms      |  
| EfficientDet       | 0.47   | -          |  
| Faster R-CNN       | 0.41   | 54ms       |  
| YOLOv5             | 0.58   | 2.8ms      |
```

Based on the results presented, it is clear that YOLOv8 is the most accurate and fastest of the four architectures evaluated, achieving a mAP50 of 0.62 on the test set. YOLOv5 achieved a score of 0.58 on the test set, making it the runner-up to YOLOv8 both in terms of accuracy and processing speed. EfficientDet came in third, achieving a mAP@50 of 0.47 on the test set. Finally, Faster R-CNN performed the worst of the four reaching a mAP@0.5 of 0.41, while also being much slower than others.

Now, we are going to dig deeper into what lessons we have learnt while experimenting with each of these architectures.

---

### YOLOv8

[YOLOv8](https://docs.ultralytics.com/) is an extension of the popular YOLO (You Only Look Once) object detection architecture. It is known for its high speed and accuracy, making it a popular choice for real-time applications. The authors claim to outperform previous yolo releases (yolov7, yolov6 and yolov5) on the COCO dataset (image below).

![credit: yolov8 github repo](https://cdn-images-1.medium.com/max/1200/1*6Sn93qyovio0qn3Y3q7Vgw.png)

credit: yolov8 github repo

In our case YOLOv8 achieves an mAP50 of 0.62 on the test set, making it the most accurate and fastest among the compared architectures. These are findings:

* YOLOv8n (nano) is faster, smaller and more accurate than yolov8 small or yolov8 medium on small datasets.
* Fine-tuning from COCO weights yields better results than random weights.
* Downsizing 1024 tiles to 512 input size yields slightly better accuracy and faster prediction speed.
* While Adam optimizer is good for quick experimentation, SGD optimizer outperforms Adam in the longer training.
* Larger batch size does not necessarily lead to better results.

![Comparison chart for various yolov8 setups](https://cdn-images-1.medium.com/max/1200/1*V94aE2HOQO6-YyX3jWAgOw.png)

Comparison chart for various yolov8 setups

---

#### EfficientDet

[EfficientDet](https://github.com/google/automl/tree/master/efficientdet) ([pytorch implementation](https://github.com/rwightman/efficientdet-pytorch)) is a family of object detection models that use EfficientNet as the backbone network. It is known for its high accuracy and efficiency, making it a popular choice for resource-constrained applications.

![credit: official efficientdet github repo](https://cdn-images-1.medium.com/max/1200/1*Ow270e5lGOp824y5b-U_uA.png)

credit: official efficientdet github repo

EfficientDet achieves a mAP@50 of 0.47 on our setup. The efficientdet\_d1 backbone and tf\_efficientdet\_d1\_ap backbone are the most accurate for remote sensing with SAR data on our small dataset.

---

#### Faster R-CNN

Faster R-CNN is a popular two-stage object detection architecture that uses a Region Proposal Network (RPN) to generate object proposals. It is known for its high accuracy and flexibility, making it a popular choice for a wide range of applications. We have used a [detectron2](https://detectron2.readthedocs.io/en/latest/index.html) repo for training and evaluation.

The Faster-R-CNN model achieves a mAP@50 of 0.41 on the test set. Summary of findings:

* Best results were achieved by fine-tuning from detectron2 weights, although fine-tuning from ImageNet weights yielded similar results. Training from scratch requires significantly more time and is not guaranteed to match the results of fine-tuning.
* Training with the Adam optimizer with a learning rate between 3e-4 and 1e-4 yielded better results much faster than SGD.
* Resizing images to 512x512 from 1024x1024 tiles yielded identical results but was faster in training and inference.

![Comparison chart for various faster r-cnn setups](https://cdn-images-1.medium.com/max/1200/1*xSbPdRFrQzAPTYQxZ9GQDg.png)

Comparison chart for various faster r-cnn setups

---

#### YOLOv5

[YOLOv5](https://github.com/ultralytics/yolov5) is a predecessor of YOLOv8. It is known for its simplicity and speed, making it a popular choice for real-time applications.

Results:

* yolov5s (small) outperforms other yolov5 nano, medium and large on a small dataset.
* larger model input sizes lead to better results.
* Adam optimizer with a default learning rate is a good choice for experimentation.

---

### Summary

Overall, our comparison of object detection architectures for remote sensing with SAR data shows that YOLOv8 is the best choice in terms of accuracy and speed. Additionally, YOLOv8 is the quickest in going from 0 to 1 and it’s highly configurable, allowing for customization of hyper-parameters to further optimize its performance.

Faster R-CNN and EfficientDet models didn’t show competitive accuracy, as well as being significantly slower in inference time. YOLOv5 also showed competitive accuracy but required larger model and input sizes to achieve it. In conclusion, for remote sensing with SAR data, YOLOv8 is the recommended architecture for accurate and fast object detection with easy customization.

*Subscribe and share this article if you like the content.*
