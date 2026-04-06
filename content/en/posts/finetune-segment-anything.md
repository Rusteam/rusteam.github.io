---
title: "Fine-tune Segment-Anything model"
date: 2023-06-09
slug: "finetune-segment-anything"
canonicalURL: "https://medium.com/@rustemgal/fine-tune-segment-anything-model-9877993d9db9"
author: "Rustem G"
---

In this blog post, we will explore the process of fine-tuning SAM (Segment-Anything-Model), an image semantic segmentation model. We will…

---

In this blog post, we will explore the process of fine-tuning SAM (Segment-Anything-Model), an image semantic segmentation model. We will delve into the reasons behind fine-tuning, what are available strategies and I’ll share tips and caveats from my own experiments.

---

[SAM](https://segment-anything.com/) is a powerful image semantic segmentation model designed to accurately predict pixel-level masks for a wide range objects within an image. It consists of three parts:

1. **Image encoder** —a heavy vision transformer backbone that generates image features.
2. **Prompt encoder**— a lightweight embedding module that creates sparse and dense embeddings out of prompt inputs (points, boxes and or masks).
3. **Mask decoder**— a decoder that takes outputs of the image encoder and the prompt encoder to produce masks.

![Source: Segment-anything paper. Image is passed through the image encoder, then its latent features are combined with prompt features before feeding into the mask decoder. Finally, up to 3 output masks are generated.](https://cdn-images-1.medium.com/max/1200/1*RUicIUMkw665uDJEvrjA_g.png)

Source: Segment-anything paper. Image is passed through the image encoder, then its latent features are combined with prompt features before feeding into the mask decoder. Finally, up to 3 output masks are generated.

There are two main modes that SAM runs on. The first mode is *automatic mask generation* (AMG) in which the model generates proposals for mask and then tries to segment all of the areas in an image into unlabelled polygons. The other mode is prompt-guided which usually takes bounding boxes or points as prompt inputs along with an image and outputs a polygon for each prompt.

![Example of running SAM ViT-H on a set of images in the AMG mode. It generates pretty good masks on various objects.](https://cdn-images-1.medium.com/max/1200/1*NNCtw85c7hNN0CGv_jccOQ.png)

Example of running SAM ViT-H on a set of images in the AMG mode. It generates pretty good masks on various objects.

![Example of running SAM ViT-H with box prompts. Given rectangles around objects, SAM is able to produce impeccable object masks.](https://cdn-images-1.medium.com/max/1200/1*Um4Z_m8mbhrcbbWgLJ1PaQ.png)

Example of running SAM ViT-H with box prompts. Given rectangles around objects, SAM is able to produce impeccable object masks.

Finally, SAM comes in three different flavors: *base*, *large* and *huge.* The huge model is a large 32-block-deep vision transformer with about **636 million** parameters. It takes more time to generate predictions but generates masks of much better quality compared to smaller models.

---

While SAM itself is quite robust to any vision data model, it might prove useful to fine-tune it for two primary reasons:

1. To adapt the SAM model to new domains such as medical imagery or remote sensing (check out this [segment-geospatial](https://samgeo.gishub.org/) package).
2. To use SAM’s image encoder as a backbone for a downstream semantic segmentation problem.

**Full SAM fine-tuning.** This approach is mainly beneficial to speed up internal data labelling process with cases where the original SAM does not perform well. However it requires significant training resources as even the base model has close to 100M parameters, and with bigger models, larger amounts of data are necessary even for fine-tuning. Finally, it only makes sense if box/point prompts will be available at inference time which can be fed from a data annotation process or a object/keypoint detection model.

**SAM’s image encoder backbone.** In this approach SAM acts as a feature extractor to generate latent image representations for a subsequent decoder pass like in the [Unet architecture](https://arxiv.org/abs/1505.04597). For semantic segmentation problems this might be a favorable solution as it requires smaller amounts of resources and is independent from prompt supervision.

---

**Tips & caveats**

**GPU machines.** According to the authors, they used a “batch size of 128 distributed across 128 GPUs”. It’s hardly possible to fit more than 1 sample per batch on a single GPU even with a base variant, hence multiple GPU machines are needed to run a training process. Luckily, packages such as [accelerate](https://huggingface.co/docs/accelerate/index) provide a low-barrier entry for distributed training.

**Fixed image size.** [Vision transformers](https://arxiv.org/abs/2010.11929) use a patch embedding layer which produces feature maps of fixed spatial dimensions (H // patch\_size, W // patch\_size). If we want to use a pretrained model for initial weights, we have to stick to the original image size (which is 1024).

**Freeze the encoder.** SAM was trained on a semantic segmentation task and its image encoder is powerful enough to extract robust features for a specific image segmentation task. Freezing the encoder and training only the decoder part can save a lot of compute time and allow training with a larger batch size.

**Gradient accumulation.** When number of available GPUs is less than 128, `accelerate` can help with artificially increasing the batch size through the technique called [gradient accumulation.](https://huggingface.co/docs/accelerate/v0.15.0/en/usage_guides/gradient_accumulation) In a nutshell, it will run a specified number of passes through a dataloader before making an optimization step. Larger batch size should lead to more stable training.

**Train with prompts, evaluate without.** If you decide to go for full SAM fine-tuning without using prompts, you can convert your existing mask/point/box annotations to prompts for a train set. Conversely, do not pass any prompts when evaluating on validation or test sets and check if a metric improves over time. With large and huge variants it should grow, but beware of unused prompt encoder in your inference. It might also be wise to freeze the prompt encoder at all.

---

**Conclusion**

To summarize, it becomes evident that the decision to fine-tune the full SAM model or only utilize the image encoder depends on the availability of resources and the specific task requirements. When considering simple semantic segmentation tasks, it is reasonable to conclude that focusing solely on the image encoder can yield satisfactory results.

If you want to train a Unet with SAM’s image encoder check out [my implementation](https://github.com/qubvel/segmentation_models.pytorch/pull/757) with `segmentation-models-pytorch` package (it is still under review as of this writing, run `pip install git+https://github.com/Rusteam/segmentation_models.pytorch.git@sam` to make it available). In case you want to run SAM on your own imagery I recommend checking out [this article](https://towardsdatascience.com/see-what-you-sam-4eea9ad9a5de) from [Jacob Marks](https://medium.com/@jacob_marks) on how to use SAM with `fiftyone` package (model zoo integration coming soon).

*Let me what you think and subscribe to get notified when my new posts arrive.*
