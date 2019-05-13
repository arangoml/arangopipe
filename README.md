# arangopipe
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/arangoml/arangopipe/master?filepath=README.md)

# Overview of Arangopipe

Arangopipe is a ArangoDB API component for tracing meta-data about machine learning projects. Tracking details of machine learning experiments, like hyper-parameters, or details of optimization techniques, etc., are of explicit concern to data scientists. This need is well served by most machine learning frameworks that are currently around. For example, <a href = https://www.tensorflow.org/guide/summaries_and_tensorboard> Tensorboard </a>, can be useful for this purpose for data scientists using Tensorflow. Analyzing modeling results in the aggregate, rather than focussing on a small set of experiments is equally important to data scientists. For example, data scientists may be interested in:

1. Finding out the range of modeling techniques that have been used for a particular modeling task.
2. Finding out the range of feature engineering techniques that have been used for a particular modeling task.
3. What feature selection or feature extraction methods are useful for a particular modeling task?
4. Did adding a particular attribute to a dataset result in consistent performance gains?
5. How many datasets have been used for a particular modeling task last year?

Machine learning tools and libraries focus of solving machine learning problems and are not explicitly concerned with tracking information to answer questions such as the above. This is the need Arangopipe fulfills. Arangopipe tracks the following data from machine learning experiments:

1. Data for Model Building: Data that goes into the model building activity is tracked. This includes meta-data about the model, the hyper-parameters associated with the model, the featureset used for model building and the dataset used to generate the featureset.
2. Data from Model Building: Data from model building activity is tracked. This includes data about the model parameters (post optimization) and optimization parameters (learning rates, batch-sizes, optimization technique etc.)
3. Data from Model Performance: Data about the model performance is tracked. This includes performance observed in development and deployed model performance.

## Arangopipe Usage Narrative

Arangopipe has two components:

1. **Arangopipe**
2. **ArangopipeAdmin**

**ArangopipeAdmin** is an administrative component. It is meant to provision projects and users into **Arangopipe**. When projects and users have been provisioned in **Arangopipe**, they can start using **Arangopipe** to track data from their machine learning experiments. To begin with, data scientists can *register* entities like datasets, featuresets and model meta-data with **Arangopipe**. Registeration yields an identifier for the entity that they can use to reference the entity in their subsequent interaction with **Arangopipe**. Information provided during registeration includes a component name that they can use to *lookup* the identifier for the entity using the lookup API.
When data scientists have refined their models to a point where they are ready to track it and log its performance during model development, they can do so with a simple API call. If the model is deployment ready, they can indicate this by adding a deployment tag as part of the data provided to the model tracking API.  When models have been deployed, **Arangopipe** administrators provision a *deployment* entitiy in **Arangopipe** to start tracking the serving performance of the deployed model. As serving performance becomes available, it can be recorded against this deployed entity.
 
## Arangopipe Graph Model
The graph representation of entities used in **Arangopipe** and **ArangopipeAdmin** is shown below
![Graph Representation of Arangopipe Entities](arangopipe_schema.png)

### Data Dictionary 
To do:
provide a short concise description of the entities. Point out that the nodes and edges in the model above are modeled as documents. Do we want to at least mention that the there is schema associated with the document structure?

## Arangopipe API Examples
The following section provides examples of using the Arangopipe API

### Creating a Project
```python
# The following lines illustrate how a project can be created.

```

### Registering Datasets, Featuresets and Models


```python
# The following lines illustrate how a dataset, featureset and model can be registered.

```
### Looking up Datasets, Featuresets and Models by Registered Name
```python
# The following lines illustrate how to lookup a dataset, featureset or model by their registered name

```
### Logging Model Performance - Development
```python
# The following lines illustrate how to log model performance

```
### Tagging a Model for Deployment

```python
# The following lines illustrate how to tag a model for deployment

```

### Registering a Deployed Model


```python
# The following lines illustrate how to register a deployed model with Arangopipe

```

### Logging Serving Performance


```python
# The following lines illustrate how to log server performance 

```

## Adhoc Queries with AQL

**Arangopipe** permits us to run ad-hoc queries on the meta-data gathered from ML experiments. Here are some examples.

### Find the dataset used with a deployment tag
```
# Query to get the dataset associated with a deployment tag
```


### What was the performance observed during model performance for a deployed model

```
# Query to get the model performance for a deployed model.
```

###  What were the features used in a particular deployment.
```
# Query to get the features associated with a deployment.
```

## Installation
Installing Arangopipe requires an installation of the following components.
### ArangoDB
To do: Provide two line description of installing Arangodb with docker
### Arangopipe
To do: Complete a conda install of arangopipe, verify it and document it here. Create an environment.yml file for Arangopipe
