---
title: "2023 highlights of computer vision progress"
date: 2023-12-26
slug: "cv-highlights-2023"
canonicalURL: "https://medium.com/@rustemgal/2023-my-journey-through-the-world-of-computer-vision-technologies-48c6949bb3a3"
author: "Rustem G"
---

This year has been a journey full of learning and experimentation in the world of computer vision and deep learning. In this article, I’m…

---

#### 2023 highlights of computer vision progress

This year has been a journey full of learning and experimentation in the world of computer vision and deep learning. In this article, I’m excited to share a summary of my experiences, focusing on the practical aspects of my work, primarily in the geo-spatial domain. I’ve spent the year delving into various architectures and tools, understanding their nuances and how they fit into traditional computer vision tasks. My goal is to give you a straightforward, honest look at what worked, what didn’t, and the lessons I learned along the way.

---

#### Models and architectures

In the realm of computer vision and deep learning, a variety of tasks and corresponding models have been central to my work this year. Let’s break them down.

#### Image classification

In the sphere of image classification this year, my experience heavily leaned towards the [EfficientNet family](https://pytorch.org/vision/master/models/efficientnetv2.html) of models. A standout feature of EfficientNet models is their exceptional balance between accuracy and speed. This becomes particularly evident when working with smaller datasets, where EfficientNet models often outperform newer, larger models Vision Transformers. This efficiency is not just a theoretical advantage but a practical aspect, especially when resources or data availability are constrained.

![EfficientNetV2's training and parameter efficiency (source: efficientnetv2 paper)](https://cdn-images-1.medium.com/max/1200/1*sfQGEN734e5k_Pn_5suNWQ.png)

EfficientNetV2's training and parameter efficiency (source: [efficientnetv2 paper](https://github.com/ultralytics/ultralytics))

Another noteworthy mention in the realm of computer vision architectures is [ConvNeXt](https://pytorch.org/vision/master/models/convnext.html), which has also seen significant advancements this year, particularly with its [latest v2 release.](https://arxiv.org/abs/2301.00808) ConvNeXt, building on the strengths of traditional convolutional networks, has been a powerhouse in handling new and diverse datasets. Its architecture, fine-tuned for modern deep learning tasks, provides an exemplary balance between performance and computational efficiency. The v2 iteration of ConvNeXt brings further enhancements, optimizing it for even greater effectiveness across a range of computer vision tasks.

Additionally, the realm of data augmentation has been revolutionized with techniques like [RandAugment](https://pytorch.org/vision/master/generated/torchvision.transforms.v2.RandAugment.html#torchvision.transforms.v2.RandAugment) and AutoAugment. These methods have proven to be more than just enhancements; they are game-changers in improving model robustness and generalization. By automatically adjusting the augmentation strategies, these techniques ensure that models are not just trained on a wider variety of data but are also better equipped to handle real-world variability.

#### Object detection

In the field of object detection, this year has been marked by significant developments, most notably with the release of [YOLOv8](https://docs.ultralytics.com/#yolo-a-brief-history) from Ultralytics. YOLOv8 has emerged as a standout model, primarily due to its ease of use in getting started, training, and deploying. Its out-of-the-box performance is commendable, often surpassing other YOLO architectures and many heavier models in terms of efficiency and accuracy. My experience with YOLOv8 has been overwhelmingly positive; it consistently delivered high-quality results with little customization, making it a go-to choice for quick yet effective object detection.

![YOLOv8 coco results (source: ultralytics github)](https://cdn-images-1.medium.com/max/1200/1*6Sn93qyovio0qn3Y3q7Vgw.png)

YOLOv8 coco results (source: [ultralytics github](https://github.com/ultralytics/ultralytics))

On the other hand, [YOLO-NAS](https://github.com/Deci-AI/super-gradients/tree/master), a newer entry in the object detection space, presented a different experience. While it promises advancements and optimizations in network architecture search, my initial trials on custom datasets were less successful. However, I plan to fix this in the upcoming year.

#### Semantic segmentation

The area of semantic segmentation has seen significant advancements this year, most notably with the release of the [Segment-anything model](https://segment-anything.com/) (SAM). SAM has demonstrated great versatility and performance across a wide range of domains, including challenging ones in the geo-spatial imagery. Its ability to handle diverse segmentation tasks with high accuracy makes it a noteworthy addition to the semantic segmentation toolkit. However, SAM is not without its challenges. It is a relatively heavy model, and fine-tuning it can be a complex and resource-intensive process. Despite these hurdles, SAM often performs admirably even without fine-tuning the backbone, making it a powerful tool for broad applications.

[Fine-tune Segment-Anything modelIn this blog post, we will explore the process of fine-tuning SAM (Segment-Anything-Model), an image semantic…medium.com](https://medium.com/@rustemgal/fine-tune-segment-anything-model-9877993d9db9)

In contrast, when working with custom datasets, I’ve found that backbones based on EfficientNet or [MiT](https://huggingface.co/nvidia/mit-b0) (SegFormer) are often a better choice. These models strike a balance between speed and performance, making them particularly suitable for full model fine-tuning on specific datasets. Their efficiency in training and the quality of performance they deliver have made them a preferred choice in my semantic segmentation tasks. These models are not only fast to train but also maintain a high level of accuracy and effectiveness, making them ideal for projects where resource optimization and model precision are key considerations.

![Dalle-3 generated this image for semantic segmentation, saying it’s a complex scene — a suitable task for semantic segmentation.](https://cdn-images-1.medium.com/max/1200/1*e0_2aZzLYA4TsgZHnq-Q5g.png)

Dalle-3 generated this image for semantic segmentation, saying it’s a complex scene — a suitable task for semantic segmentation.

#### Self-supervised learning

A key trend I’ve observed this year is the growing importance of Self-Supervised Learning (SSL) in many computer vision tasks. The approach of pre-training models using SSL techniques and then fine-tuning them on downstream tasks is gaining a momentum. This method leverages the power of learning from unlabeled data, which is abundantly available, and then applying this learned knowledge to more specific tasks. The trend towards SSL pre-training not only enhances model performance but also opens up new possibilities in object detection, especially in scenarios where labeled data is scarce or expensive to obtain.

The release of [DINOv2](https://github.com/facebookresearch/dinov2) marks another milestone in the field. Building on the success of its predecessor, DINOv2 offers enhanced features for self-supervised learning. I’ve found that starting with DINO features often gives a strong foundation for various tasks. The ability of DINOv2 to learn rich representations without labeled data is particularly valuable, providing a versatile starting point for numerous computer vision applications.

![DINOv2 downstream task results (source: dinov2 project site).](https://cdn-images-1.medium.com/max/1200/0*nHBndPz4SfKh3sfJ)

DINOv2 downstream task results (source: [dinov2 project site](https://dinov2.metademolab.com/)).

#### Other key areas in computer vision

**Zero-shot object detection:** [**Grounding DINO**](https://github.com/IDEA-Research/GroundingDINO)**.** This year, Grounding DINO for zero-shot object detection has emerged as a significant development. It presents a unique approach where the model can detect objects that it has never seen during training, showcasing the expanding capabilities of zero-shot learning. This advancement has profound implications, especially in scenarios where labeled data for every possible object is not feasible.

[Zero-training object detectionWith zero-training approaches, object detection becomes faster, more flexible, and adaptable to real-world scenarios…medium.com](https://medium.com/@rustemgal/zero-training-object-detection-81820c30073f)

**Feature Extraction: CLIP, DINO, ImageNet-pretrained models.** In the domain of feature extraction for computer vision, models such as CLIP, DINO, and those pretrained on ImageNet each stand out for their unique capabilities. CLIP excels in tasks requiring a nuanced blend of visual and textual understanding, while DINO showcases its strength in a broad domain of images, extracting rich features from unlabeled datasets. ImageNet-pretrained models offer a versatile and reliable foundation due to their extensive training across diverse imagery. The optimal choice among these models often hinges on the specific needs of the task, as their performance varies depending on the application.

**Multi-object tracking: SORT improvements.** In the realm of multi-object tracking, OCSORT, ByteTrack, and BOT-SORT have stood out this year. Each of these models offers robust tracking capabilities, making them excellent choices for tasks that involve tracking multiple objects over time. Their performance in dynamic and complex scenes has been impressive, making them go-to options for multi-object tracking needs.

---

### Computer vision tools

**FiftyOne for data curation.** FiftyOne has been an indispensable tool in my computer vision toolkit, especially for data curation. Its rich and intuitive Python SDK, coupled with a powerful browser app, makes visualizing data and labels for any computer vision task (like classification, detection, instance/semantic segmentation, keypoints, etc.) a breeze. The ease with which it allows users to download and explore public datasets and models is remarkable. Moreover, its integration with various labeling tools (such as CVAT and Label Studio) and the ability to import/export datasets in a variety of formats streamline the entire data preparation process significantly.

[**DVC Pipelines**](https://dvc.org/doc/user-guide/pipelines) **for Reproducible Data Pipelines.** Data Version Control (DVC) pipelines have been instrumental in establishing reproducible data workflows. The key strengths of DVC lie in its ability to cache intermediate results and track dependencies and outputs, which greatly aids in maintaining consistency across different stages of a project. The flexibility DVC offers in building DAGs for data processing pipelines allows for efficient and transparent management of complex data transformations, making it a cornerstone in my data handling practices.

[Reproducible data prepYour future self and your team members will thank you for this. Keep on reading to see a real-world example of a…medium.com](https://medium.com/@rustemgal/reproducible-data-prep-a49207ded8bc)

[**Lightning**](https://lightning.ai/) **for Model Training.** PyTorch Lightning has transformed my model training workflow. Its clean and clear API, along with numerous built-in features, has simplified model improvement and routine operations. The integration for metric calculation and tracking is seamless, enhancing the training process’s efficiency and effectiveness. Lightning’s abstraction layer atop PyTorch makes complex training routines more manageable and accessible. On the other hand, HuggingFace’s transformers has so far implemented most of the CV tasks already and seems appealing to try out — a good starting challenge for 2024.

[**Accelerate**](https://huggingface.co/docs/accelerate/index) **for Distributed Training.** When it comes to distributed training, Accelerate has been a game-changer. It supports multi-GPU and multi-node setups and is PyTorch-native, requiring only a few code changes to get started. The power and simplicity it brings to distributed training have significantly reduced the complexity typically associated with scaling up training processes.

[**RayTune**](https://docs.ray.io/en/latest/tune/index.html) **for Hyperparameter Search.** RayTune stands out in the realm of hyperparameter tuning. Its support for multi-GPU setups and device fractions, along with built-in algorithms like ASHA, makes it an efficient tool for optimizing model parameters. The integrations with tracking tools like TensorBoard and MLflow, combined with the minimal code required to get started, make RayTune a robust and user-friendly choice for fine-tuning models to achieve optimal performance.

[Practical hyper-parameter tuning for any deep neural netWhether you’re fine-tuning YOLO, EfficientNet or Unet, hyper-parameter tuning with ASHA can help reduce search time and…medium.com](https://medium.com/@rustemgal/practical-hyper-parameter-tuning-for-any-deep-neural-net-303cc537fd01)

[**MLflow**](https://mlflow.org/docs/0.7.0/tracking.html) **and** [**ClearML**](https://clear.ml/) **for Experiment Tracking.** MLflow has established itself as a robust tool for experiment tracking, akin to a mastodon in the field. Its ease of getting started, straightforward API, and versatile visualization tools make it highly accessible. Additionally, the model registry and artifact tracking features of MLflow enhance the management and deployment of models. On the other hand, my foray into ClearML has been enlightening. ClearML offers an extensive set of features, including a dataset registry, nested structure of projects, and remote execution with agents. Its comprehensive approach to experiment tracking and management has added a new dimension to my workflow, allowing for more organized and scalable project handling. I’m yet to try other amazing tracking tools which have proliferated over the past few years.

**Triton inference server.** Triton Inference Server stands as a robust solution for serving models in production, renowned for its extensive support of multiple frameworks and efficient model management. It offers seamless integration with popular deep learning frameworks like TensorFlow, PyTorch, and ONNX, enabling a diverse range of models to be deployed with ease. A key feature of Triton is its dynamic model management, which simplifies the process of updating and maintaining various models in a production environment. This server is designed to handle simultaneous requests efficiently, ensuring high throughput and low latency, which are critical for real-time applications. Additionally, Triton’s support for GPU and CPU-based inference and its scalability across multiple nodes make it an adaptable and powerful tool for businesses of all sizes.

[Automate model training with CI/CDWould you believe if I told you that our team trains deep neural nets on a remote GPU machine with a single git commit…medium.com](https://medium.com/@rustemgal/streamline-deep-learning-model-training-with-ci-cd-71680976b2c2)

---

#### Conclusion

As we reflect on the past year, it’s evident that the field of computer vision and deep learning has continued to evolve at a rapid pace. Particularly noteworthy has been the surge in developments within generative AI, which, in the past two years, have somewhat overshadowed traditional deep learning tasks in computer vision. These advancements have captured much of the spotlight, showcasing the ever-expanding capabilities of AI.

However, it’s crucial to recognize that the foundational tasks in computer vision — such as image classification, object detection, semantic segmentation, and others — continue to be essential. These tasks are not fading into obsolescence; rather, they remain integral to solving specific, practical problems in various domains.

Moreover, the number and variety of models and tools available for computer vision tasks have grown exponentially, providing practitioners with an ever-increasing array of options. This abundance offers the flexibility to tailor solutions to specific needs and preferences, enabling anyone, from beginners to seasoned experts, to build their own comprehensive computer vision workflows.

As we move forward, it’s clear that the journey of discovery and application in computer vision and deep learning is far from over. The foundational tasks will continue to be relevant, and the tools and models will keep evolving, offering new possibilities and challenges. It’s an exciting time to be part of this field, and I look forward to what the future holds.

Do check out other great 2023 reviews:

[Computer Vision and FiftyOne Community Year in Review 2023Welcome to the final community update for 2023! In this blog we’ll bring you up to speed on recent happenings in the…medium.com](https://medium.com/voxel51/computer-vision-and-fiftyone-community-year-in-review-2023-b0df944350f2)

[Why 2023 was the most exciting year in computer vision history (so far)The 10 developments that reshaped computer visionmedium.com](https://medium.com/voxel51/why-2023-was-the-most-exciting-year-in-computer-vision-history-so-far-8a812aa7a11f)
