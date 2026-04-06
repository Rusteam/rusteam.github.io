---
title: "Reproducible data prep"
date: 2023-03-03
slug: "reproducible-data-prep"
canonicalURL: "https://medium.com/@rustemgal/reproducible-data-prep-a49207ded8bc"
author: "Rustem G"
---

Your future self and your team members will thank you for this. Keep on reading to see a real-world example of a reproducible data pipeline…

---

Your future self and your team members will thank you for this. Keep on reading to see a real-world example of a reproducible data pipeline for preparing satellite imagery for deep neural network training.

---

When working on a machine learning project, data preparation is often the most time-consuming and error-prone task. In the rush to get results, it’s tempting to take shortcuts and manually prepare the data. However, investing time in making your data preparation steps reproducible will pay off in the long run.

There are many compelling reasons to introduce a reproducible data preparation:

* data preparation steps are recorded and model training results can be re-created any time in future
* fast iteration on the data preparation process, as you can simply re-run the process whenever new data becomes available or changes are made to the process
* easy to understand and reproduce when sharing your work with others.

In practice, machine learning projects often involve spending a significant amount of time on [data preparation](https://datacentricai.org/) rather than on model selection or tuning. This is because the quality of data has a direct impact on the accuracy and robustness of machine learning models. While selecting an appropriate model and optimizing its hyper-parameters are important, they are usually secondary to the quality of the data.

### Automate data preparation steps with DVC

As data preparation can be time-consuming and resource-intensive, it is important to leverage automation wherever possible. Additionally, automating data preparation can make it easier to reproduce and iterate on the machine learning process, as it reduces the likelihood of human error and ensures consistency across different runs when conducting experiments.

[DVC (Data Version Control)](https://dvc.org/) is an open-source tool for versioning and tracking data in machine learning projects. It provides a way to manage and track changes to large data files, along with their dependencies and versions, similar to version control systems used for code. It provides a simple and easy-to-use interface for managing and tracking data, which can help to improve productivity and reduce errors.

In addition to its core functionality for data versioning and tracking, DVC also provides several advanced tools for machine learning projects. [DVC Pipelines](https://dvc.org/doc/start/data-management/data-pipelines) is a tool for defining and executing complex machine learning workflows. It allows you to define a sequence of stages, where each stage represents a data pipeline step.

### How to get started

#### 1. Project structure

A proper project structure is crucial for managing and organizing machine learning projects. One popular approach is to use the [data science cookiecutter](https://drivendata.github.io/cookiecutter-data-science/#directory-structure), which provides a standardized layout for organizing data, code, and documentation. The data folder structure consists of several subfolders, each with a specific purpose:

* the **external** data folder contains the original, unprocessed data files
* the **processed** data folder contains the final, processed data files used for training and evaluation
* the **interim** data folder contains intermediate files generated during data preprocessing.
* the **raw** data folder can be used to cache data files when fetched from internal systems.

#### 2. Install and initialize DVC

```
pip install dvc  
dvc init
```

Bear in mind that DVC requires a project to be tracked with *git.*

#### 3. Create dvc.yaml

Assuming you already have scripts that manipulate data, create a *dvc.yaml* file and define your DVC pipeline. For example, a pipeline can include several stages to clean, transform, and aggregate data. Each stage in the pipeline has a specific input and output, and the output of one stage becomes the input of the next stage in the pipeline —this will be crucial to run your stages in a particular sequence. Sample file might look like this:

```
stages:  
  clean:  
    cmd: python src/data/clean.py -i data/external/file.csv -o data/interim/cleaned.csv  
    deps:  
      - data/external/file.csv  
    outs:  
      - data/interim/cleaned.csv  
  transform:  
    cmd: python src/data/transform.py -i data/interim/cleaned.csv -o data/interim/transformed.csv  
    deps:  
      - data/interim/cleaned.csv  
    outs:  
      - data/interim/transformed.csv  
  aggregate:  
    cmd: python src/data/aggregate.py -i data/interim/transformed.csv -o data/processed/final.csv  
    deps:  
      - data/interim/transformed.csv  
    outs:  
      - data/processed/final.csv
```

This will generate a sequence of three commands that will process a file located at *data/external/file.csv* and spit out a file that can be used for model training at *data/processed/final.csv*. We can review a graph of stages with `dvc dag path/to/dvc.yaml.` The example above will generate the following DAG:

![an example dvc dag with three stages](https://cdn-images-1.medium.com/max/1200/1*TDv-9TNquruqeleRbH_zpg.png)

an example dvc dag with three stages

#### 4. Run DVC pipeline

To actually run a DVC pipeline we simply need to execute the `dvc repro`command. If we make any changes, we can simple execute `dvc repro`again. DVC will automatically determine which stages need to be re-run based on changes to input data and code, and only execute those stages that need to be updated.

---

Using DVC pipeline stages provides several benefits for managing machine learning workflows. First, it promotes modularity and flexibility by allowing you to easily add, remove, or modify stages in the pipeline. This makes it easier to experiment with different approaches and iterate on your workflow over time. Additionally, by tracking the inputs and outputs for each stage in the pipeline, DVC can automatically determine when a stage needs to be re-run based on changes to the input data or code. This saves time and reduces errors by ensuring that each stage is run with the correct input data and code. One of the key benefits of using DVC pipeline stages is that the outputs for each stage are tracked automatically. This means that when a pipeline stage is executed, DVC knows exactly which inputs are needed for the stage and which outputs are generated by the stage.

DVC provides two useful tools for reviewing pipeline stages and commands: `dvc dag` and `dvc repro --dry`. `dvc dag` is a command that generates a directed acyclic graph (DAG) of the pipeline stages in a DVC project. Each node in the DAG represents a pipeline stage, while edges represent the input-output dependencies between stages. `dvc repro --dry` is a command that simulates the execution of the pipeline stages in a DVC project, without actually executing any commands.

`vars` and `params.`yaml are two other features that can be added to the `dvc.yaml` file to make it more flexible and customizable. `vars` allow us to define variables that can be used across multiple stages, or they can be imported from a `params.yaml` file. Stage descriptions are another feature that can be added to each stage in the `dvc.yaml` file to improve readability and understanding of the pipeline (use `dvc stage list` to print out a sequence of stages and their descriptions). `foreach/do` loops are a powerful feature that can also be added to the `dvc.yaml.` For example, `foreach/do` can be used to generate multiple training datasets with different hyper-parameters by iterating over a list of possible hyper-parameter values.

### Real-world example

This is a data prep pipeline from one of my projects to train a semantic segmentation model based on satellite imagery from the [SAR domain](https://asf.alaska.edu/information/sar-information/what-is-sar/). I start from a folder of raw satellite imagery and respective annotations and transform them into files that can be used to create a *data loader* for training a deep learning model.

```
vars:  
  - target_resolution: -1  
    tile_size: 1024  
    stride: 0  
    sar_filters:  
      - filters: '["rescale","refined_lee"]'  
        name: refined_lee  
      - filters: '["rescale", "lee"]'  
        name: lee  
      - filters: '["rescale","bilateral"]'  
        name: bilateral  
    test_size: 0.25  
    external_data: data/external/segmentation  
    annotations: data/external/annotations  
    interim_data: data/interim/segmentation  
    processed_data: data/processed/segmentation  
  
stages:  
  tile:  
    desc: "Tile satellite data and annotations"  
    cmd:  
      - >-  
        python main.py run_tiler  
        ${external_data}  
        ${annotations}  
        ${interim_data}/tiles  
        --tile-size=${tile_size}  
        --resolution=${target_resolution}  
        --stride=${stride}   
        --log-file=${interim_data}/logs/tiler.log  
    deps:  
      - ${external_data}  
      - ${annotations}  
      - src/data/tiler.py  
    outs:  
      - ${interim_data}/logs/tiler.log  
  to_masks:  
    desc: "Convert the geojson annotations to masks"  
    cmd:  
      - >-  
        python main.py gen_masks  
        ${interim_data}/tiles  
        --log-file ${interim_data}/logs/gen_masks.log  
    deps:  
      - ${interim_data}/logs/tiler.log  
    outs:  
      - ${interim_data}/logs/gen_masks.log  
  prep:  
    foreach: ${sar_filters}  
    do:  
      desc: "Apply ${item.name} filter to the raw data"  
      cmd:  
        - >-  
          python main.py sar_filters  
          ${interim_data}/tiles/images  
          ${interim_data}/prep/${item.name}/images  
          --filters '${item.filters}'  
          --log-file ${interim_data}/logs/prep_${item.name}.log  
      deps:  
        - ${interim_data}/logs/tiler.log  
        - ${interim_data}/logs/gen_masks.log  
        - ../../../src/data/sar.py  
      outs:  
        - ${interim_data}/logs/prep_${item.name}.log  
  split:  
    foreach: ${sar_filters}  
    do:  
      desc: "Split ${item.name} data into train and test sets"  
      cmd:  
        - >-  
          python main.py split_files  
          ${interim_data}/prep/${item.name}  
          ${processed_data}/${item.name}  
          --test-size ${test_size}  
      deps:  
        - ${interim_data}/logs/gen_masks.log  
        - ${interim_data}/logs/prep_${item.name}.log  
      outs:  
        - ${processed_data}/${item.name}
```

This is an example of a `dvc.yaml` file that defines a pipeline with four stages: `tile`, `to_masks`, `prep`, and `split`. The file also includes a `vars` section that defines variables used throughout the pipeline.

1. First, the `tile` stage runs a command that tiles the `external_data` and `annotations` into small images with a given `tile_size`, and then saves them to the `interim_data` directory.
2. Next, the `to_masks` stage runs a command that converts the geojson annotations to masks and saves them to the `interim_data` directory.
3. The `prep` stage applies despeckling filters to the tiled images in the `interim_data` directory using the `sar_filters` list and saves them to the `interim_data/prep` directory.
4. Finally, the `split` stage splits the preprocessed data into train and test sets with a specified `test_size` and saves them to the `processed_data` directory.

The `foreach/do` feature is also used in the `prep` and `split` stages, allowing the commands to be run multiple times with different variables specified in the `sar_filters` list. Each iteration creates a subdirectory with a unique name based on the `item.name` variable specified in the `vars` section. Running `dvc stage list` will display the following list of commands:

```
tile      Tile satellite data and annotations  
to_masks  Convert the geojson annotations to masks  
prep@0    Apply refined_lee filter to the raw data  
prep@1    Apply lee filter to the raw data  
prep@2    Apply bilateral filter to the raw data  
split@0   Split refined_lee data into train and test sets  
split@1   Split lee data into train and test sets  
split@2   Split bilateral data into train and test sets
```

`dvc dag dvc.yaml` command will generate the following graph displaying relationships among stages.

![dvc dag output starting from tile command and ending in three split commands.](https://cdn-images-1.medium.com/max/1200/1*6k3CgskFGI4T-JAAsFS7uQ.png)

dvc dag output starting from **tile** command and ending in three **split** commands.

---

Data versioning and tracking are essential in data science projects, and DVC is a powerful tool that can help manage these tasks efficiently. DVC provides features such as data versioning, data tracking, and data pipelines to manage data in a structured and organized manner. By adopting DVC, data scientists can easily collaborate with their team members, reproduce their experiments, and track their progress throughout the project’s lifecycle. Additionally, by combining DVC with other tools such as CI/CD pipelines and project templates, data scientists can achieve more efficient and streamlined workflows, ultimately leading to better project outcomes. I’ve also written about leveraging Gitlab CI/CD to automate model training, check out the link below.

[https://medium.com/me/stats/post/71680976b2c2](https://medium.com/me/stats/post/71680976b2c2?source=main_stats_page)

DVC pipelines can also be used to run multi-step pipelines for training models and automatically tracking model outputs and metrics. I’m planning to write more about it, let me know in the comments if you want to find out more about specific details. If you find this article useful, please subscribe and share it with others.
