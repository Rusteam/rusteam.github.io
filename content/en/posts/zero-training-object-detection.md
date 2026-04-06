---
title: "Zero-training object detection"
date: 2023-07-10
slug: "zero-training-object-detection"
canonicalURL: "https://medium.com/@rustemgal/zero-training-object-detection-81820c30073f"
author: "Rustem G"
---

With zero-training approaches, object detection becomes faster, more flexible, and adaptable to real-world scenarios. By eliminating the…

---

With zero-training approaches, object detection becomes faster, more flexible, and adaptable to real-world scenarios. By eliminating the need for time-consuming training processes, zero-training approaches enable rapid deployment, resource efficiency, and the detection of a wide range of objects without predefined labels.

---

#### **Task**

Imagine a car-mounted camera capturing a bustling city street. Your task is to develop an algorithm that can automatically detect and identify objects of interest in the video stream, without the need for extensive training or predefined labels. The lack of labelled data and time coupled with a broad range of objects requires you to think beyond traditional approaches and explore innovative methods.

![Examples of car-mounted camera output](https://cdn-images-1.medium.com/max/1200/1*xHBoMaIAkxREez8t-CQ3vQ.png)

Examples of car-mounted camera output

From recognizing common vehicles and pedestrians to identifying unique or rare objects, the goal is to create an intelligent system that can adapt to dynamic environments and deliver accurate detections in real-time. Get ready to dive into the world of zero-training object detection and unravel the possibilities of cutting-edge computer vision technologies.

#### Methods

We explore a range of approaches, each with its unique strengths and considerations. These approaches differ significantly in terms of inputs, outputs and processing time. Our primary goal is to develop a system with highest accuracy using a reasonable amount of compute. Thus we can group all methods into the following groups:

1. General-purpose COCO-based detectors.
2. Models trained on specialized datasets such as Cityscapes or KITTI.
3. Auto mask generation with the Segment-Anything model.
4. Open-set object detection with Grounding DINO.

We consecutively apply each of these methods to our data and visually inspect predictions to figure out which methods perform well on our task. As a result, we discuss advantages and disadvantages of each algorithm and provide visual results.

---

#### COCO-based

![Example of COCO image with annotations. Source: https://cocodataset.org/#explore](https://cdn-images-1.medium.com/max/1200/1*7azB3AJTlwpq36ysfKhg9w.png)

Example of COCO image with annotations. Source: <https://cocodataset.org/#explore>

[COCO](https://cocodataset.org)-based methods, including pre-trained [YOLOv8](https://docs.ultralytics.com/modes/predict/) and [Mask R-CNN](https://arxiv.org/abs/1703.06870) models, are widely used for *closed-set* object detection in various computer vision tasks. YOLOv8 (You Only Look Once) is the latest release of a popular one-stage object detection algorithm that offers real-time performance. It utilizes a single neural network to directly predict bounding box coordinates and class labels for detected objects. Versions V5 and V8 also offer an instance segmentation along with a bounding box prediction.

On the other hand, Mask R-CNN is a two-stage approach that not only performs object detection but also provides instance-level segmentation masks for each detected object. These methods leverage the COCO dataset, which contains a diverse range of object categories, making them effective for detecting **common** objects.

**Pros:**

* Ease of use: COCO-based methods provide a user-friendly approach to object detection, allowing researchers and developers to quickly apply them to various applications.
* Boxes and masks: Both Mask R-CNN and YOLOv8 offer the advantage of instance segmentation masks, enabling more detailed analysis and understanding of object boundaries.
* Production-ready: These methods have been around for a while and proved to be a good choice for a production application.

**Cons:**

* Limited labels: COCO-based methods are trained on datasets with limited labels, which may affect their performance in detecting smaller or infrequent objects.
* Performance on Smaller Objects: While these methods excel at detecting major objects, they may struggle with accurately identifying smaller or less common objects.
* Computational Requirements: Mask R-CNN, with its two-stage architecture, can be computationally intensive, requiring significant resources for inference.

![Results of YOLOv8m predictions: transport and larger objects are detected well, many smaller road infrastructure objects are missed.](https://cdn-images-1.medium.com/max/1200/1*6UUUadRJiM2h7LNao0jlNw.png)

Results of YOLOv8m predictions: transport and larger objects are detected well, many smaller road infrastructure objects are missed.

#### **Specialized datasets**

The [KITTI dataset](https://www.cvlibs.net/datasets/kitti/) focuses on autonomous driving scenarios, capturing real-world images from various viewpoints, weather conditions, and traffic situations. It includes pixel-level annotations for tasks like semantic segmentation, instance segmentation, and 3D object detection. With a particular emphasis on urban environments, KITTI offers a diverse range of object classes commonly encountered on the road, such as cars, pedestrians, cyclists, and traffic signs. Models trained on KITTI can leverage this domain-specific knowledge, making them well-suited for detecting major road objects.

![Example imagery from KITTI](https://cdn-images-1.medium.com/max/1200/1*uH5UVCT85tEYUioQwFOwyA.png)

Example imagery from KITTI

[CityScapes](https://www.cityscapes-dataset.com/examples), on the other hand, focuses on urban street scenes and provides high-quality pixel-level annotations for semantic segmentation. The dataset covers various cities and includes diverse environmental factors such as different weather conditions, lighting variations, and occlusions. With a comprehensive set of object classes including cars, pedestrians, buildings, road markings, and vegetation, CityScapes enables the training of segmentation models tailored for urban environments.

![Example imagery from CityScapes, credit: https://www.cityscapes-dataset.com/examples](https://cdn-images-1.medium.com/max/1200/1*Dx2IAdFNBAbID-dBswGcCg.png)

Example imagery from CityScapes, credit: [https://www.cityscapes-dataset.com/examples](https://www.cityscapes-dataset.com/examples/#coarse-annotations)

**Pros:**

* Trained on similar data: These specialized datasets are designed to capture specific scenarios such as urban environments or driving scenes.
* Diversity: They include images taken under different weather conditions, lighting conditions, and varying perspectives. This diversity provides the models with exposure to a broad range of real-world scenarios, making them more robust and adaptable when deployed.
* Inclusive labels: KITTI includes annotations for not only cars and pedestrians but also less common objects like cyclists, traffic signs, and road markings. Similarly, CityScapes covers an extensive range of classes, including different vehicle types, pedestrians, buildings, and vegetation.

**Cons:**

* Limited labels: Similar to the COCO-based methods, segmentation models trained on specialized datasets may suffer from limited labels, which can hampers our ability to detect a broad range of objects.
* Imprecise Masks: Due to the limited label availability, the generated instance segmentation masks may not be as accurate or precise, leading to challenges in fine-grained object analysis.

![Results of applying a semantic segmentation model trained on CityScapes: All objects including roadside items are masked, however with noticeable mismatches.](https://cdn-images-1.medium.com/max/1200/1*TAVjF9mFY9XrgGWvqgU_pA.png)

Results of applying a semantic segmentation model trained on CityScapes: All objects including roadside items are masked, however with noticeable mismatches.

#### Auto mask generation

Auto mask generation with the [Segment-anything model](https://segment-anything.com/) (SAM) offers unique advantages for zero-training object detection, particularly in terms of high-quality masks and domain adaptation. The segment-anything model is specifically designed to generate accurate instance segmentation masks for detected objects. It leverages advanced techniques to achieve precise boundaries and detailed segmentation results. Check out my other post on fine-tuning SAM if you’re interested to find out more details about it.

[Fine-tune Segment-Anything modelIn this blog post, we will explore the process of fine-tuning SAM (Segment-Anything-Model), an image semantic…medium.com](https://medium.com/@rustemgal/fine-tune-segment-anything-model-9877993d9db9)

An essential component of the auto mask generation is the incorporation of a second-stage classifier, such as [CLIP](https://github.com/openai/CLIP). After SAM generates instance segmentation masks, a separate classification step is required to assign labels to each polygon. In this second stage, the CLIP zero-shot class prediction is utilized to perform the object classification. By leveraging CLIP’s image-text matching capabilities, the method enables zero-shot object detection with open-set labels. This two-stage approach enhances the accuracy and semantic understanding of the detected objects. However, it’s important to note that the inclusion of this second-stage classifier introduces additional complexity and computational requirements to the overall pipeline.

**Pros:**

* High-quality masks: The segment-anything model excels in producing high-quality instance segmentation masks for detected objects. This capability enables finer-grained analysis, allowing for precise delineation and understanding of object boundaries for the second-stage classification.
* Open-set labels: The usage of a zero-shot classifier such as CLIP enables including any class labels. This means that the method is not limited to a predefined set of object classes unlike models trained on COCO or CityScapes.
* Domain adaptation: The model has been trained on diverse datasets and environments, which helps it generalize well to different scenarios and adapt to the specific characteristics of video streams.

**Cons:**

* Heavy model: Its heavy model architecture necessitates substantial computational resources for efficient inference, which may pose constraints in terms of real-time performance or deployment on resource-constrained devices.
* Hand-crafted rules: To select relevant polygons generated by the segment-anything model, extra hand-crafted rules need to be engineered. These rules are necessary to discard irrelevant polygons or segments that do not correspond to actual objects of interest, adding an additional layer of complexity to the method.
* Challenges with object classification: In the second stage of the process, the segment-anything model relies on a CLIP zero-shot class prediction to classify each polygon. This introduces an additional step, increasing the overall complexity of the pipeline and potentially impacting inference time.
* Negative labels: As each generated polygon from the segment-anything model requires classification, it is necessary to introduce negative labels along with target labels. Negative labels serve as counterweights to the target labels, ensuring a balanced classification process. The addition of negative labels creates extra effort in reviewing data and recording various objects and things that appear on a video stream.

![SAM output: It’s able to generate high-precision masks for all kinds of objects, even for smaller ones such as lane markings and parts of road signs.](https://cdn-images-1.medium.com/max/1200/1*vbrfgX3uddhuv29YJbnylQ.png)

SAM output: It’s able to generate high-precision masks for all kinds of objects, even for smaller ones such as lane markings and parts of road signs.

#### Grounding DINO

[Grounding DINO](https://github.com/IDEA-Research/GroundingDINO) is a method that enables open-set object detection, providing several distinct advantages for zero-training approaches. It’s an innovative object detection method that combines human inputs with advanced deep learning techniques. This approach, inspired by language understanding, allows the detection of various objects simply by using category names or referring expressions. By effectively merging language and visual information, it is able to handle previously unseen objects in open-set scenarios.

Grounding DINO combines feature extraction, language-guided query selection, and a cross-modality decoder. It enhances image and text features using self-attention mechanisms and aligns modalities through cross-attention. The language-guided query selection module selects relevant features based on input text, initializing decoder queries. The cross-modality decoder fuses image and text features through self-attention and cross-attention layers. This integration enables accurate and language-driven object detection, improving modality alignment and detection performance.

![Grounding DINO model architecture. Source: Grounding DINO paper.](https://cdn-images-1.medium.com/max/1200/1*S4o0qx9Ixju02n2VQf_hFw.png)

Grounding DINO model architecture. Source: Grounding DINO paper.

**Pros:**

1. Open-set labels: Grounding DINO excels at open-set object detection, enabling the detection of objects that do not belong to any pre-defined classes. This flexibility makes it suitable for scenarios where new or unknown objects may appear, providing adaptability and robustness in real-world environments.
2. Accurate bounding boxes: Grounding DINO demonstrates remarkable performance in generating accurate bounding boxes for detected objects.

**Cons:**

1. Output variability: It is important to note that the output of Grounding DINO may not always perfectly match the given labels. As a result, there can be slight inconsistencies between the predicted objects and the ground truth.
2. Lack of masks: Grounding DINO focuses primarily on bounding box predictions and does not directly provide segmentation masks for detected objects. However, this limitation can be addressed by incorporating additional techniques such as box-guided SAM ( [Grounded-Segment-Anything implementation](https://github.com/IDEA-Research/Grounded-Segment-Anything)).

![Grounding DINO output with a target list of classes: All objects are detected correctly with accurate bounding boxes and class labels.](https://cdn-images-1.medium.com/max/1200/1*u1GRAOhkn_JQOSLq_7R69w.png)

Grounding DINO output with a target list of classes: All objects are detected correctly with accurate bounding boxes and class labels.

---

#### Conclusion

In summary, Grounding DINO stands out as an impressive approach for zero-training object detection due to its versatility in handling a broad range of labels. This method effectively combines Transformer-based detection with grounded pre-training, enabling the detection of arbitrary objects guided by inputs such as category names or referring expressions. With its remarkable performance and open-set concept generalization, Grounding DINO proves to be a valuable solution for various real-world scenarios.

However, depending on the specific area of interest, alternative approaches may be more suitable. For instance, if the focus is primarily on major transport vehicles and pedestrians, a coco-based approach such as YOLOv8 or Mask R-CNN could be an excellent choice. These methods offer simplicity and effectiveness in detecting common objects, making them well-suited for scenarios where precise identification of major objects is crucial.

On the other hand, if the task requires high-precision masks for detailed object segmentation (and processing power and speed are not a concern), a hybrid approach combining one of these detectors with the Segment-anything model could be an ideal option. By incorporating SAM, the system can achieve more accurate and refined masks, improving the overall quality of object segmentation.

*Let me know in the comments what you think about zero-training methods in computer vision and subscribe to get notified about my new posts.*
