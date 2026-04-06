---
title: "Detect and classify with zero labels and code"
date: 2024-02-09
slug: "zero-label-detection"
canonicalURL: "https://medium.com/@rustemgal/detect-and-classify-with-zero-labels-and-code-618b84a9d927"
author: "Rustem G"
---

In part two of our series, we build on our progress from selecting key video frames. Now, we focus on the critical tasks of labeling these…

---

In part two of our series, we build on our progress from selecting key video frames. Now, we focus on the critical tasks of labeling these frames and developing effective models. Our aim is to transform these raw frames into a well-annotated dataset, setting the stage for rigorous training in object detection and image classification. Let’s delve into these essential steps.

[Efficient Frame Extraction for Video Object AnnotationData labeling is crucial but time-consuming. Imagine if we could label less and achieve more accuracy. Smart frame…pub.aimind.so](https://pub.aimind.so/efficient-frame-extraction-for-video-object-annotation-366daba84556)

Creating video processing systems boils down to two essentials: spotting and knowing what’s in the frame. First, we have object detection — it’s like the system’s eyes, spotting and tracking everything from people to cars in the video. This step is crucial for making sense of what we see. Next up is object classification. It’s the brainy part, not just seeing but understanding what each object is. This combo — detection and classification — is the core of video analysis, helping us unravel the story hidden in the pixels.

---

We’re using [FiftyOne](http://docs.voxel51.com/), just like before, to make working with datasets, models and annotations a snap. It links our data and annotations smoothly. A few lines of Python code let us load images and model predictions into the FiftyOne app and visualize everything in the browser. With the help of [fiftyone plugins](https://github.com/voxel51/fiftyone-plugins), we are able to perform all actions in the browser interface or using the command-line interface.

```
# install fiftyone if not available in the system  
pip install -U fiftyone
```

---

### Object detection

First up, we build an object detection model to find our target items. Training this model usually involves marking objects with bounding boxes, a time-consuming task if done by hand. But here’s a shortcut: use an existing model to create rough labels, then tweak them manually to speed things up.

Depending on what you’re detecting, choose your pre-trained model wisely. For everyday objects, a [COCO](https://cocodataset.org/) pre-trained model is great — it’s like a huge database of common items, ready to spot things quickly and accurately. Got something more unique? Turn to a zero-shot object detection model. It needs a bit of help though — you’ll have to feed it positive and negative labels to teach it right. Below, I’ve outlined some top object detection methods to get you started:

[Zero-training object detectionWith zero-training approaches, object detection becomes faster, more flexible, and adaptable to real-world scenarios…medium.com](https://medium.com/@rustemgal/zero-training-object-detection-81820c30073f)

We are able to get started with predictions from a COCO-pretrained model with just a few clicks in the fiftyone app:

1. **Open a dataset**.
2. **Select a zoo model**: all available models can be filtered based with tags depending on a task.
3. **Apply it to the dataset** (this might take some time for a model to run on all image samples).
4. **Review predictions**: model predictions will be available under a freshly created label field.

![Applying an object detection model with the @voxel51/zoo plugin](https://cdn-images-1.medium.com/max/1200/1*NVhcCDRRNQYd1d5Q3mS5LA.gif)

Applying an object detection model with the @voxel51/zoo plugin

After getting our initial object detection guesses, we need to refine them for a dataset with spot-on labels. CVAT (Computer Vision Annotation Tool) is perfect for this. It’s tailor-made for computer vision tasks, allowing us to tweak bounding boxes, get rid of wrong detections, and add new labels easily. It’s also super useful for object tracking later on.

There are simple steps to create a new labelled dataset:

1. Select labels of interest and create a view.
2. Send the samples with pre-polulated predictions for annotations.
3. Fix annotation mistakes.
4. Load new annotations.

![Requesting annotations with the @voxel51/annotation plugin](https://cdn-images-1.medium.com/max/1200/1*PPXtJwaT6vqSnlAlDTCTmw.gif)

Requesting annotations with the @voxel51/annotation plugin

Now, with our precise labels, we’re set to prep the data for model training. Thanks to FiftyOne, exporting the dataset in formats like YOLO, COCO, or Pascal VOC is as easy as running these scripts in the terminal:

```
# Export samples with a sample tag "animals"  
# into a ./data/export/quickstart_coco directory
```

After exporting our dataset into a standard detection format, we’re ready to leverage an object detection framework to train and deploy models. Each of these frameworks brings unique strengths to the table:

* **Ultralytics-YOLOv8** is at the forefront with its YOLO (You Only Look Once) architecture, ideal for real-time object detection. It delivers fast and precise predictions, making it a top choice for applications requiring quick processing without sacrificing accuracy.
* **HuggingFace Transformers** offers a comprehensive library with a vast range of pre-trained models. Its easy integration and versatile model hub make it incredibly efficient for training and deploying models across various tasks.
* **Super-Gradients YOLO-NAS** introduces a novel approach with its Neural Architecture Search (NAS) for YOLO, optimizing model architecture for specific tasks. This adaptability ensures superior performance tailored to the unique demands of your data.
* **MMDetection** shines with its modular design, facilitating customization and scalability. It’s particularly valuable for video processing projects, where managing resource demands efficiently is paramount.

```
# Example of training a detection model with  
# Ultralytics YOLOv8 from cli  
  
yolo detect train \  
    data="coco.yaml" \  
    model="yolov8s.pt" \  
    epochs="100" \  
    imgsz="640"  
  
  
# Example of YOLOX training  
# with the super-gradients package  
  
python -m super_gradients.train_from_recipe \  
    --config-name="coco2017_yolox" \  
    "multi_gpu=Off" \  
    "num_gpus=1"
```

Each framework offers specialized features and capabilities, allowing developers to choose the most suitable tool for their specific object detection needs.

---

#### **Object classification**

To tackle the object classification challenge, annotated bounding boxes can be leveraged to construct a dedicated classification dataset. Each detection patch becomes a distinctive sample that can be passed to a classification model individually. We could have used the object detector in order to classify objects to the common categories, however for fine-grained classification use-cases it’s better to train a separate lightweight image classifier.

There are two ways to create an initial image classification dataset. On one hand, we can employ a two-step process involving a pre-trained feature extractor and a clustering algorithm. (Refer to the step 2 in [the part I](https://medium.com/ai-mind-labs/efficient-frame-extraction-for-video-object-annotation-366daba84556) in order to find out more which pre-trained models and clustering algorithms can be used at this stage). On the other hand, we can export detection patches as a classification dataset and fix labels according to our needs. Below is an example of how to the latter approach done entirely within the fiftyone app.

![](https://cdn-images-1.medium.com/max/1200/1*ndmNgWxxwO4lPETZpL5CxQ.gif)

The exported dataset will have the following directory structure:

```
animals_img_clf  
├── bear  
│   ├── 000001.jpg  
│   ├── 000002.jpg  
│   ├── 000003.jpg  
│   ...  
├── bird  
│   ├── 000001.jpg  
│   ├── 000002.jpg  
│   ├── 000003.jpg  
│   ...  
├── cat  
│   ├── 000001.jpg  
│   ├── 000002.jpg  
│   ├── 000003.jpg  
│   ...  
├── cow  
│   ├── 000001.jpg  
│   ├── 000002.jpg  
│   ├── 000003.jpg  
│   ...  
├── dog  
│   ├── 000001.jpg  
│   ├── 000002.jpg  
│   ├── 000003.jpg  
│   ...  
├── elephant  
│   ├── 000001.jpg  
│   ├── 000002.jpg  
│   ├── 000003.jpg  
│   ...
```

It’s crucial to manually check and fix resulting classification labels, especially for small datasets. These datasets need to be error-free to build a strong model. Carefully sorted classes make the dataset more refined, setting a solid base for training. One can leverage the process in the fiftyone app to fix classification labels in CVAT.

Next, we train a compact image classification model like **MobileNet** or **EfficientNet**. These smaller models are great because they’re efficient and accurate, even with small datasets. Leverage tools such as flash.zero in order to train an image classification without writing a single line of code.

```
# Install flash for vision  
# and train a simple image classifier  
  
pip install "flash[image]"  
flash image_classification \  
    --trainer.max_epochs="10" \   
    --model.backbone="efficientnet_b0" \  
    from_folders \  
    --train_folder="path/to/exported/dataset
```

---

**Conclusion**

We have been able to train two lightweight models with minimal amount of data and code. By leveraging an iterative process in enhacing each dataset, we can achieve significant improvements in both object detection and classification. Digging deeper, in order to efficiently analyze video streams we have to connect detections and classifications across frames.

In the upcoming post of this series, we’ll delve into the exciting realm of video object tracking. We will review few state-of-the-art real-time algorithms for multiple object tracking and evaluate them on our data using several evaluation benchmarks. Adding a tracking algorithm will allows to perform various analytics such as object counting, video tagging, generating summaries, etc.

*Subscribe to get notified when new posts are published.*
