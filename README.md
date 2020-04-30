# ArangoML Pipeline

<center>
<img src="assets/logos/ArangoML_Logo.png" width=95% >
</center>

ArangoML Pipeline is a common and extensible Metadata Layer for Machine Learning Pipelines which allows Data Scientists and [DataOps](https://en.wikipedia.org/wiki/DataOps) to manage all information related to their ML pipeline in one place.

<center>
<img src="assets/logos/ArangoML_Pipleline_Overview.jpg" width=95% >
</center>

**News:**
[ArangoML Pipeline Cloud](https://www.arangodb.com/2020/01/arangoml-pipeline-cloud-manage-machine-learning-metadata/) is offering a no-setup, free-to-try managed service for ArangpML Pipeline. A [ArangoML Pipeline Cloud  tutorial](https://colab.research.google.com/github/arangoml/arangopipe/blob/master/examples/Arangopipe_with_TensorFlow_Beginner_Guide.ipynb#) is also available without any installation or Signup.

## Quick Start
To get started with no installations of any sort (using ArangoML Pipeline Cloud)
, click :
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arangoml/arangopipe/blob/master/examples/Arangopipe_Feature_Examples.ipynb)

The [examples folder](https://github.com/arangoml/arangopipe/tree/master/examples) contains examples more example notebooks that illustrate the features of **Arangopipe**.

## Introduction
When productizing Machine Learning Pipelines (e.g., [TensorFlow Extended](https://www.tensorflow.org/tfx/guide) or [Kubeflow](https://www.kubeflow.org/))
the capture (and access to) of metadata across the pipeline is vital. Typically, each of the  components of such ML pipeline produces/requires Metadata, for example:
* Data storage: size, location, creation date, checksum, ...
* Feature Store (processed dataset): transformation, version, base datasets ...
* Model Training: training/validation performance, training duration, ...
* Model Serving: model linage, serving performance, ...

Instead of each component storing its own metadata, a common Metadata Layer allows for queries across the entire pipeline and more efficient management.
[**ArangoDB**](https://www.arangodb.com) being a multi model database supporting both efficient document and graph data models within a single database engine is a great fit for such kind of common metadata layer for the following reasons:
* The metadata produced by each component is typically unstructured (e.g., TensorFlow's training metadata is different from PyTorch's metadata) and hence a great fit for document databases
* The relationship between the different entities (i.e., metadata) can be neatly expressed as graphs (e.g., this model has been trained by *run_34* on *dataset_y*)
* Querying the metadata can be easily expressed as a graph traversal (e.g., all models which have been derived from *dataset_y*)

## Use Cases
ArangoML Pipeline benefits many different scenarios including:
* Capture of Lineage Information (e.g., Which dataset influences which Model?)
* Capture of Audit Information (e.g, A given model was training two months ago with the following training/validation performance)
* Reproducible Model Training
* Model Serving Policy (e.g., Which model should be deployed in production based on training statistics)
* Extension of existing ML pipelines through simple python/HTTP API

## Documentation
Please refer to the [**Arangopipe** documentation](documentation/README.md) for further information.
