---
title: "How to share ML experiments and code"
date: 2024-05-30
slug: "share-ml-experiments"
canonicalURL: "https://medium.com/@rustemgal/how-to-share-ml-experiments-and-code-38b29bedc5bf"
author: "Rustem G"
---

Narrative-driven documentation in machine learning helps reach more people by making experiment results and code easily understandable.

---

In the fast-paced world of machine learning, the significance of narrating experiments and documenting them is often overlooked. By creating structured, narrative-driven documentation, we can effectively share the journey of our experiments, making the results and code easily reusable and comprehensible.

---

#### Problem

In the realm of machine learning (ML), sharing and reusing code is a crucial yet often overlooked aspect. Despite the abundance of commonalities across ML projects, code snippets and functionalities are frequently reinvented from scratch.

Moreover, while experiment tracking tools like MLflow or TensorBoard are excellent for monitoring and visualizing experiment metrics, they fall short in providing a narrative or comprehensive documentation that explains the context, decisions, and rationale behind the experiments.

#### Solution

To address these challenges, creating detailed documentation that narrates the story of your experiments can be invaluable. Such documentation should not only describe the features and outcomes of the project but also include reusable code snippets, detailed explanations of methodologies, and insights into the decision-making process. This is where [MkDocs](https://www.mkdocs.org/) comes into play — a powerful yet user-friendly static site generator that is perfect for creating project documentation.

![With a basic functionality we are getting a multi-page site with navigation and search](https://cdn-images-1.medium.com/max/1200/1*bzcxlWZ0xcE3BFI4aUSkFg.gif)

With a basic functionality we are getting a multi-page site with navigation and search

---

#### Why MkDocs?

MkDocs is renowned for its simplicity and versatility, making it an ideal choice for documenting ML experiments. It allows you to create a professional-looking documentation site with minimal effort. Here’s why MkDocs stands out:

* **Ease of Use**: MkDocs is straightforward to set up and configure.
* **Versatile Features**: It supports various themes and plugins to enhance functionality and aesthetics.
* **Markdown Support**: It allows the integration of Markdown files for easy documentation creation.
* **Extensibility**: MkDocs can be extended with a multitude of plugins to parse docstrings, code parameters, and more.

---

#### **Crafting a Compelling Story**

Sharing the results of machine learning experiments is more than just presenting numbers and metrics; it’s about narrating a journey of discovery, decisions, and iterations. One effective way to convey this narrative is by using a changelog format. A [changelog](https://keepachangelog.com/) is traditionally used to document changes and updates in software development, but it can be adeptly adapted to tell the story of an ML experiment. Here’s how you can generate a great story using this format.

[Keep a Trainlog for machine learningIf you’re looking for a way to store a history of model changes, consider keeping a trainlog. Similar to a changelog, a…medium.com](https://medium.com/@rustemgal/keep-a-trainlog-8ee35553c0bd)

#### **Structuring the Changelog**

A well-structured changelog serves as a timeline, capturing the evolution of your ML project. Start by categorizing your updates chronologically, and break them down into meaningful entries. Each entry should include:

* **Date and title**: When the changelog was updated and a short title.
* **Changes**: A brief description of the changes.
* **Results:** A human-readable summary of improvements achieved during experimentation.
* **Lessons learnt and new ideas**: Description of experiment outcome (especially negative results) and a shortlist of ideas for next iteration.

#### **Example Entry**

Here’s an example of how an entry in your changelog might look:

```
## 2024-05-15 - hyper-parameter tuning
```

#### **Emphasizing the Narrative**

To make your changelog more engaging, weave a narrative around your experiments. Start with a **problem statement** that sets the stage for each entry. Describe the **motivation** behind each change — what challenges or limitations you were facing, and why you chose a particular approach to address them.

Incorporate **insights and learnings**. This not only highlights the progress but also shares valuable knowledge with others who might be tackling similar issues. Discuss what worked, what didn’t, and any surprising findings. For instance, mention if a certain hyper-parameter had an unexpected impact or if a particular technique drastically improved performance.

**Using Visuals**

Enhance your changelog with visuals like graphs, charts, and diagrams. Visual aids can help illustrate the impact of your changes more clearly. For example, include a graph showing the accuracy improvement over different iterations or a diagram explaining the modified neural network architecture. Tools like MkDocs with plugins such as mermaid2 can help integrate these visuals seamlessly into your documentation. Alternatively, it might be easier to link the charts from experiment tracking tools.

![Adding importaining experiment metrics improves storytelling](https://cdn-images-1.medium.com/max/1200/1*FV5NN-nTzqiQz6dbrcr3Ig.png)

Adding importaining experiment metrics improves storytelling

**Keeping it Up-to-Date**

A changelog is a living document that should be regularly updated. Each new entry builds on the previous ones, gradually painting a comprehensive picture of your project’s journey. Make it a habit to update the changelog immediately after each significant experiment. This ensures that all details are fresh and accurately recorded.

**Encouraging Collaboration**

Lastly, a well-maintained changelog can foster collaboration. By documenting your thought process and results, you invite feedback and suggestions from peers. This can lead to new ideas, alternative approaches, and even potential collaborations. Share your changelog within your team or with the broader ML community to leverage collective expertise.

![The best way to maintain a research project is through using version-control systems.](https://cdn-images-1.medium.com/max/1200/1*yxoXCB7gWhv1gFIkfStAHA.png)

The best way to maintain a research project is through using version-control systems.

---

**Getting Started**

Install `mkdocs` and create a new MkDocs project with the following commands:

```
pip install mkdocs  
mkdocs new my-project  
cd my-project
```

This will create a basic project structure that you can build upon.

#### **Project Structure**

A typical MkDocs project has the following structure:

```
my-project/  
    docs/  
        index.md  
    mkdocs.yml
```

* **docs/**: This directory contains your Markdown documentation files.
* **mkdocs.yml**: This is the configuration file for your MkDocs.

#### Config

The **mkdocs.yml** file is the heart of your MkDocs project. Here’s an example configuration:

```
site_name: My ML Project  
theme:  
  name: 'material'  
nav:  
  - Home: index.md  
  - Changelog: changelog.md  
plugins:  
  - search
```

This will create a documentation with two pages:

1. **Home** — with the contents of the *docs/index.md* file.
2. **Changelog** — with the contents of the *docs/changelog.md* file.

#### **Navigation and Pages**

MkDocs allows you to create a clear and organized navigation structure for your documentation. The *nav* section in the *mkdocs.yml* file defines the navigation menu for your site. Here’s how you can structure it:

```
nav:  
  - Home: index.md  
  - API Documentation:  
      - Overview: api.md  
      - Modules:  
          - Module1: modules/module1.md  
          - Module2: modules/module2.md  
  - Changelog: changelog.md  
  - About: about.md
```

This configuration creates a hierarchical navigation menu that helps users easily find the information they need. Each item in the nav section points to a Markdown file inside the ./docs folder, allowing you to organize your documentation into sections and subsections.

#### Serve and build

Once we have the basic structure and configuration, we are ready to serve the website and check in a browser. Run the following command and open `localhost:8000` in your browser.

```
mkdocs serve
```

Keep editing files inside *docs/* folder and monitor the page for live updates. Once satisfied with the results, build the site and upload the*./site* folder contents to a static site server (a public S3 folder works as well).

```
mkdocs build -d ./site
```

---

#### **Conclusion**

Using a changelog format to document and share your ML experiments transforms a simple log into a compelling narrative. It provides a structured yet flexible way to record progress, share insights, and foster collaboration. By meticulously documenting each step, you create a valuable resource that not only tracks your journey but also guides others on similar paths.

Moreover, leveraging MkDocs to tell the story of your ML experiments can significantly boost the outreach of your project. MkDocs makes it easy to create professional, visually appealing documentation that is both accessible and engaging. This approach ensures that your documentation is not only comprehensive but also easy to maintain. As your project evolves, updating your documentation is straightforward, keeping it aligned with the latest developments.

*In the follow-up post we will discuss how to use plugins to make mkdocs documentation more appealing for readers with nifty and easy-to-use tools, as well as how to automate builds on GitHub. Subscribe to stay updated.*
