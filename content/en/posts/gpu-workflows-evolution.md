---
title: "From notebooks to agents: Evolution of GPU workflows in deep learning"
date: 2024-03-20
slug: "gpu-workflows-evolution"
canonicalURL: "https://medium.com/@rustemgal/from-notebooks-to-agents-evolution-of-gpu-workflows-in-deep-learning-154b480ec47d"
author: "Rustem G"
---

Explore the transformative journey from the simplicity of Jupyter notebooks to the cutting-edge efficiency of remote agents in GPU…

---

Embarking on deep learning projects often necessitates powerful computational resources, with GPUs being at the forefront due to their efficiency in handling large-scale data and complex algorithms. Thus, it’s essential for every deep learning practitioner to learn to harness the power of GPUs efficiently.

My journey through utilizing remote GPUs for deep learning has been evolutionary, transitioning from basic setups like Jupyter notebooks to more sophisticated systems like remote execution. Here’s a detailed exploration of each approach, complete with relevant code samples, reflecting the progression from simplicity to complexity.

---

### Jupyter notebooks server

[Jupyter Notebooks](https://jupyter.org/) are an indispensable tool familiar to virtually every data scientist and machine learning researcher. Renowned for their flexibility and ease of use, they serve as the go-to starting point for most individuals in the field. These interactive notebooks provide a user-friendly interface that blends code, visualizations, and text in a single document, making them an ideal platform for exploratory data analysis, prototyping, and quick experimentation.

Initially, my approach revolved around running Jupyter notebooks within Docker containers on a remote server thourgh SSH. Additionally, I configured port forwarding to facilitate local access to the notebooks, and handled data management through manual uploads. While this method was relatively straightforward and leveraged the strengths of both Jupyter and Docker, it presented challenges, particularly in the areas of maintaining code version history and data tracking.

#### Spin up a docker container with jupyter notebook server

The first step is to create a *Dockerfile* with a *cuda* version matching your *nvidia* drivers and *pytorch* and required *python* packages:

```
FROM my-nvidia-cuda-image:11.3-py310-torch2  # custom image with python=3.10 and torch==2  
RUN pip install jupyterlab notebook nbclassic  
RUN pip install transformers accelerate bitsandbytes  
RUN pip install langchain langchain-community langchainhub langchain-openai lancedb bs4 pandas  
RUN apt-get update && apt-get install -y git
```

Accompany this *Dockerfile* with a *docker-compose.yml* to automatically:

* persist all of your workspace files;
* expose ports for accessing notebooks;
* access nvidia gpus;
* enable aremote access.

```
services:  
  jupyter:  
    build: .  
    image: jupyter:11.3-py310-torch2  
    container_name: jupyter-notebook  
    ports:  
      - 8898:8888  
    environment:  
      - NVIDIA_VISIBLE_DEVICES=all  
    volumes:  
      - .:/workspace  
      - $HOME/.cache:/root/.cache  
    working_dir: /workspace  
    command: "jupyter nbclassic --ip=0.0.0.0 --no-browser --allow-root"  
    deploy:  
      resources:  
        reservations:  
          devices:  
          - driver: nvidia  
            count: all  
            capabilities: [gpu]
```

With the setup above, running a jupyter notebook with a complete environment setup on a any server becomes a breeze:

```
docker compose -f path/to/docker-compose.yml run jupyter --service-ports
```

This will print a jupyter access token that you can paste in your browser for jupyter at `http://server-ip-address:8898`.

**Pros:**

* **Easy Setup:** The process is straightforward, making it accessible even for those new to Docker or remote environments.
* **Continuity:** Users can maintain their existing workflows and preferences within Jupyter notebooks, ensuring a smooth transition to a remote setup.
* **Flexibility:** Offers the ability to tailor the environment, libraries, and tools to specific project needs through interactive package management or Dockerfile customization.

**Cons:**

* **Reproducibility:** Challenges in ensuring consistent environments, data files and results, especially when notebooks and dependencies are not meticulously tracked.
* **Version control: T**his approach often leads to overlooking code tracking and review.
* **Manual** data uploads and downloads: Requires hands-on management of data and models, which can be time-consuming and prone to errors, especially with large datasets or numerous model artifacts.

---

### CI/CD to Train Models

Despite the initial ease and familiarity of using Jupyter notebooks, I soon found myself grappling with its limitations, particularly in terms of reproducibility, experiment sharing, and the cumbersome process of manually handling data and models. This dissatisfaction spurred me to seek more robust and scalable solutions for running my deep learning experiments on GPUs.

After exploring various options, I settled on integrating [GitLab CI/CD](https://docs.gitlab.com/ee/ci/yaml/) into my workflow. GitLab CI/CD provided a highly flexible and efficient platform to create automated and reproducible workflows. This framework not only streamlined the experiment process but also significantly enhanced collaboration and version control, aligning perfectly with the needs of our growing deep learning projects. (Check my post below on how to build CI/CD pipelines with Gitlab.)

[Automate model training with CI/CDWould you believe if I told you that our team trains deep neural nets on a remote GPU machine with a single git commit…medium.com](https://medium.com/@rustemgal/streamline-deep-learning-model-training-with-ci-cd-71680976b2c2)

Yet another step further, integrating GitLab CI/CD with Data Version Control (DVC) offers a robust solution for managing large datasets and external files in machine learning projects. DVC can enhance an existing pipeline by providing version control for datasets and machine learning models, allowing for efficient tracking of data changes and ensuring that the correct version of data is used during each run. In the GitLab CI/CD pipeline, DVC can be set up to automatically pull the latest data before the training process begins and/or track resulting model versions.

#### Pipeline setup

Creating a pipeline for code tracked with Gitlab and integrated gitlab-runners is as easy as adding a `gitlab-ci.yml` file (below) to a git repository, committing and pushing it to gitlab.

```
stages:  
  - build
```

The `.gitlab-ci.yml` pipeline is structured into distinct stages: building the Docker image, fetching the latest data with DVC, and training the model. The `build` stage compiles a Docker image with all necessary dependencies. The `pull` stage uses the docker image to execute `dvc pull`, syncing the most current data files. Finally, the `train` stage uses the updated Docker environment and data to train the machine learning model. The `rules` directive is employed to conditionally execute jobs, specifically targeting actions when the main branch is involved.

**Advantages:**

* Code is version-controlled, and the training process is automated and reproducible.
* Facilitates collaboration through shared experiments and centralized data storage.

**Challenges:**

* Requires understanding of CI/CD concepts and GitLab configuration.
* Pipeline maintenance can be complex, especially for large-scale projects.

---

### Remote execution with ClearML agents

Transitioning from the structured and automated workflows of GitLab CI/CD, we pivot to the dynamic and flexible environment of ClearML Agents. This shift marks a progression towards an even more refined control over remote experiment execution, harnessing the power of ClearML’s seamless integration for comprehensive experiment tracking and management, particularly on remote GPU machines.

ClearML is a versatile end-to-end MLOps platform designed to streamline the lifecycle of machine learning projects. One of the standout features of ClearML is the [ClearML Agent](https://clear.ml/docs/latest/docs/clearml_agent/), a powerful component that enables the remote execution of code, particularly beneficial for leveraging remote GPU resources. This means that developers can effortlessly run their training scripts or entire workflows on remote servers equipped with GPUs, without the need for complex setup or constant monitoring.

![ClearML remote execution overview (source: clearml-agent docs)](https://cdn-images-1.medium.com/max/1200/0*rTBkr5WDlO8rZeXy.png)

ClearML remote execution overview (source: clearml-agent docs)

The agent listens for tasks queued in the ClearML Server and executes them on the designated machine, automatically logging all experiment details, outputs, and artifacts. This not only maximizes the utilization of GPU resources but also allows for scalability and flexibility in managing machine learning experiments. Users can trigger experiments from their local machine, push them to a queue, and let the ClearML Agent handle the rest, ensuring that the compute-intensive training processes are offloaded to powerful remote servers once a worker is free to accept new tasks.

#### Spin up a clearml agent

To start a ClearML Agent on a **remote machine with GPU support**, you first need to ensure that ClearML is installed and then start the agent. Here’s how you can do it:

```
# Install ClearML Agent  
pip install clearml-agent  
  
# Configure connection to clearml-server  
clearml-agent init  # follow prompts  
  
# Start the ClearML Agent  
clearml-agent daemon --queue my_gpu_queue --docker --detach --gpus 0,1,2,3
```

After successfully spinning up a ClearML Agent and specifying a queue name for it to listen to, this specific queue should automatically appear in the ClearML frontend within the “Queues & Workers” section. This section provides a real-time overview of all the active queues and the connected agents (workers) that are listening to them. The appearance of your queue in this section confirms that the agent is operational and ready to receive tasks.

#### Create a ClearML Remote Execution Task

To create a task programmatically that you intend to run remotely, use the following Python code:

```
# Initialize ClearML Task  
  
from clearml import Task  
task = Task.init(project_name='my_project', task_name='my_remote_task')  
task.connect(training_params)  
  
# Configure Task for Remote Execution  
task.set_base_docker('nvidia/cuda:10.2-cudnn7-runtime-ubuntu18.04')  # Example for a GPU-based docker image  
task.execute_remotely(queue_name=None) # Set a queue name 'my_gpu_queue' to start the execution at once
```

After executing this code a draft task will pop up in the ClearML experiment tracking frontend. In the next step we will schedule it for execution.

#### Enqueue a Task for execution

To enqueue a task from the ClearML web frontend, follow the steps in the screen recording below:

![Execute a task remotely with clearml](https://cdn-images-1.medium.com/max/1200/1*XzfM86H6F7P8YsNUNN44Zw.gif)

Execute a task remotely with clearml

We open a draft task, check execution configuration and update certain hyper-parameters. Finally, we’re ready to enqueue a task for execution on a remote GPU machine. Logs of a task will be available in the “Console” tab and the status of a task will change from pending to failed or completed.

By following these steps, you can seamlessly set up a remote execution environment with ClearML, create tasks programmatically, and manage their execution right from the ClearML frontend, utilizing powerful remote GPUs for your computations.

#### Extra benefits

* ClearML Agent offers seamless integration with ClearML’s experiment tracking.
* Streamlines workflow for enhanced management and monitoring of machine learning tasks.
* Automatic tracking of all task details: hyper-parameters, output metrics, artifacts.
* Enables easy result reproduction and detailed training process analysis with logs retention.
* ClearML Datasets integration simplifies data management in training code.
* Facilitates versioning, tracking, and linking of data to experiments for traceability.

### Conclusion

In conclusion, the journey from Jupyter Notebooks to the sophisticated use of GitLab CI/CD, and ultimately to the dynamic capabilities of ClearML, represents a remarkable progression in managing and executing machine learning workflows. Each approach offers its unique strengths, from the familiarity and interactive nature of notebooks to the structured automation of GitLab pipelines and the advanced experiment tracking and remote execution provided by ClearML Agents. With these tools at their disposal, data scientists and ML engineers are equipped to tackle the challenges of model training and deployment with greater efficiency, reproducibility, and scale. As we continue to push the boundaries of what’s possible with machine learning, the evolution of these tools will no doubt play a pivotal role in shaping the future of AI development and deployment.

*If you’ve enjoyed this dive into the depths of machine learning workflows and the powerful tools that make them more accessible, don’t forget to subscribe for more insights and updates on the cutting edge of AI technology.*
