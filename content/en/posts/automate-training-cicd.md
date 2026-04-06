---
title: "Automate model training with CI/CD"
date: 2023-02-03
slug: "automate-training-cicd"
canonicalURL: "https://medium.com/@rustemgal/streamline-deep-learning-model-training-with-ci-cd-71680976b2c2"
author: "Rustem G"
---

Would you believe if I told you that our team trains deep neural nets on a remote GPU machine with a single git commit? Keep on reading to…

---

Would you believe if I told you that our team trains deep neural nets on a remote GPU machine with a single git commit? Keep on reading to find out how you can accomplish that as well.

---

Training deep learning models is frequently a manual and time-consuming process, which means it can be difficult to reproduce and it is prone to human errors. Before CI/CD my normal model-research workflow included quite a few manual steps:

1. SSH into our GPU server.
2. Launch a *Jupyter* notebook inside a docker container.
3. Upload data with tools like *rsync*.
4. Experiment with models, evaluate and save the best model.
5. Download the trained model and package it for production.

While this approach may work just fine for cases when a model is trained and deployed only once, it has crucial flaws in a continuous data science workflow when many iterations with models and data are expected. These are just some major problems that might arise along the way:

* Outdated codebase — you can simple forget to commit changes and push it to your central git repository.
* Misplaced data and model files — it is easy to get lost in different versions of data or forget to upload latest data and to download a final model.
* Data pre-processing in production — it has to be recreated once again for production and maintained in sync in two codebases.
* Sharing experiments — your teammates will not be able to access your files, they will have to set up the environment from scratch.

In order to avoid these problems, automated training of deep learning models can be integrated into a CI/CD (Continuous Integration and Continuous Deployment) pipeline, which can greatly streamline the process and make it more efficient. This can be done by incorporating the training process as a step in the pipeline and triggering it automatically when code changes are made.

