# ArangoML Pipeline

<center>
<img src="assets/logos/ArangoML_Logo.png" width=95% >
</center>

ArangoML Pipeline is a common and extensible Metadata Layer for Machine Learning Pipelines which allows Data Scientists and [DataOps](https://en.wikipedia.org/wiki/DataOps) to manage all information related to their ML pipeline in one place.

<center>
<img src="assets/logos/ArangoML_Pipleline_Overview.jpg" width=95% >
</center>

**News:**
[ArangoML Pipeline Cloud](https://www.arangodb.com/2020/01/arangoml-pipeline-cloud-manage-machine-learning-metadata/) is offering a no-setup, free-to-try managed service for ArangpML Pipeline. An [ArangoML Pipeline Cloud  tutorial](https://colab.research.google.com/github/arangoml/arangopipe/blob/master/examples/Arangopipe_with_TensorFlow_Beginner_Guide.ipynb#) is also available without any installation or signup.

## **Quick Start**
To skip to Part 2 of this series and get started without any installations (using ArangoML Pipeline Cloud)
, click :
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arangoml/arangopipe/blob/master/examples/Arangopipe_Feature_Examples.ipynb)

The [examples folder](https://github.com/arangoml/arangopipe/tree/master/examples) contains notebooks that illustrate the features of **Arangopipe**.

## **Overview**

This overview is a part of a series of posts introducing ArangoML and showcasing its benefits to your machine learning pipelines. In this first post, we look at what exactly ArangoML is, with later posts in this series showcasing the different tools and use cases. You can follow along with this series by [watching](https://github.com/arangoml/arangopipe/subscription) this repository or by signing up for the [ArangoDB Newsletter](https://www.arangodb.com/blog/).

If you have a use case you would like to see highlighted as a part of this series, please let us know on the [ArangoML Slack channel](https://arangodb-community.slack.com/archives/CN9LVJ24S).

### **ArangoML Tools/Stack**
The ArangoDB  tool stack for analytics allows you to explore relationships of interest in your ArangoDB graph. These include:

1. **AQL**:  The ArangoDB Query Language is a declarative language that aims to be human-readable and supports the complex query patterns that are only possible within a multi-model database. These features make machine learning tasks more powerful and accessible to both the data scientists performing exploratory data analysis and the dev-ops personnel running ad hoc queries for maintenance and issue investigation.  See the [AQL Fundamentals](https://www.arangodb.com/docs/stable/aql/fundamentals.html) for an overview of AQL and some examples of using AQL to query graphs in ArangoDB.

2. **Pregel**: Data engineers use Pregel, a system for large-scale graph processing, to implement computationally intensive data transformations, while data scientists use it for data analysis tasks on large graphs. See our [pregel tutorial](https://www.arangodb.com/pregel-community-detection/) for examples and an overview of using Pregel with ArangoDB. 

3. **ArangoDB-NetworkX Adapter**:  NetworkX is a widely used tool for graph analytics; it provides robust implementations of many algorithms used for graph analytics. If your application requires such algorithms, you can leverage the implementation of these algorithms’ for your ArangoDB graphs. We provide an adapter to convert ArangoDB graphs to NetworkX graphs.  You can leverage ArangoDB’s robust, reliable, and high-performing storage solution with the wide range of algorithms for graph analytics in NetworkX. We will cover our NetworkX implementation in greater detail in our upcoming network analytics post, be sure to [sign up for our newsletter](https://www.arangodb.com/blog/) to be notified on the upcoming posts in this series. If you would like to explore some of the existing notebooks, you can find more examples in [the repository](https://github.com/arangoml/networkx-adapter).

### **Use Cases**
ArangoML Pipeline can benefit many scenarios, such as:

* Capture of lineage information (e.g., Which dataset influences which model?)
* Capture of audit information (e.g, A given model was training two months ago with the following training/validation performance)
* Reproducible model training
* Model serving policy (e.g., Which model should be deployed in production based on training statistics)
* Extension of existing ML pipelines through simple python/HTTP API

### **Learning Through Metadata**
When machine learning pipelines are created, for example using [TensorFlow Extended](https://www.tensorflow.org/tfx/guide) or [Kubeflow](https://www.kubeflow.org/), 
the capture of and access to metadata across the pipeline is vital. Typically, each component of such an ML pipeline produces or requires metadata, for example:

* Data storage: size, location, creation date, checksum, ...
* Feature Store (processed dataset): transformation, version, base datasets ...
* Model Training: training/validation performance, training duration, ...
* Model Serving: model linage, serving performance, ...

In contrast to exploring relationships or entities in a graph, machine learning applications learn autonomously and continuously with new data. A key idea in making this possible is the use of machine learning pipelines. They make it possible for applications to learn from new data. Managing machine learning pipelines is achieved through metadata.

Metadata describes the components and actions involved in building the machine learning pipeline. The steps involved in constructing the pipeline are expressed as a graph by most tools, making ArangoDB a natural fit to store and manage machine learning application metadata. Arangopipe is ArangoDB’s tool for managing machine learning pipelines. Machine learning libraries such as DGL accept NetworkX graphs as input. Therefore the ArangoDB-Networkx adapter can be used to develop machine learning applications with ArangoDB graphs using libraries such as DGL. An example of using this available [here](https://github.com/arangoml/networkx-adapter/blob/master/examples/ITSM_ArangoDB_Adapter.ipynb).

### **Knowledge Graphs**
Thanks to the features that come with using a multi-model database, it is possible to work with Knowledge Graphs(KGs) in ArangoDB; this combines the benefits of still being machine-readable while having the human readability benefits of a property graph. If you would like to learn more about using KGs with ArangoDB take a look at the upcoming Knowledge Graphs in ArangoDB series.

## Documentation
Please refer to the [**Arangopipe** documentation](documentation/README.md) for further information.

**Stay Tuned**

Be sure to [sign up for our newsletter](https://www.arangodb.com/blog/) to be notified of the follow-up posts in this series!

This article is the first in a series covering the many different features of ArangoML. In the upcoming series, we will showcase topics such as:

* Using ArangoML for common network analysis tasks such as discovering structures.
* Using ArangoML to develop graph neural networks on graphs stored in ArangoDB.
* Using ArangoML for common tasks associated with model management.
