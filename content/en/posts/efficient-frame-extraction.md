---
title: "Efficient Frame Extraction for Video Object Annotation"
date: 2023-08-15
slug: "efficient-frame-extraction"
canonicalURL: "https://medium.com/@rustemgal/efficient-frame-extraction-for-video-object-annotation-366daba84556"
author: "Rustem G"
---

Data labeling is crucial but time-consuming. Imagine if we could label less and achieve more accuracy. Smart frame selection is the answer…

---

Data labeling is crucial but time-consuming. Imagine if we could label less and achieve more accuracy. Smart frame selection is the answer. By picking frames that capture the essence and diversity of the data, we can slash manual effort without sacrificing quality. This article unveils a savvy approach that not only speeds up labeling but also maximizes results. Let’s dive into the world of efficient data annotation through strategic frame selection.

By adopting our approach, we achieve impressive efficiency improvements. Out of 50 clips, covering 495 seconds and containing 12k frames, we pull out only 15 frames — yet these frames capture the dataset’s core. Our method streamlines annotation by identifying the most informative instances, maintaining quality, and significantly cutting manual work. The chart below displays how much we reduce manual workload at each step.

![Number of frames left after each step.](https://cdn-images-1.medium.com/max/1200/1*3RpTXr1IabVks5FIqFOwGw.png)

Number of frames left after each step.

In a nutshell, our workflow consists of three steps:

1. Extract a subset of frames from a video collection.
2. Select most informative frames for annotation.
3. Filter and sort frames based on their content and diversity.

### Step 1. Extract keyframes

Keyframes are frames that stand out as representative of the content within a video. Extracting these frames is the first step in the process of selecting frames for object annotation. [FFmpeg](https://ffmpeg.org/), a powerful multimedia framework, is an ideal tool for this purpose. By extracting keyframes, we create a subset of frames that capture significant moments in the video, providing a diverse representation of its content.

A [keyframe](http://nickyguides.digital-digest.com/keyframes.htm), in the context of video compression, is a fundamental and standalone frame that holds complete visual information. Unlike intermediate frames, keyframes do not rely on previous or subsequent frames for reconstruction. They act as reference points for the video codec, allowing efficient compression by storing the entire image content. Keyframes are strategically inserted at regular intervals in a video stream, enabling the codec to use interframe compression techniques for the frames between keyframes. This approach significantly reduces data redundancy and helps maintain video quality while optimizing storage and transmission.

Run this command below in order to extract keyframes for a single video file (after installing `ffmpeg`):

```
ffmpeg -i path/to/my/video/file.mp4 -vf "select=eq(pict_type\,I)" -vsync vfr "keyframes_%03d.jpg"
```

The script utilizes the FFmpeg command with the following flags:

* `-vf` flag to select keyframes only,
* `-vsync vfr` flag to maintain the variable frame rate,
* the extracted keyframes are named `keyframes_%d.jpg` and sequentially numbered.

For example, *ffmpeg* extracts 21 frames from a 79-second-long video clip with with 30 frame/s rate. It’s **less than** **1%** of the original number of frames. Below is the result of extracting 160 keyframes from a collection of 50 short video clips (12082 original frames) from the [kinetics-700–2020 dataset](https://docs.voxel51.com/user_guide/dataset_zoo/datasets.html#kinetics-700-2020).

![Keyframes extracted from 50 short video clips.](https://cdn-images-1.medium.com/max/1200/1*KhWY4LvrldluToDpZGofnw.png)

Keyframes extracted from 50 short video clips.

It’s evident that keyframes within uneventful videos exhibit remarkable similarity, calling for a single selection for labeling. On the other hand, videos with more motion allow us to pick multiple frames. The subsequent step reveals how to perform this selection process optimally.

### Step 2. Select informative frames

Once we have extracted keyframes, the next step is to extract features from these frames that can be used to differentiate and classify them. Deep learning models, particularly convolutional neural networks (CNNs) or visual transformers, excel at capturing intricate features within images. A pre-trained CNN model, from a family of ResNet, VGG, or EfficientNet models, can be used to extract image embeddings from the keyframes.

**Compute embeddings.** This is an example of how to get image embeddings with *EfficientNet-B0* model in PyTorch:

```
import torch  
from torchvision import models  
from torchvision.models import feature_extraction  
  
model = models.get_model('efficientnet_b0')  
model.eval()  
  
feature_extractor = feature_extraction.create_feature_extractor(eff, return_nodes=["avgpool"])  
  
x = torch.randn(1, 3, 224, 224)  
with torch.no_grad():  
    out = feature_extractor(x)  
  
print(out["avgpool"].size())  
# prints torch.Size([1, 1280, 1, 1])
```

The code first imports the required modules, including `torch` and `models` from `torchvision` and loads the *EfficientNet-B0* model using and creates a feature extractor from the EfficientNet model by specifying that only the “avgpool” node’s output should be returned. Passing a random input through this model results in a tensor with dimensions `[1, 1280, 1, 1]`, where 1280 represents the output embedding size.

Several strong backbone architectures have emerged in the field of deep learning, each with its unique advantages that cater to various computer vision tasks.

* [**EfficientNet**](https://pytorch.org/vision/master/models/efficientnet.html?highlight=efficientnet) stands out for its scalability, achieving excellent performance across a wide range of model sizes by optimizing depth, width, and resolution simultaneously. It strikes a balance between efficiency and accuracy, making it suitable for resource-constrained environments.
* [**DINO**](https://github.com/facebookresearch/dino) **and** [**DINOv2**](https://dinov2.metademolab.com/)introduce a self-supervised approach that leverages both instance discrimination and clustering to learn robust visual representations. Its ability to capture fine-grained details and discover similarities across different data domains makes it particularly effective for unsupervised tasks.
* [**ConvNeXt**](https://pytorch.org/vision/master/models/convnext.html?highlight=convnext) combines best features of convolutional neural nets and vision transformers.
* [**CLIP**](https://github.com/openai/CLIP)combines vision and language understanding, allowing it to learn powerful visual representations aligned with natural language descriptions. This makes it versatile for tasks involving cross-modal understanding, like image-text retrieval.

**Cluster embeddings.** Selecting frames for annotation is not only about choosing representative frames but also ensuring diversity. We want to cover a wide range of visual characteristics present in the video collection. To achieve this, we can employ clustering techniques on the extracted image embeddings. Clustering groups similar frames together, allowing us to choose a single frame from each cluster that represents the entire group.

Clustering options:

1. **DBSCAN (Density-Based Spatial Clustering of Applications with Noise):** DBSCAN is effective at identifying clusters of varying shapes and sizes based on density. It doesn’t require the specification of the number of clusters beforehand and can identify noise points as well.
2. **KMeans:** KMeans is a classic centroid-based clustering algorithm that partitions data into a pre-defined number of clusters. It works well when the number of clusters is known and data clusters are relatively well-separated.
3. **Hierarchical Clustering:** Hierarchical clustering builds a tree-like structure of clusters, which can be visualized as a dendrogram. It doesn’t require the number of clusters to be specified and can be agglomerative (bottom-up) or divisive (top-down).

Having split data into clusters, we can select a frame that represents an entire cluster:

1. **Centroid (KMeans):** In KMeans, each cluster has a centroid representing its center. Choosing the data point closest to the centroid can serve as the cluster representative.
2. **Core Point (DBSCAN):** DBSCAN defines core points that have a minimum number of points within a specified distance (epsilon). You can select the core point with the highest density as the representative.
3. **Agglomerative Clustering (Hierarchical):** In agglomerative hierarchical clustering, each cluster is formed by merging two smaller clusters. You can select the most central data point in the merged cluster.
4. **Average Embedding:** Calculate the average of embeddings within each cluster and select the one closest to the cluster’s average. This method works well when embeddings are used for similarity measurement.

By performing this operation we can ensure that our selected samples will be distinct from one another and represent a group of similarly looking samples, thus, reducing efforts on subsequent data annotation.

**FiftyOne**

If you use [**fiftyone**](https://docs.voxel51.com/index.html) package to manage your computer vision datasets, then the entire second step boils down to few simple lines of python code:

```
import fiftyone as fo  
  
dataset = fo.load_dataset(YOUR_DATASET_NAME)  
res = fob.compute_similarity(dataset, brain_key="frame_sim")  
res.find_unique(NUM_SAMPLES_YOU_WANT)  
uniq_view = dataset.select(res.unique_ids)  
fo.launch_app(view=uniq_view)
```

The code above will generate embeddings for each image sample using a lightweight *mobilenet-v2* and then keep selecting distinct samples from a neighborhood of similar images until a desired number of target images is reached.

After a fiftyone window pops up, you can review samples that were selected. Below is the result of selecting top-30 most unique frames. Even though the frames are quite distinct from each other, it’s easy to notice that half of them will not be informative for annotation and model training as they are either blurry or do not contain objects of interest. We can filter out irrelevant frames at the next stage.

![Top-30 most unique frames.](https://cdn-images-1.medium.com/max/1200/1*eH--oP8j_UmWvAG8MEhTQw.png)

Top-30 most unique frames.

### Step 3. Sort frames by diversity

In the pursuit of robust model training, it’s imperative to start with a diverse and representative set of samples, ensuring that the resulting model generalizes effectively. However, within a collection of frames, there inevitably exist irrelevant and redundant ones that must be skipped before sending them to the manual annotation process.

By employing a pre-trained model designed to identify objects or classify images, we can identify frames that offer the most valuable contributions to model training. Simultaneously, the pre-trained model predictions effectively filter out irrelevant frames, streamlining the dataset and focusing model training on high-impact examples.

For this purpose, established models can prove invaluable to identify common object classes:

* Object detectors such as **YOLOv8**, **EfficientDet**, or **Mask R-CNN** which are pre-trained on the COCO dataset. These models possess a deep understanding of common object classes and visual patterns, making them well-suited for detecting and classifying relevant objects within your frames. Running an object detector with *fiftyone*: `fiftyone zoo models apply --model-name mask-rcnn-resnet50-fpn-coco-torch --dataset-name quickstart --label-field mask-rcnn`
* Imagenet-based classifiers like **EfficientNet**, **Vision Transformers**, and **ConvNeXt** can provide precise and detailed annotations for a wide spectrum of objects in case data involves a broader range of object classes. Running an image classifier with *fiftyone*: `fiftyone zoo models apply --model-name resnet18-imagenet-torch --dataset-name quickstart --label-field resnet18`
* Alternatively, zero-shot predictors can also play a pivotal role. Utilizing models such as [**CLIP**](https://github.com/openai/CLIP) for image classification and [**Grounding DINO**](https://github.com/IDEA-Research/GroundingDINO) for object detection enables us to tap into the power of generalized learning. These models can recognize objects outside of common set of labels making them useful to all kinds of data domains.

Check out my other article below to see the comparison between pre-trained object detectors on a video stream.

[Zero-training object detectionWith zero-training approaches, object detection becomes faster, more flexible, and adaptable to real-world scenarios…medium.com](https://medium.com/@rustemgal/zero-training-object-detection-81820c30073f)

This is the final output after we apply *Grounding DINO* with a single class label “Person” in order to select images having people with high confidence.

![Images selected with a “Person” class label and confidence above 0.5.](https://cdn-images-1.medium.com/max/1200/1*mlnIoOvXCQSyofWqSAVU7g.png)

Images selected with a “Person” class label and confidence above 0.5.

As we can see the subset selected contains all relevant and distinct samples to further enhance labels. There are few misses especially in blurry samples but overall result looks impressive for a zero-shot object detector. We can now send these images for semi-automated annotation to quickly improve the labels and train our own person detection algorithm.

### Conclusion

The process of selecting frames for precise object annotation within video collections represents a critical step in building accurate and effective computer vision models. This article has explored a comprehensive workflow that seamlessly integrates various techniques to optimize this selection process. By leveraging FFmpeg for keyframe extraction and deep learning for feature extraction and object detection, this workflow ensures that the curated frames are both diverse and relevant.

In addition to its technical benefits, this automated workflow also holds the potential to significantly reduce costs. By selecting frames with precision, it minimizes the required man-hours for manual annotation, thereby optimizing human resources and saving valuable time and money.

*If you like what you have read and want to see more, subscribe to get updates when I release new posts.*
