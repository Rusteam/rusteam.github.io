---
title: "Improve performance of models deployed with Triton"
date: 2023-01-13
slug: "triton-model-performance"
canonicalURL: "https://medium.com/@rustemgal/improve-performance-of-models-deployed-with-triton-c0d3f676c3b0"
author: "Rustem G"
---

If you already use Triton-inference-server in production to serve deep learning models, you might benefit from Triton-model-analyzer in…

---

If you already use **Triton-inference-server** in production to serve deep learning models, you might benefit from **Triton-model-analyzer** in order to find out best configuration parameters for each model that optimize *throughput vs latency*. In this post I want to share how I have done it and my results.

---

Deep learning models have made significant advances in a range of fields, from image and video analysis to natural language processing. However, deploying these models in production environments can be challenging, especially at scale. One key issue is the [throughput](https://www.comparitech.com/net-admin/latency-vs-throughput/) of the models, or the number of predictions they can make in a given time period.

Improving the throughput of deep learning models in production is important for a number of reasons. For one, it can help reduce latency and improve the user experience for applications that rely on real-time predictions. It can also allow for more efficient use of resources, such as GPUs, which can be expensive to operate at scale.

There are a number of ways to improve the throughput of deep learning models in production, including optimizing the model architecture, using more efficient hardware, and parallelizing the prediction process. In this post, we will explore one strategy for improving the throughput of deep learning models in production environments.

---

[Triton-inference-server](https://github.com/triton-inference-server/server) is an open source, high-performance inference serving software developed by NVIDIA. It allows users to deploy trained machine learning models in a production environment and serve them over a network, providing a simple and scalable way to serve predictions to a wide range of clients.

Triton-inference-server supports most of popular model frameworks, including *TensorFlow, PyTorch*, and *ONNX*. It also provides a range of features to optimize the performance of models in production, such as dynamic batching, GPU acceleration, and support for parallel and distributed inferencing.

In addition to serving machine learning models, the tritonserver comes with a tool called [**Triton-model-analyzer.**](https://github.com/triton-inference-server/model_analyzer) This tool provides a range of features to help users understand and optimize the performance of their models.

Some of the features offered by Triton-model-analyzer include model performance analysis, search for optimal parameters and report generation. These tools can be especially useful in production environments, where it is important deliver a specific throughput under certain constraints.

---

### Setup

Triton-model-analyzer is packaged as a Docker image and its tag matches the one from the main tritonserver. This means that the version of the Triton Model Analyzer tool is the same as the version of the tritonserver that it is being used with. This ensures compatibility and allows for easy integration of the tool with the server itself.

Triton-model-analyzer can run in four different modes:

* In the default **local** mode, the model-analyzer will spin up tritonserver in the current environment. It’s required to build a docker image that contains both the model-analyzer and the tritonserver executables in one docker image (a Dockerfile is provided in the repo).
* In the **docker** mode, the model-analyzer will pull and run a tritonserver docker container. Docker socket has to be binded as a volume which will cause troubles if trying to run this in Kubernetes, although runs smoothly on the localhost Docker engine:

```
volumes:  
- /var/run/docker.sock:/var/run/docker.sock
```

* In the **remote** mode, the model-analyzer will try to connect to an existing tritonserver docker container. Note that in this mode it’s currently not possible to sweep through various model configs.
* the **C API** mode is similar to the *local* model except that inference requests are sent directly via C-API rather than GRPC or HTTP.

### Search config

Triton-model-analyzer supports **brute-force** and **quick** search modes. In the *brute-force* mode it will sweep across all model configurations by increasing concurrency. In the *quick* mode it will use a hill climbing algorithm in order to find an optimal configuration under specified constraints: this should yield results faster and almost as good as *brute-force* approach.

Another nifty feature is a **multi-model** search for scenarios when a range of models can be run in parallel. Weights and objectives can be set differently for each model. Unfortunately, this does not support a sweep across instances counts, concurrency or max batch size.

It’s also possible to configure a sequential search across multiple models for a single model-analyzer run. This approach makes sense when we want to optimize each model separately with various configuration options for number of model instances, dynamic batching or concurrency. Sample configuration might look something like this:

```
run_config_search_disable: False  
  
run_config_search_max_concurrency: 16  
  
profile_models:   
  my_classifier:  
    model_config_parameters:  
      max_batch_size: [1, 4, 8, 16]  
      dynamic_batching:  
        max_queue_delay_microseconds: [100, 1000, 2000]  
      instance_group:  
        - kind: KIND_GPU  
          count: [1, 2, 3]  
  my_detector:  
    model_config_parameters:  
      max_batch_size: [1, 4, 8]  
      dynamic_batching:  
        max_queue_delay_microseconds: [100, 1000, 2000]  
      instance_group:  
        - kind: KIND_GPU  
          count: [1, 2]
```

In the example above, Triton-model-analyzer will sweep across 37 configurations for my-classifier and 19 configurations for my-detector with varying values of dynamic batching, max batch size and model instances. A number of concurrent requests will keep increasing exponentially from 1 to 2, 4, 8 and 16 or until throughput stops increasing.

---

### Results

We have trained a detector model ([*yolov5*](https://github.com/ultralytics/yolov5) family) to run on a stream of imagery and a classifier model ([*efficientnet*](https://pytorch.org/hub/nvidia_deeplearningexamples_efficientnet/) family) to determine what kind of object is in each bounding box. Although these models are already quite fast during inference we wanted to give them an extra boost for the quantity of data being processed in production.

Fortunately, the Triton-model-analyzer repo already provides helm-charts to launch an analyzis on a Kubernetes cluster. After a few tweaks I was able to get it running on our development server with a Tesla T4 GPU. It did however require building a docker image that contained both *tritonserver*, *model*-*analyzer* and *perf\_analyzer* executables as only the *local* launch mode was available for kubernetes. My launch command looked like this:

```
containers:  
  name: analyzer  
  image: "{{ .Values.images.analyzer.image }}:{{ .Values.images.analyzer.tag }}"  
  args: [  
    "/bin/bash", "-c",  
    "model-analyzer profile   
    --model-repository /models   
    --output-model-repository-path /output_models/output  
    --override-output-model-repository  
    --checkpoint-directory /checkpoints/  
    --triton-launch-mode local   
    --config-file /config/config.yaml  
    --export-path /results"]  
  volumeMounts:  
      - name: data  
        mountPath: /results  
        subPath: triton_model_analyzer/results  
      - name: data  
        mountPath: /models  
        subPath: models  
      - name: data  
        mountPath: /output_models  
        subPath: triton_model_analyzer/output_models  
      - name: data  
        mountPath: /checkpoints  
        subPath: triton_model_analyzer/checkpoints  
      - name: config  
        mountPath: /config  
  resources:  
      limits:  
          cpu: "1"  
          memory: "4Gi"  
          nvidia.com/gpu: "1"  
volumes:  
- name: data  
  persistentVolumeClaim:  
    claimName: <YOUR_PVC>  
- name: config  
  configMap:  
    name: analyzer-config  
runtimeClassName: nvidia
```

Above is an excerpt from *job.yaml* file provided in the *helm-chart*/*templates* folder. This implies that docker image name and tag values are specified in the *values.yaml* file and your PVC contains a *models* subfolder where search models are stored in the [triton format](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_configuration.md). Results will be available upon completion in the *triton\_model\_analyzer* subfolder.

Results include a summary pdf report for each model and a csv file with all measurements. The pdf report is a very descriptive outline of the best model configurations and a comparison against a default measurement. It’s possible to generate more detailed reports as well when going deeper into performance analysis.

![an example of throughput vs latency chart for a model](https://cdn-images-1.medium.com/max/1200/1*5lehl_PlKiFghGOU_4fX-w.png)

In our case the classifier reached a throughput of **138 inferences per second** which provided **14%** improvement over a default configuration. The detector achieved **49 inferences per second** with a **22%** gain compared to the default setting. Best configuration looked like this:

```
# detector config.pbtxt  
name: "my_detector"  
max_batch_size: 4  
instance_group {  
  count: 2  
  kind: KIND_GPU  
}  
dynamic_batching {  
  preferred_batch_size: 4  
  max_queue_delay_microseconds: 100  
}  
backend: "onnxruntime"  
  
# ========================  
  
# classifier config.pbtxt  
name: "my_classifier"  
max_batch_size: 4  
instance_group {  
  count: 2  
  kind: KIND_GPU  
}  
dynamic_batching {  
  max_queue_delay_microseconds: 2000  
}  
backend: "onnxruntime"
```

**Conclusion**

Overall, Triton Inference Server is a powerful tool for deploying and serving machine learning models in a production environment. By providing a simple and scalable way to serve predictions, it allows organizations to build and deploy intelligent applications that can drive business value.

With the help of Triton-model-analyzer it’s possible to further improve inference performance by finding an optimal model configuration. Luckily the model-analyzer provides a set of features to perform an analyzis end-to-end, including:

* docker or pip installation
* search configuration including multi-model search and optimizing specific metrics under certain constraints
* checkpointing
* kubernetes deployment

In this post we have seen how the Triton-model-analyzer is able to improve performance of our models served with Triton-inference-server. If this was useful to you, do not hesitate to share with like-minded people.

*This post was partially generated by chatGPT.*
