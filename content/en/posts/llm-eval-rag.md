---
title: "LLM evaluation for RAG applications"
date: 2024-04-17
slug: "llm-eval-rag"
canonicalURL: "https://medium.com/@rustemgal/llm-evaluation-for-rag-applications-9a281dd75b00"
author: "Rustem G"
---

Recently, I’ve immersed myself in the world of LLMs and generative AI. My goal was to integrate open-source LLMs with external knowledge…

---

Recently, I’ve immersed myself in the world of LLMs and generative AI. My goal was to integrate open-source LLMs with external knowledge base. Here I’m sharing a high-level overview of how I’ve picked the best LLM for our use-case and later on I’m going to present a more detailed discussion on each of the topics.

---

### It’s easy

In the world of LLM applications the development and integration of tools have significantly simplified the deployment and utilization process. The ecosystem surrounding these tools is evolving at an unprecedented pace, negating the need for individual developers or organizations to dive into the complexities of training or fine-tuning their models.

**Ecosystem.** The evolution of the tools like [LangChain](http://langchain), [LlamaIndex](http://docs.llamaindex.ai/), and [Haystack](https://haystack.deepset.ai/), has drastically simplified the development and deployment of LLM applications by providing plug-and-play components. Furthermore, the tools boast a large number of integrations with other tools which saves a significant amount of time during experimentations.

**No more model training.** The emergence of LLMs has revolutionized AI applications by removing the need to train custom deep learning models. Users can now achieve a wide range of outputs by simply inputting specific prompts into pre-trained LLMs, covering everything from content generation to problem-solving.

### RAG overview

The intrinsic limitation of Large Language Models is that their knowledge is confined to the data on which they were trained, which naturally leads to the question of how to make LLMs aware of external, perhaps more current or specialized, documentation. This is where Retrieval-Augmented Generation (RAG) comes into play, bridging the gap between static LLM knowledge and dynamic external information sources.

RAG operates by augmenting the generative process of LLMs with a retrieval component that fetches relevant documents or data in response to a query. This approach allows LLMs to dynamically incorporate external documentation into their responses, effectively extending their knowledge base beyond the initial training data. RAG is usually implemented in two stages.

#### **1. Index documents**

The process begins with chunking documents into manageable pieces, followed by the use of a document embedding model to index these chunks effectively.

![Load documents, split into chunks, embed chunks and index to a vector db (source: langchain)](https://cdn-images-1.medium.com/max/1200/0*gTWJhS5bKVHgEoOe.png)

Load documents, split into chunks, embed chunks and index to a vector db (source: [langchain](https://python.langchain.com/docs/use_cases/question_answering/))

#### **2. Retrieve and generate an answer**

When new queries are received, the system searches for the most similar documents in the index.Retrieved documents are fed into an LLM, which then generates a tailored response.

![Find relevant documents and prompt an LLM to build an answer (source: langchain)](https://cdn-images-1.medium.com/max/1200/0*6q7tOLJfe63NPmru.png)

Find relevant documents and prompt an LLM to build an answer (source: [langchain](https://python.langchain.com/docs/use_cases/question_answering/))

### LLM serving

Serving LLMs presents a unique set of challenges due to their size and complexity. These models require significant computational resources for operation, making them difficult to deploy in environments with limited processing power or memory.

Enter [Ollama](http://ollama.ai/), a solution designed to mitigate these hurdles. *Ollama* simplifies the process of downloading and running models. The ease with which *Ollama* can be set up and operationalized underscores the shifting dynamics in the LLM ecosystem. Downloading and running a state-of-the-art LLM is as-easy-as:

```
ollama pull llama2  
ollama pull mixtral  
ollama pull qwen  
ollama pull falcon  
# etc.  
  
# generate answer inline  
ollama run mixtral "Tell me a techie joke"  
  
# start interative chat  
ollama run falcon  
> My user query here
```

### LLM Comparison setup

When it comes to evaluating LLMs, the comparison setup can vary significantly based on several factors such as hosting options, model size, licensing, and computational requirements. On one end of the spectrum, self-hosted, small, open-license models offer flexibility and ease of use for developers with limited resources. These lightweight models are ideal for prototyping and small-scale applications. On the other end, default and heavyweight models, although requiring more substantial computational resources, provide unparalleled performance and accuracy, suitable for enterprise-level applications.

Choosing between these models involves a trade-off between computational overhead and the quality of the generated content. Lightweight models can be quickly deployed and run on minimal hardware, making them accessible to a broader range of developers. In contrast, heavyweight models, while more demanding, unlock the full potential of LLMs, offering deep, nuanced, and contextually relevant responses.

![Gemma and qwen are more efficient in terms of throughput and disk space](https://cdn-images-1.medium.com/max/1200/1*vKwjj-3P4N_Eta1FsW1X-w.png)

Gemma and qwen are more efficient in terms of throughput and disk space

### Promptfoo — experiment tracking with unit-tests

[PromptFoo](http://promptfoo.dev/docs/) is a node.js-based LLM comparison tool designed to streamline the selection and optimization of Large Language Models (LLMs) for specific tasks. This tool simplifies the initial setup, allowing users to quickly start testing and comparing different LLMs. By blending the structured approach of unit tests with the dynamic tracking of machine learning experiments, `promptfoo` provides a systematic way to evaluate model performance and behavior against a series of tasks or challenges, ensuring each model meets predefined criteria.

With its user-friendly configuration and intuitive UI, PromptFoo makes it accessible for users of all technical levels to adjust parameters and monitor the impact of hyper-parameter changes or test data adjustments on model performance. This tool is essential for optimizing LLM behavior before production deployment, helping organizations to mitigate risks and enhance the reliability and effectiveness of their LLM applications in real-world scenarios.

![promptfoo llm evaluation review page](https://cdn-images-1.medium.com/max/1200/1*RpQEXx_CICKJW0EKCEFiwQ.png)

promptfoo llm evaluation review page

### Results

The evaluation of Large Language Models across different categories reveals a varied spectrum of performance in standardized testing scenarios. In the heavyweight category, **llama2–70b** and **qwen-72b** both recorded impressive scores, each achieving an **87.5%** pass rate. This indicates a robust capability in handling complex tasks that demand extensive understanding and generation abilities. However, **falcon**, despite its 40 billion parameters, lagged behind with a pass rate of 62.5%, suggesting potential areas for improvement in certain aspects of its modeling.

On the other hand, the default models showcased a mixed range of outcomes, with **mixtral** and **llama2** both achieving the highest scores at 87.5%, mirroring the performance of their heavyweight counterparts. **Gemma** and **jais-13b** both scored 50%, indicating moderate reliability, while **qwen** and **falcon** displayed lower efficacy at 25% and 12.5%, respectively, highlighting a variance in model performance at this level.

![Test case pass rate for default size LLMs](https://cdn-images-1.medium.com/max/1200/1*68nlX1EN5vpDB_wlCyzAkA.png)

Test case pass rate for default size LLMs

The lightweight models demonstrated the challenges smaller models face in comprehensive tasks, with **gemma** at 50% and **qwen** at just 12.5%. In stark contrast, OpenAI models, **chatgpt-3.5-turbo** and **chatgpt-4**, both achieved perfect scores of 100%, underscoring their advanced capabilities and the effectiveness of their training and underlying architecture.

### Conclusion

This article has provided a high-level overview of the tools and methodologies involved in evaluating Large Language Models (LLMs), highlighting the importance of selecting and optimizing the right model for specific tasks. From leveraging powerful tools like PromptFoo to understanding the nuances of Retrieval-Augmented Generation (RAG), the landscape of LLM evaluation is both broad and intricate.

In future discussions, I will delve deeper into each of these topics, providing more detailed insights and practical examples to further enhance our understanding and application of these advanced technologies in various domains. Stay tuned for more in-depth exploration into the world of LLM evaluation.

*If you found this overview intriguing and are eager to dive deeper into the world of LLM applications, make sure to subscribe for updates and join us on this journey to unlock the full potential of language models in your applications.*
