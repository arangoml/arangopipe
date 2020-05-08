# ArangoML Pipeline

<center>
<img src="assets/logos/ArangoML_Logo.png" width=95% >
</center>

ArangoML Pipeline is a common and extensible Metadata Layer for Machine Learning Pipelines which allows Data Scientists and [DataOps](https://en.wikipedia.org/wiki/DataOps) to manage all information related to their ML pipeline in one place.

<center>
<img src="assets/logos/ArangoML_Pipleline_Overview.jpg" width=95% >
</center>

**News:**
[ArangoML Pipeline Cloud](https://www.arangodb.com/2020/01/arangoml-pipeline-cloud-manage-machine-learning-metadata/) is offering a no-setup, free-to-try managed service for ArangpML Pipeline. A [ArangoML Pipeline Cloud  tutorial](https://colab.research.google.com/github/arangoml/arangopipe/blob/master/examples/Arangopipe_with_TensorFlow_Beginner_Guide.ipynb#) is also available without any installation or signup.

## Quick Start
To get started without any installations (using ArangoML Pipeline Cloud)
, click :
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arangoml/arangopipe/blob/master/examples/Arangopipe_Feature_Examples.ipynb)

The [examples folder](https://github.com/arangoml/arangopipe/tree/master/examples) contains notebooks that illustrate the features of **Arangopipe**.

## Overview
When machine learning pipelines are created, for example using [TensorFlow Extended](https://www.tensorflow.org/tfx/guide) or [Kubeflow](https://www.kubeflow.org/), 
the capture (and access to) of metadata across the pipeline is vital. Typically, each component of such an ML pipeline produces or requires metadata, for example:

* Data storage: size, location, creation date, checksum, ...
* Feature Store (processed dataset): transformation, version, base datasets ...
* Model Training: training/validation performance, training duration, ...
* Model Serving: model linage, serving performance, ...

Instead of each component storing its metadata, a common metadata layer simplifies data management and permits querying the entire pipeline.
[**ArangoDB**](https://www.arangodb.com), being a multi model database, supporting both efficient document and graph data models within a single database engine, is a great fit for such a metadata layer, for the following reasons:

* The metadata produced by each component is typically unstructured (e.g., TensorFlow's training metadata is different from PyTorch's metadata) and hence a great fit for document databases
* The relationship between the different entities (i.e., metadata) can be neatly expressed as graphs (e.g., this model has been trained by *run_34* on *dataset_y*)
* Metadata queries are easily expressed as graph traversals (e.g., all models which have been derived from *dataset_y*)

## Use Cases
ArangoML Pipeline can benefit many scenarios, such as:

* Capture of lineage information (e.g., Which dataset influences which model?)
* Capture of audit information (e.g, A given model was training two months ago with the following training/validation performance)
* Reproducible model training
* Model serving policy (e.g., Which model should be deployed in production based on training statistics)
* Extension of existing ML pipelines through simple python/HTTP API

## Documentation
Please refer to the [**Arangopipe** documentation](documentation/README.md) for further information.