I will walk you through the steps to make it happen in [Gitlab CI/CD.](https://docs.gitlab.com/ee/ci/)

---

**GitLab CI/CD** is a built-in continuous integration, continuous delivery, and continuous deployment tool that is included with GitLab,. It allows developers to automate the process of building, testing, and deploying their code. Furthermore developers can catch and fix issues early in the development process, and deploy code changes more quickly and reliably.

Similarly to traditional software development, certain model training tasks can also be integrated into CI/CD. After setting up a gitlab repository and connecting gitlab-runners to execute tasks it becomes pretty easy to define CI/CD pipelines. These are general steps to get started:

1. Create a YAML file called a `.gitlab-ci.yml.`
2. Define **stages** and **jobs** that will be run whenever code is pushed to origin. A **stage** is a group of **jobs** that represent a phase in the pipeline. For example, common stages in a pipeline include: *build, test, deploy*. Jobs are individual tasks within a stage that perform a specific action, such as compiling code, running tests, or deploying to a specific environment.
3. For each job, define the necessary scripts and commands to run.
4. Push your code to the repository and trigger a pipeline run. GitLab will automatically run the pipeline and execute the steps defined in the*.gitlab-ci.yml* file.
5. As the pipeline runs, GitLab will show the progress and the output of each stage in the pipeline.
6. If the pipeline completes successfully, the model will be deployed to the production environment.

For example, you could have:

* a build stage that runs your training script;
* a test stage that runs your model against a validation set;
* a deploy stage that deploys the model to a production environment.

```
stages:  
  - build  
  - test  
  - deploy  
  
train_model:  
  stage: build  
  script:  
    - python main.py train --data path/to/train/data --write-model path/to/best.model  
  
eval_model:  
  stage: test  
  script:  
    - python main.py test --data path/to/test/data --model path/to/best.model  
  
upload_model:  
  stage: deploy  
  script:  
    - python main.py --model path/to/best.model
```

This sample setup allows you to automate the entire model training process, from running the training script to testing the model and deploying it to a production environment. This can help save time and resources, and also reduce the risk of human error.

---

In our case we have a DGX server with multiple GPUs, and we have to train our deep neural nets on a remote server with an *ssh* access. Each user has docker rights on that machine, whereas gitlab-runners are installed on a separate machine but are connected in the same network with the DGX.

Considering all of these nuances, we have decided to split out model training into three stages:

1. **Build** — build a docker image and push it to a docker registry. Training and evaluation scripts, pip dependencies and other configuration files are added at this stage. With code updates, a docker image will be re-built to contain all the latest changes. Sample *dockerfile* might look like this:

```
FROM nvidia/cuda:11.3-devel-ubuntu20.04  
  
COPY requirements.txt .  
RUN pip install --no-cache -r requirements.txt  
  
COPY . /app  
WORKDIR /app
```

**2. Pull**— log in to the GPU machine, pull the latest docker image and download training data.

**3. Train** — log in to the GPU machine and launch model training. This step includes model evaluation, best model export to *onnx* and logging metrics and the model to [MLflow tracking server](https://mlflow.org/).

This is our *.gitlab-ci.yml*:

```
variables:  
  # docker image name will correspond to a gitlab project name  
  # and docker tag will be a git branch name  
  DOCKER_IMAGE_TAG: $CI_REGISTRY$CI_PROJECT_NAME:$CI_COMMIT_REF_SLUG  
  # we assume that a user pushing a commit to git is able   
  # to log in to the DGX server  
  USER: $CI_USERNAME  
  # DGX host can be a domain address or IP  
  DGX_HOST: 10.10.10.10  
  MLFLOW_TRACKING_URI: https://my-mlflow-url.com/  
  
before_script:  
  # this script will run before each job  
  - export DGX="-i path/to/private.key -l $USER $DGX_HOST"  
  
stages:  
  - build  
  - pull  
  - train  
  
.trigger-training-commit-message:  
  rules:  
    # model training steps will be only launched if  
    # a commit message starts with "train ..."  
    - if: "$CI_COMMIT_MESSAGE =~ /^train.*/"  
  
build:  
  extends:  
    # we will use the same `rules` for each job  
    - .trigger-training-commit-message  
  stage: build  
  script:  
    # we'll pull and existing docker image if it exists  
    # to save some time during a docker-build process  
    - docker pull -q $DOCKER_IMAGE_TAG || true  
    - >-  
      docker build --cache-from $DOCKER_IMAGE_TAG  
      -t $DOCKER_IMAGE_TAG  
      .  
    - docker push $DOCKER_IMAGE_TAG  
  
pull:  
  extends:  
    - .trigger-training-commit-message  
  stage: pull  
  script:  
    # this script logs in to the DGX machine,  
    # pulls a docker images built during the previous stage  
    # and downloads a training dataset to ./data folder.  
    - >-  
      ssh $DGX <<EOF  
        set -e  
        docker pull --quiet $DOCKER_IMAGE_TAG  
        docker run --rm \  
          -v "$PROJECT_DIR/data/:/app/data/"   
          $DOCKER_IMAGE_TAG bash get_data.sh  
        EOF  
  
train:  
  extends:  
    - .trigger-training-commit-message  
  stage: train  
  timeout: 24h  
  script:  
    # this runs model training, evaluation and logging   
    # inside an nvidia docker container with a GPU #2  
    - >-  
      ssh $DGX <<EOF  
        set -e  
        docker run --rm \  
          -v "$PROJECT_DIR/data/:/app/data/" \  
          -e "NVIDIA_VISIBLE_DEVICES=1" \  
          --runtime nvidia \  
          --shm-size 10g \  
          $DOCKER_IMAGE_TAG python train.py --data data/processed/dataset  
        EOF
```

There can be different strategies as to when to launch a model training as we do not want to do it every time we make a small code change. Some people might prefer to have a dedicated git branch solely for model training, we, on the other hand, have decided to launch model training contingent upon a specific git commit message. I can see a few of benefits of this strategy:

1. It will be hard to train a model unintentionally and we can use [git-flow](https://www.gitkraken.com/learn/git/git-flow) strategy keep our code up-to-date.
2. Training a model requires a commit message — which will always be helpful to go back in history to review changes that cause metrics to improve or decrease.

![If all goes well, we should eventually see this on a gitlab repository’s pipelines page meaning all the stages completed successfully:](https://cdn-images-1.medium.com/max/1200/1*tKBLoAChy3wPmjEOYD3CVg.png)

If all goes well, we should eventually see this on a gitlab repository’s pipelines page meaning all the stages completed successfully:

---

This task may present its fair share of challenges and require a lot of effort, trial-and-error, and patience. However, the sense of accomplishment and satisfaction that comes from overcoming these obstacles and achieving success makes it all worth it in the end. The hard work and determination put in will ultimately pay off in the form of personal and professional growth.

In addition to improving your own skillset, your teammates and yourself from a few months in the future will benefit greatly from an automated CI/CD for model training. Advantages are clear:

* training experiments are essentially *reproducible* as code is always kept up-to-date and data is available to download from shared resources.
* model training *logs* are preserved, you can always go back and read outputs of a logger or a *print* statement.
* a pipeline will encourage a developer to use a centralized storage for experiment tracking and model logging that should be available for every team member.

*If you like the ideas in this post, do not hesitate to share it with your colleagues and friends and ask questions in the comments below.*
