---
title: "Practical hyper-parameter tuning for any deep neural net"
date: 2023-10-04
slug: "hyperparameter-tuning"
canonicalURL: "https://medium.com/@rustemgal/practical-hyper-parameter-tuning-for-any-deep-neural-net-303cc537fd01"
author: "Rustem G"
---

Whether you’re fine-tuning YOLO, EfficientNet or Unet, hyper-parameter tuning with ASHA can help reduce search time and improve metrics.

---

Whether you’re fine-tuning *YOLO*, optimizing *EfficientNet* and *Vision Transformers*, or delving into the complexities of *Unet*, hyper-parameter tuning can be a solution to long and tedious hours of exploring various model configurations. It can significantly reduce the time spent on model search, yet still be able find the best performing model, while cutting down on CO2 emissions — all in one go.

In this guide, we’ll explore how **Asynchronous Successive Halving Algorithm** can streamline the process of hyper-parameter search, allowing you to achieve better model performance more quickly while adopting eco-friendly computing practices. I will also share some practical tips that help me boost search efficiency and usually result in **3–5%** model improvement (check out the real chart below).

![Efficient hyper-parameter search boosts model metrics by a few percent.](https://cdn-images-1.medium.com/max/1200/1*N42z679jLih-02RVywR3zQ.png)

Efficient hyper-parameter search boosts model metrics by a few percent.

### **Deep learning search space**

Modern practical deep learning models have numerous hyper-parameters, ranging from selecting a backbone to selecting an optimizer, learning rates, batch sizes, and losses, among others. Each hyper-parameter can often take on a wide range of values. This results in an expansive search space, making it challenging to identify the best combination of hyper-parameters manually.

For example, a simple image classification configuration below will generate a total of 720 configurations! At the same time, these are just very basic parameters that are needed to get started with a new task or a new dataset.

```
image_classification_config:  
  backbone:  
    - efficientnet_b0  
    - resnet18  
    - mobilenet_v3_small  
  lr:  
    max: 0.002  
    min: 0.00002  
  image_size:  
    - 224  
    - 112  
  optimizer:  
    - Adam  
    - SGD  
    - RMSprop  
    - Adamax  
    - AdamW  
  augmentation:  
    - default  
    - RandAugment  
    - AutoAugment  
  weights:  
    - None  
    - IMAGENET1K_V1
```

If we continue to optimize our model even further, adding other features such as learning rate scheduling, gradual weights unfreezing or a number of penultimate fully-connected layers, the total number of available configurations will quickly exceed tens of thousands options. It becomes impractical to try all configurations manually. Moreover, there are other aspects that make this process laborious and time-consuming:

* **Trial and error**: Data scientists and machine learning engineers typically start with some initial settings, train the model, evaluate its performance, and then iterate by adjusting hyper-parameters. This process can be time-consuming as it may require many iterations and a substantial amount of waiting time for a training run to complete.
* **Computationally intensive**: Exhaustive grid searches and random searches are among the common techniques used for hyper-parameter tuning. While they provide comprehensive coverage of the search space, they are highly computationally intensive.
* **Lack of generalization**: Hyper-parameters that work well for one dataset or task may not be optimal for another. Finding a set of hyper-parameters that generalizes well across different datasets or tasks can be challenging and time-consuming.
* **Environmental impact.** Running a grid search over these hyper-parameters for 50 epoch and 60 seconds per epoch on a small dataset will result in 600 hours of compute time. It is equal to **64.8 kg of CO2 (**A100 on a private infrastructure),or 252 km driven by a car, according to [this calculator](https://mlco2.github.io/impact/#compute). Considering the fact that only one model is need for production, this results in a lot of wasted computation.

### Hyper-parameter tuning with ASHA

To overcome all of the issues above, modern deep learning needs a solution that can make this process efficient and automated. There are plenty of algorithms that improve grid/random search and one of them stands out as a very efficient in terms of time and metric improvement.

[ASHA](https://arxiv.org/abs/1810.05934), short for **A**synchronous **S**uccessive **H**alving **A**lgorithm, takes its inspiration from SHA (**S**uccessive **H**alving **A**lgorithm) and extends it with a powerful twist — parallel computing.

**Successive halving algorithm**

The SHA algorithm starts by dividing a pool of candidate configurations into different brackets, each with a different number of configurations. The top-performing configurations in each bracket are retained, while the less promising ones are discarded. This process is repeated in successive rounds, with fewer configurations in each subsequent round. The idea is to allocate more computational resources to the configurations that show promise early on, thereby focusing on the most promising candidates.

The concept underlying SHA is straightforward: initially assign a modest resource allocation to each configuration, evaluate all configurations, retain the best 1/η of them, then increment the resource allocation for each configuration by a factor of η. This process continues iteratively until the maximum resource allocation per configuration, denoted as R, is reached. The basic idea for a single bracket can be illustrated in the following table (η=3, R=81):

```
|Rung|# Configuraions|# Epochs|Total budget|  
|---|---|---|---|  
|1|81|1|81|  
|2|27|3|81|  
|3|9|9|81|  
|4|3|27|81|  
|5|1|81|81|
```

At each stage (which is called a “**rung**” in the original paper) the following happens:

1. SHA starts with 81 configurations, each given a small budget of 1 epoch. This totals to a budget of 81 epochs for this step.
2. SHA narrows down the search by selecting the top 1/3 (27) configurations from the previous step and allocates them a budget of 3 epochs each. This again sums up to a total budget of 81 epochs for this step.
3. SHA further prunes the configurations to just 9, and each receives a budget of 9 epochs. The total budget remains at 81 epochs.
4. SHA retains only 3 configurations and provides each with a larger budget of 27 epochs, still keeping the total budget constant at 81 epochs.
5. Finally, SHA selects the single best configuration and allocates the entire budget of 81 epochs to it.

SHA’s strength lies in its ability to quickly identify and prioritize the most promising hyper-parameter configurations. However, it operates in a sequential manner, which means that it can be computationally expensive, especially when dealing with a large number of hyper-parameters combinations.

**Asynchronous SHA**

To address this limitation, the Asynchronous Successive Halving Algorithm builds upon SHA by introducing asynchronous scheduling and parallel computing, making the hyper-parameter optimization process even more efficient and scalable. ASHA’s parallelism allows it to explore multiple configurations simultaneously, significantly reducing the time required to find the best hyper-parameter settings for deep learning models.

ASHA is especially effective when you have limited time to train models like in large-scale scenarios and/or want to automate the delivery of deep learning models. To put it simply, if you have 9 machines to train a model, ASHA can deliver a fully trained configuration in a time that’s 13/9 times the duration of a single configuration run. This will always be faster than two consecutive model runs. As for comparison to other hyper-parameter tuning algorithms, refer to the chart below.

![ASHA tends to find better model configuration faster than algorithms (source: the original ASHA paper)](https://cdn-images-1.medium.com/max/1200/1*7fIlTdrJNqYsxAyAMzXu7g.png)

ASHA tends to find better model configuration faster than algorithms (source: the original ASHA paper)

**Practical tips**

These practical tips are derived from my personal experience with ASHA and can be applied for efficient hyper-parameter tuning.

1. **Core parameters first**: Start your ASHA hyper-parameter tuning journey by focusing on the core parameters that have the most significant impact on model performance. These could include choices like the *backbone architecture, input size, optimizer,* and *learning rate.* Continue with other parameters after fixing the core ones.
2. **Incremental approach:** ASHA is especially handy when you introduce a new feature such as *progressive learning* or *automated augmentations* and need to test different variations such as *progression steps* or *strength of augmentations*, respectively. You can fix the base model parameters and launch multiple trials with various parameters of a new feature.
3. **Tweak grace period**: ASHA provides a “grace period” during which less promising configurations are allowed to continue before elimination. To fine-tune this aspect, consider adjusting the grace period to allow for learning saturation. This means giving your model more time to stabilize and potentially reveal its true potential before making early judgments. As you progress through different steps of ASHA’s iterative process, consider increasing the grace period.
4. **Parallelization**: ASHA truly excels with a large number of experiments running concurrently. Connect as many GPUs as you have available and utilize device fractions (will be discussed below).

### Raytune implementation

A simple way to get started is to use `ray[tune]` package for hyper-parameter tuning. [Their implementation of ASHA](https://docs.ray.io/en/latest/tune/api/doc/ray.tune.schedulers.ASHAScheduler.html#ray-tune-schedulers-ashascheduler) provides a highly scalable and efficient solution. Next, I am going to demonstrate how to get started fairly quickly with ASHA using *raytune* and [*lightning*](https://lightning.ai/docs/pytorch/stable/)with a simple image classification example.

![Raytune overview (source: raytune website)](https://cdn-images-1.medium.com/max/1200/0*2BMYwPFMb-7SSdwA.png)

Raytune overview (source: raytune website)

[Install torch, torchvision](https://pytorch.org/get-started/locally/) and packages required for this example `pip install ray[tune] lightning` .

#### Session reporting

Regardless of what framework we use for model training, as long as we compute metrics at some intervals we can report them to *raytune* to monitor training progress. Below is an example of how to report validation results after each epoch**:**

```
### Pytorch lightning ###  
import lightning as pl  
  
  
# only report metrics that start with "val"  
class RaytuneCallback(pl.Callback):  
    def on_validation_epoch_end(  
        self, trainer: pl.Trainer, pl_module: pl.LightningModule  
    ) -> None:  
        metrics = {  
            k: v.item()  
            for k, v in trainer.callback_metrics.items()  
            if k.startswith("val")  
        }  
        session.report(metrics)  
  
  
# log metrics during training  
class MyCustomLightningModel(pl.LightningModule):  
    def validation_step(self, batch, batch_idx):  
        x, y = batch  
        preds = self.model(x)  
        loss = self.loss(preds, y)  
        self.log("val/loss", loss.item(), on_epoch=True, on_step=False)  
        self.val_metric(preds, y)  
        self.log("val/acc", metric, on_epoch=True, on_step=False)  
        return loss
```

#### Objective function

Then we need to define an “objective” function i.e. a python function that launches model fitting and runs for a specified number of epochs. We are going to use [*pydantic*](https://docs.pydantic.dev/latest/) to validate inputs and create a usual *lightning* script with the *raytune* callback from the previous step:

```
class ImgClfConfig(BaseModel):  
    data: str = Field(..., description="Path to dataset")  
    backbone: str = Field("resnet18", description="Backbone model name")  
    weights: str | None = Field(  
        "IMAGENET1K_V1", description="Pre-trained weights or None"  
    )  
    optimizer: str = Field("Adam", description="Optimizer name")  
    lr: float = Field(0.001, description="Learning rate")  
    image_size: int = Field(  
        224, description="Model input shape as int or tuple"  
    )  
    batch_size: int = Field(4, description="Batch size")  
    augmentation: str = Field(  
        "default", description="Image augmentation type"  
    )  
    epochs: int = Field(25, description="Number of epochs")  
  
  
def img_clf_objective(config: dict):  
    config = ImgClfConfig(**config)  
  
    train_loader, val_loader, test_loader = make_dataloaders(config)  
  
    model = MyCustomLightningModel.from_config(  
        config, num_classes=len(train_loader.dataset.classes)  
    )  
    trainer = pl.Trainer(  
        accelerator="gpu" if torch.cuda.is_available() else "cpu",  
        max_epochs=config.epochs,  
        enable_model_summary=False,  # disable prints as many configurations  
        enable_checkpointing=False,  # run at the same time  
        enable_progress_bar=False,  
        callbacks=[RaytuneCallback()],  
    )  
    trainer.fit(model=model, train_dataloaders=train_loader, val_dataloaders=val_loader)  
    *_, test_results = trainer.test(model=model, dataloaders=test_loader)
```

#### Search space

Next, we will use *raytune* methods in order to define a search space for our hyper-parameters. There are two major types of sampling methods: choosing from a list of available values or sampling from a distribution. We can use `tune.grid_search` for categorical variables and `tune.uniform` for number variables ([other methods](https://docs.ray.io/en/latest/tune/api/search_space.html) are available as well). A function to apply an appropriate method might look like the following:

```
from ray import tune  
  
  
def get_search_space(v: Any):  
    if isinstance(v, list):  
        return tune.grid_search(v)  
    elif isinstance(v, dict) and ("min" in v and "max" in v):  
        return tune.uniform(v["min"], v["max"])  
    elif isinstance(v, (str, int, float, bool, dict)) or v is None:  
        # return the value itself if it's set for all runs  
        return v  
    else:  
        raise NotImplementedError(f"{type(v)} type is not supported yet.")
```

#### Resource fractions

It is advised to run more experiments in parallel for a more efficient search. *Raytune* also allows us to control which resources should be allocated to each trial. Provided a gpu memory high enough to fit two runs we can run multiple configuration on the same gpu by defining a gpu fraction of **0.5**:

```
objective_with_resources = tune.with_resources(  
    img_clf_objective, {"gpu": 0.5}  
)
```

#### Tuning

Finally, after all preparation steps we can launch hyper-parameter tuning. First, we will define image classification *search space* and *asha config* in a yaml file:

```
# Image classifier parameters  
img_clf:  
  backbone:  
    - efficientnet_b0  
    - resnet18  
    - mobilenet_v3_small  
  lr:  
    max: 0.002  
    min: 0.00002  
  image_size: 224  
  optimizer:  
    - Adam  
    - SGD  
    - RMSprop  
  augmentation:  
    - default  
    - RandAugment  
    - AutoAugment  
  batch_size: 32  
  epochs: 25  
# ASHA configuration parameters  
asha:  
  grace_period: 5  
  reduction_factor: 3  
  max_t: 30
```

Next, we will write a simple function to load the yaml config and launch hyper-parameter tuning with ASHA. All grid search values will be sampled at least once and create all possible combinations among these variables. Another parameter `n_trials` controls how many times a value is sampled from a given distribution. In the following scenario, the grid search variables (*backbone, optimizer, augmentation*) will create 27 different configuration and with `n_trials=3` , the learning rate will be sampled three times for each configuration, resulting in the **total 81 configurations**. Other parameters (*batch\_size, epoch* and *image\_size*) will be set for all experiments.

```
def asha(  
    config: str | dict = "search.yaml",  
    n_trials: int = 3,  
    resource_fraction: float = 0.5,  
):  
    """Search best hyper-parameters using ASHA scheduler.  
  
    Number of actual iterations depends on choices and distribution variables.  
  
    Args:  
        config: path to yaml file with search choices, or a dict.  
        n_trials: how many times to sample for distribution variables.  
  
    Returns:  
        results that contains all configurations and results.  
    """  
    search_params = load_yaml(config)  
    search_config = _get_search_config(search_params)  
  
    search_space = {  
        k: _get_search_space(v) for k, v in search_params[search_config.name].items()  
    }  
    algo = AsyncHyperBandScheduler(**search_params["asha"])  
    objective_with_resources = tune.with_resources(  
        search_config.objective, get_resources(resource_fraction)  
    )  
    tuner = tune.Tuner(  
        objective_with_resources,  
        tune_config=tune.TuneConfig(  
            metric=search_config.metric,  
            mode=search_config.mode,  
            scheduler=algo,  
            num_samples=n_trials,  
        ),  
        param_space=search_space,  
    )  
    results = tuner.fit()  
    print("Best result is:")  
    pprint(results.get_best_result().metrics)  
    return result
```

#### Logging

By default, *raytune* logs all experiment results to TensorBoard. Additionally, all essential logs are printed to the console, allowing real-time progress monitoring. The output includes all hyper-parameters and metrics logged with `session.report()` . We can also see how many iterations each experiment has run. Apart from the final output, *raytune* prints intermediate results, indicating a current best trial and basic stats.

Below are screenshots with sample outputs of a single *raytune* run with many trials.

![Final output of raytune hyper-parameter tuning.](https://cdn-images-1.medium.com/max/1200/1*PTUXA0HY8PhNby8rwtlS8Q.png)

Final output of raytune hyper-parameter tuning.

![Metrics are printed at the end of each trial.](https://cdn-images-1.medium.com/max/1200/1*rqR-I8OAMFKISXAOeL18Rg.png)

Metrics are printed at the end of each trial.

![Hyper-parameters are printed at the start of each trial.](https://cdn-images-1.medium.com/max/1200/1*0elLDnpf7D_T2nQdkZFUNw.png)

Hyper-parameters are printed at the start of each trial.

![Intermediate output includes current best trial and number of finished, pending and running trials.](https://cdn-images-1.medium.com/max/1200/1*1h4TLrv0RSz_hWClDejagw.png)

Intermediate output includes current best trial and number of finished, pending and running trials.

### Conclusion

In summary, ASHA represents a significant leap forward in the practical deep learning. It’s the ultimate time-saver, cutting down arduous hours and days of manual trial and error into a mere fraction of the time. Beyond just saving time, ASHA actively enhances your model’s performance by pinpointing the most effective hyper-parameters. Its ability to identify the strongest configurations while sidelining weaker ones ensures that your models achieve peak potential.

But ASHA offers even more than time savings and model improvement. It’s a resource-efficient solution, reducing computational waste by gracefully terminating less promising runs. Moreover, it encourages a culture of exploration among researchers. ASHA allows you to venture into a wide array of hyper-parameter configurations, facilitating learning through experimentation.

*Subscribe and share this post if you reached this far.*
