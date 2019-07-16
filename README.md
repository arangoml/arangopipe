# ArangoML Pipeline

ArangoML Pipeline is a common and extensible Metadata Layer for Machine Learning Pipelines which allows Data Scientists and [DataOps](https://en.wikipedia.org/wiki/DataOps) to manage all information related to their ML pipeline in one place.

## Introduction
When productizing Machine Learning Pipelines (e.g., [TensorFlow Extended](https://www.tensorflow.org/tfx/guide) or [Kubeflow](https://www.kubeflow.org/))
the capture (and access to) of metadata across the pipeline is a vital. Typically, each of the  components of such ML pipeline produces/requires Metadata, for example:
* Datastorage: size, location, creation date, checksum, ...
* Feature Store (processed dataset): transformation, version, basedatasetm ...
* Model Training: training/validation performance, training duration, ...
* Model Serving: model linage, serving performance, ...

Instead of each component storing its own metadata, a common Metadata Layer allows for queries across the entire pipeline and more efficient management.
[**ArangoDB**](https://www.arangodb.com) being a multi model database supporting both efficient document and graph data models within a single database engine is a great fit for such kind of common metadata layer for the following reasons:
* The metadata produced by each component is typically unstructured (e.g., TensorFlow's training metadata is different from PyTorch's metadata) and hence a great fit for a document databases
* The relationship between the different entities (i.e., metadata) can be neatly expressed as graphs (e.g., this model has been trained by *run_34* on *dataset_y*)
* Querying the metadata can be easily expressed as a graph traversal (e.g., all models which have been derived from *dataset_y*)

## Use Cases
ArangoML Pipeline benefits many different scenarios including:
* Capture of Linage Information (e.g., Which dataset influences which Model)
* Capture of Audit Information (e.g, A given model was training two month ago with the following training/validation performance)
* Reproducibility of Model Training
* Model Serving Policy (e.g., Which model should be deployed in production based on training statistics)
* Extension of existing ML pipelines through simple python/HTTP API


## Overview
Arangopipe is a ArangoDB API component for tracing meta-data about machine learning projects. Tracking details of machine learning experiments, like hyper-parameters, or details of optimization techniques, etc., are of explicit concern to data scientists. This need is well served by most machine learning frameworks that are currently around. For example,  [**Tensorboard**](https://www.tensorflow.org/guide/summaries_and_tensorboard), can be useful for this purpose for data scientists using Tensorflow. Analyzing modeling results in the aggregate, rather than focussing on a small set of experiments is equally important to data scientists. For example, data scientists may be interested in:

1.  Finding out the range of modeling techniques that have been used for a particular modeling task.
2.  Finding out the range of feature engineering techniques that have been used for a particular modeling task.
3.  What feature selection or feature extraction methods are useful for a particular modeling task?
4.  Did adding a particular attribute to a dataset result in consistent performance gains?
5.  How many datasets have been used for a particular modeling task last year?

Machine learning tools and libraries focus of solving machine learning problems and are not explicitly concerned with tracking information to answer questions such as the above. This is the need  **Arangopipe**  fulfills.  **Arangopipe**  tracks the following data from machine learning experiments:

1.  Data for Model Building: Data that goes into the model building activity is tracked. This includes meta-data about the model, the hyper-parameters associated with the model, the featureset used for model building and the dataset used to generate the featureset.
2.  Data from Model Building: Data from model building activity is tracked. This includes data about the model parameters (post optimization) and optimization parameters (learning rates, batch-sizes, optimization technique etc.)
3.  Data from Model Performance: Data about the model performance is tracked. This includes performance observed in development and deployed model performance.

##  Usage
Arangopipe has two components:
1. **Arangopipe**
2. **ArangopipeAdmin**

**ArangopipeAdmin** is an administrative component. It is meant to provision projects and users into **Arangopipe**. When projects and users have been provisioned in **Arangopipe**, they can start using **Arangopipe** to track data from their machine learning experiments. To begin with, data scientists can *register* entities like datasets, featuresets and model meta-data with **Arangopipe**. Registeration yields an identifier for the entity that they can use to reference the entity in their subsequent interaction with **Arangopipe**. Information provided during registeration includes a component name that they can use to *lookup* the identifier for the entity using the lookup API.
When data scientists have refined their models to a point where they are ready to track it and log its performance during model development, they can do so with a simple API call. If the model is deployment ready, they can indicate this by adding a deployment tag as part of the data provided to the model tracking API.  When models have been deployed, **Arangopipe** administrators provision a *deployment* entitiy in **Arangopipe** to start tracking the serving performance of the deployed model. As serving performance becomes available, it can be recorded against this deployed entity.

## Arangopipe Graph Model
![Graph representation of ArangoPipe entities](arangopipe_schema.png)

### Data Dictionary

Arangopipe represents metadata as a graph. The nodes of the graph above are the principal elements about which metadata is gathered. These elements are high level abstractions that are encountered in any machine learning pipeline. A brief description of each of these elements is provided. Elements of the data model are either nodes or edges.

1. Dataset: This node captures metadata about datasets. Examples of attributes could be the storage location (URL), source system, creation date, summary statistics etc. .
2. Featureset: This node captures metadata about the features in the dataset. A featureset is obtained by applying a transformation to a dataset.
3. (Edge) Featureset - Dataset: Captures the dataset the associated featureset was generated from. Details of the transformation, for example the jupyter notebook that performs the transformation could be captured as part of the edge data.
4. Run: Captures metadata about the execution of a pipeline, for example the start time and the end time, status of execution (errors encountered) etc. .
5. Project: Captures metadata about the project associated with a pipeline. This is created with **ArangopipeAdmin**
6. Model: Captures metadata about the model. JSON serialized representations of model metadata can be stored if desiered. For example, if the model is used for hyperparameter optimization. The hyperparameter space can be stored in JSON serialized format.
7. DevPerf: Captures metadata about the performance metrics gathered during execution of the pipeline. The metric captured depends on the purpose of the model. It could be the root mean square error (RMSE) for a regression model or the best performing model and associated hyperparameters for a hyperparameter optimization model.
8. Deployment: Captures metadata about a particular production deployment. This could include details like the scheduled date, current status (scheduled, active, archived )etc.
9. ServingPerf: Captures the serving performance for a particular period. This is associated with a deployment and could include a collection of metrics, for example model performance metrics, average response time etc. .
10. (Edge) Deployment - Model: Captures the model associated with a deployment
11. (Edge) Deployment - SevPerf: Captures the serving performance associated with a deployment.
12. (Edge) Run - Model: Captures the model associated with a pipeline execution
13. (Edge) Run - DevPerf: Captures the model performance observed in development
14. (Edge) Run - Dataset: Captures the dataset associated with a pipeline execution
15. (Edge) Run - Featureset: Captures the featureset associated with a pipeline execution.
16. Model Params: This captures the hyperparameters and the parameters associated with model development.
17. (Edge) Run - Model Params: This captures the model parameters obtained with a pipeline execution.
18. (Edge) Deployment - Featureset: This captures the featureset associated with a deployment.
19. (Edge) Deployment - ModelParams: This captures the model parameters used with a deployment.
20. (Edge) Project - Models: This captures the models associated with a project.

The data associated with the nodes and edges of the graph are stored as documents. The documents do not have a fixed structure and represent data using key-value pairs. This offers flexibility and permits users to decide the metadata elements that they would like to store. This also permits users to store metadata from any machine learning tech stack in Arangopipe.

## Installing Arangopipe

This repository contains **Arangopipe** and examples to illustrate how it can be used with machine learning tools like **hyperopt** and **MLFlow**. To install **Arangopipe**, do the following:

1.  Install ArangoDB

    `docker run -p 8529:8529 -e ARANGO_ROOT_PASSWORD=openSesame arangodb`

2.  Install pre-requisites

    `pip install -r requirements.txt`

4.  Install Arangopipe

    `pip install -i https://test.pypi.org/simple/ arangopipe`

The _tests_ durectory contains examples that illustrate how **Arangopipe** can be used with other machine learning libraries. For example, the _mlflow_ directory provides examples of how **Arangopipe** can be used with [mlflow](https://www.mlflow.org/docs/latest/index.html). To run these examples, you will need to install _mlflow_ first. Similarly, to see how **Arangopipe** can be used to with hyper-parameter optimization experiments, look at the examples in the _hyperopt_ directory. To run these examples, you will need to have [_hyperopt_](https://pypi.org/project/hyperopt/) installed.
