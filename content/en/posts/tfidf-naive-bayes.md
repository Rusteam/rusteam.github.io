---
title: "TfIdf + Naive Bayes beat neural nets"
date: 2023-11-22
slug: "tfidf-naive-bayes"
canonicalURL: "https://medium.com/@rustemgal/tfidf-naive-bayes-beat-neural-nets-a58f9dff3741"
author: "Rustem G"
---

Limited by tight speed requirements of a contest, we’ve built a text classifier that runs at less than 10ms on cpu per one file and exceeds…

---

Limited by tight speed requirements of a contest, we’ve built a text classifier that runs at less than **10ms on cpu** per one file and exceeds **82%** of multi-class accuracy for 29 classes. It’s a simple naive Bayes classifier on top of tf-idf embeddings — a proven and robust approach.

While we’re waiting for the results, I’m going to describe our solution. Make sure to checkout a github repo and hugging face demo (links in the bottom).

### Contest

A second round of the programming language [contest](https://contest.com/) from Telegram ended two days ago. The task consisted in detecting a programming language in a short text snippets. The list of programming languages included 29 programming and markup languages (and TGLANG\_LANGUAGE\_OTHER for non-code files):

```
  TGLANG_LANGUAGE_C  
  TGLANG_LANGUAGE_CPLUSPLUS  
  TGLANG_LANGUAGE_CSHARP  
  TGLANG_LANGUAGE_CSS  
  TGLANG_LANGUAGE_DART  
  TGLANG_LANGUAGE_DOCKER  
  TGLANG_LANGUAGE_FUNC  
  TGLANG_LANGUAGE_GO  
  TGLANG_LANGUAGE_HTML  
  TGLANG_LANGUAGE_JAVA  
  TGLANG_LANGUAGE_JAVASCRIPT  
  TGLANG_LANGUAGE_JSON  
  TGLANG_LANGUAGE_KOTLIN  
  TGLANG_LANGUAGE_LUA  
  TGLANG_LANGUAGE_NGINX  
  TGLANG_LANGUAGE_OBJECTIVE_C  
  TGLANG_LANGUAGE_PHP  
  TGLANG_LANGUAGE_POWERSHELL  
  TGLANG_LANGUAGE_PYTHON  
  TGLANG_LANGUAGE_RUBY  
  TGLANG_LANGUAGE_RUST  
  TGLANG_LANGUAGE_SHELL  
  TGLANG_LANGUAGE_SOLIDITY  
  TGLANG_LANGUAGE_SQL  
  TGLANG_LANGUAGE_SWIFT  
  TGLANG_LANGUAGE_TL  
  TGLANG_LANGUAGE_TYPESCRIPT  
  TGLANG_LANGUAGE_XML
```

One key aspect of the contest was to build a C++ library that runs faster than **50ms per 4096 characters on** **cpu**. No network usage was allowed. Luckily Telegram provided a skeleton to build the library called `libtglang.so` and test it.

### Data

#### Round 1 takeaways

Through the previous round of the ML Competition 2023, we learned several valuable lessons about [their testing data](https://data-static.usercontent.dev/ml2023-r1-dataset.tar.gz). One of the most surprising facts from the first round was that 90% of the files were text files (which were supposed to be labelled as “other”), not code files. This detection of code files versus non-code files counted towards the final score.

Since it was quite difficult to get so many languages accurately, they decided to reduce the number of languages to 29 most popular ones. This substantial reduction simplified the problem to a certain degree, allowing us to narrow our focus and deepen our understanding of these specific languages.

Another interesting note was that most of the provided code files had only few lines of code snippets, whereas most people could have been testing their solutions on full files from actual code repositories. Below is the distribution of how many lines were in the most of test files. Most files contained 3–8 lines with few exceptions.

![Number of lines in each class in the test set.](https://cdn-images-1.medium.com/max/1200/1*G-cisRqLj56WKYsdSo-yAA.png)

Number of lines in each class in the test set.

#### Test set

Our guess was that round-2 test files will be similar to the ones from r-1. Hence, in order to select the best model we manually labelled code files into the given 29 classes. This presented a challenging task to correctly identify a language among 100+ programming languages that exist out there, even for a seasoned software professional.

With the help of LLMs we were able to build a test set that consisted of 493 code files with 7.4k+ lines of code. We have also decided to add “other” text files to match the target distribution, however we have kept other files only at 50% of the total test set to keep metrics balanced. Some popular languages (like python and javascript) were over-represented, whereas rare languages (func, dart or tl) were hardly present:

![Test set class distribution](https://cdn-images-1.medium.com/max/1200/1*JI9ewaYK65AbilGGrhtxRw.png)

Test set class distribution

#### Train set

For the training set, we followed a two-pronged approach to ensure both breadth and diversity of the data. The backbone of the training data was the [thestack dataset](https://huggingface.co/datasets/bigcode/the-stack/viewer/default/train), which is known for its vast array of programming language examples. This dataset laid a formidable foundation for the training data, offering a variety of examples across a multitude of programming languages.

To increase diversity and number of samples for under-represented classes, we have supplemented the thestack data with manually collected files from GitHub. We particularly tried to collect files from different repositories so that files will have a diverse set of code styles and dependent packages.

This combination of thestack dataset and manually collected GitHub files has resulted in a decent train set with 37k+ source files with over 220k+ lines of code, giving the ML model a wide range of data to learn from and thereby, enhancing its ability to generalize.

In order to match the size of text in the test set, we’ve chunked the train files to randomly select 10–25 lines for each chunk, thus increasing the total number of train samples. We’ve also increased the train set with “other” text files by 20% in order to be able to identify non-code text snippets effectively. The resulting train class distribution showed a balanced distribution except for a few less popular languages:

![Train set class distribution](https://cdn-images-1.medium.com/max/1200/1*BjPg6ezqQWUL6ilNbHNKzQ.png)

Train set class distribution

#### Challenges

There were a number of challenges associated with determining the ground truth labels. I’ll provide few examples to get a better understanding:

* **Too short to identify:**

![a very short test set sample](https://cdn-images-1.medium.com/max/1200/1*dfc70l77hS2OTC7IJapwdw.jpeg)

a very short test set sample

* **No clear association rule.** For example commands like `pip install <package>` or `docker run <image> <command>` can be classified as either *python/docker* or *shell*.
* **Mix of languages.** Certain languages such as *HTML* or *SQL* often appear inside other languages and might represent a large chunk of the entire file.
* **No keywords.** Markup languages like *JSON/YAML* do not have any syntax keywords and should be solely identified by non-word characters.

### Model development

Because of the tight speed limitations (50ms/4096 chars) we’ve decided to build our solution based on simple linear models and text pre-processing techniques. Model development has been implemented in *Python* and then ported to *C++* as required by the contest rules*.*

#### Text preprocessing

After many iterations on the validation and test sets, we’ve ended up in simple tokenization technique. We start by removing code comments and docstrings and then extract tokens as words or characters. We then filter out tokens which contain only numbers. We also avoid lowercasing as it matters in most of the languages. An example tokenization on short snippets looks like this:

```
================== TGLANG_LANGUAGE_PYTHON =================  
  
 Calculates mode for GeoSeries  
 :param ind: identifier  
 :param gs: GeoSeries  
 :return: identifier and a mode for GeoSeries  
 """  
 aggregated = []  
 for g in gs:  
  if g[1].empty:  
   aggregated.append(None)  
  else:  
   selected = g[1].mode()  
   selected = selected.set_index(g[1].index)  
   aggregated.append(selected)  
 return ind, pd.concat(aggregated)  
def rowwise_average(gs, row_count=None):  
 """  
 Calculates an average for each row in each group - rowwise.  
  
TOKENS:  
Counter({':': 6, 'for': 3, 'GeoSeries': 3, 'Calculates': 2, 'mode': 2, 'param': 2, 'identifier': 2, 'each': 2, 'ind': 1, 'gs': 1, 'return': 1, 'and': 1, 'a': 1, 'an': 1, 'average': 1, 'row': 1, 'in': 1, 'group': 1, '-': 1, 'rowwise': 1, '.': 1})  
  
================== TGLANG_LANGUAGE_RUBY =================  
  
      {  
        :'bar' => :'bar'  
      }  
    end  
    # Returns all the JSON keys this model knows about  
    def self.acceptable_attributes  
      attribute_map.values  
    end  
    # Attribute type mapping.  
    def self.openapi_types  
  
TOKENS:  
Counter({'.': 3, ":'": 2, 'bar': 2, "'": 2, 'end': 2, 'def': 2, 'self': 2, '{': 1, '=>': 1, '}': 1, 'acceptable_attributes': 1, 'attribute_map': 1, 'values': 1, 'openapi_types': 1})
```

#### Text embedding

We then fit a [Tf-Idf vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) on the train set with the following parameters:

```
vect_params = dict(  
    max_df=0.25,  
    min_df=3,  
    max_features=1000,  
    binary=True,   
    ngram_range=(1,1),   
    stop_words=None,  
    tokenizer=tokenize_text,  
    lowercase=False,  
)
```

It uses our custom tokenization function from the previous step. Tf-Idf is a proven method that works well as a baseline solution and often beats the more trivial bag-of-words technique. With a bit of experimentation we’ve arrived at 1000 features as a good balance of speed and accuracy and binary vocabulary counts which meant that the actual presence of a specific keyword was more significant than the number of occurrences. Increasing number of features, didn’t always yield better results, although it gave a slight boost when we disable lowercasing.

#### Classifier

For final classification, we’ve found out that a simple [multinomial naive Bayes](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html#sklearn.naive_bayes.MultinomialNB) (MNB) gave the highest score among other linear classifiers. It’s a very robust model for text classification tasks that performs well in conjunction with tf-idf or other word counting methods. In a nutshell, it tried to figure out class priors for each term in the tf-idf vocabulary and smooth it out with a total number of features in each class. It has a decent accuracy and amazing speed.

In most of our experiments, MNB has beaten Complement NB, Logistic regression, SVM and other tree-based classifiers. In the final experiment, we were able to achieve a classification score of **0.82** both in the validation and test sets. The final model selection looked like the table below:

```
|    | input_fields   | preprocessing   | vect   | est   |   val_score |   test_score |    score |  
|---:|:---------------|:----------------|:-------|:------|------------:|-------------:|---------:|  
|  1 | ['content']    | raw             | tfidf  | mnb   |    0.81337  |     0.82132  | 0.81867  |  
|  3 | ['content']    | raw             | bow    | mnb   |    0.825348 |     0.795939 | 0.805742 |  
|  0 | ['content']    | raw             | tfidf  | cnb   |    0.716435 |     0.676142 | 0.689573 |  
|  2 | ['content']    | raw             | bow    | cnb   |    0.698329 |     0.658883 | 0.672032
```

Final confusion matrix looked the one below. It’s obvious that over-represented languages (Python and Javascript) have the most amount of errors, although a bunch of them due to the challenges described in the data section. Besides ambiguous code snippets, languages, similar in syntax, such as C and C++ cause cross-errors. “Other” files also somewhat frequently get classified as a programming language and vice versa.

![Confusion matrix on the test set](https://cdn-images-1.medium.com/max/1200/1*XOq3F6XKoRDg62i9ofjhCw.png)

Confusion matrix on the test set

### Submission

Finally, after building a dataset and selecting the best model, it was time to prepare a submission. As stated before, it had to be a fast C++ library without any network connection (no localhost as well), but it was allowed to load a model from a file (with a total file limit of 2GB).

#### C++ port

The idea consisted in exporting model weights and implementing all the required operations in cpp. Luckily, the inference parts of both Tf-Idf and MNB consist of simple linear matrix multiplications and additions. Once exported the weights are integrated to the lib for fast loading and processing. This solution yielded us less 10ms per one file.

#### Ship fast and iterate

During hackathons, it’s quite important to build an efficient workflow from a feature to submission as soon as possible. Once a baseline model is ready for a submission, we can iterate as many times as needed to improve metrics. Once the cpp code was ready, we have implemented single-command compilation and final testing using clean docker image.

#### Final cpp evaluation

In the end, there were few implementation differences between *Python* and *C++:* running `libtglang.so` on practically the same test set results in a accuracy drop down to 66%. However, we’ve preferred this drop coupled with its blazing speed to our another solution which was running at 600ms per file.

#### Things that worked, but not integrated

Some features yielded good results but were not integrated in the final solution either due to processing or insufficient time.

* [Sentencepiece tokenizer](https://pytorch.org/text/stable/data_functional.html#sentencepiece-tokenizer) trained on our data — unable to load from the *libtorch*;
* [ONMT tokenizer](https://github.com/OpenNMT/Tokenizer) which has both Python and C++ bindings performed well but was in the slow solution;
* Vocabulary lookup — our custom vocabulary lookup during tokenization worked well with the onmt tokenizer.

#### Things that did not work

Some features were promising but needed more time for fine-tuning or experimentation:

* [MobileBert](https://huggingface.co/docs/transformers/model_doc/mobilebert) could have been fast and accurate but it didn’t reach good validation scores on our dataset;
* [Libtorch](https://pytorch.org/tutorials/advanced/cpp_export.html#loading-a-torchscript-model-in-c) seemed like a good option to export models to C++, however it was quite slow for simple linear models;
* Removing character-only tokens from the tf-idf vocabulary usually resulted in the decrease of scores.

### Team

In any competition, a team is an essential factor of success. Certain people are able to handle it all, but in reality where everyone has a day job and a family, it’s quite important to have a team and establish a smooth workflow where roles are clearly defined.

In our case, we had three people working jointly on a single solution:

1. One person has worked on building a stable and diverse dataset.
2. Another teammate has been responsible with model development and preparing a submission.
3. A third developer (C++ expert) has taken care of the cpp inference.

Check out our hugging face demo or github repo for more details:

[Tglang\_programming\_langugage\_detection - a Hugging Face Space by rusteamDiscover amazing ML apps made by the communityhuggingface.co](https://huggingface.co/spaces/rusteam/Tglang_programming_langugage_detection)

[GitHub - Rusteam/tglang: C++ library to detect programming languages for telegram contestC++ library to detect programming languages for telegram contest - GitHub - Rusteam/tglang: C++ library to detect…github.com](https://github.com/Rusteam/tglang)

### Conclusion

Each competition we learn something new and do our best to have a good solution. This competition proves again the old startup formula to ship quickly and then add increments. At the same time, it’s quite important to have a good team workflow with clearly split roles and work together for final results.

Another interesting takeaway is that, even in the era of LLMs, simple models prove to be useful and have practical applications. Text pre-processing still matters a lot which requires experimentation and iteration.

*Let me know what you think about our solution in the comments.*
