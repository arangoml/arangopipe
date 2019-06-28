# Running AQL queries on Arangopipe

Apart, from using the **Arangopipe** search feature, it is also possible to query machine learning meta-data using the query feature in **ArangoDB**. An excerpt of the feature is shown in the figure below.
<figure>
  <img src="AQL_feature.png" alt="my alt text" width=90%/>
  <figcaption style ="text-align:center">Figure 1.</figcaption>
</figure>
The left pane shows an editor area where we can enter queries. We can the execute the query by clicking on the *_Execute_* button in the lower right hand corner. Let us illustrate this with an example. The dataset used for illustration is the wine dataset used to illustrate how **Arangopipe** can be used with *_mlflow_* (see the *_mlflow_* folder). We will illustrate the following operations:

1. Deleting a dataset from the database
2. Deleting a featureset from the database
3. Inserting a dataset into the database
4. Inserting a featureset into the database
5. Linking the featureset and the dataset

If you would like to learn more about AQL, please view the [AQL documentation](https://www.arangodb.com/docs/stable/aql/). The [tutorials](https://www.arangodb.com/docs/stable/tutorials.html) section of the documentation may also be of interest.



## Inserting a dataset into the database

The AQL query to insert a dataset into the database is shown below
```
INSERT {"name" : "wine dataset",
                   "description": "Wine quality ratings","source": "UCI ML Repository" } INTO datasets

```

## Inserting a featureset into the database
The AQL query to insert a featureset into the database is shown below
```
INSERT {"fixed acidity": "float64",
               "volatile acidity": "float64",
               "citric acid": "float64",
               "residual sugar": "float64",
               "chlorides": "float64",
               "free sulfur dioxide": "float64",
               "total sulfur dioxide": "float64",
               "density": "float64",
               "pH": "float64",
               "sulphates": "float64",
               "alcohol": "float64",
               "quality": "int64",
               "name": "wine_no_transformations"} INTO featuresets
```
## Linking a featureset and a dataset

The AQL query to link the featureset and the dataset we just inserted is shown below
```
FOR ds IN datasets
    FILTER ds.name == 'wine dataset'
        FOR fs in featuresets
            FILTER fs.name == 'wine_no_transformations'
            INSERT {"_from": fs._id, "_to": ds._id} INTO featureset_dataset
```

## Graph Traversal with AQL
We can use *_Graph Traversal_* to retrieve the dataset associated with the featureset. The AQL query to do this is shown below
```
FOR f in featuresets
    FILTER f.name == 'wine_no_transformations'
        FOR d IN 1..1 OUTBOUND f featureset_dataset
            RETURN d
```
## Deleting a dataset from the database

To complete the illustration, we now look at how deletes are performed. Deleting assets from **Arangopipe** requires specific privileges. However, AQL provides this feature. A user with sufficient privileges, for example an **Arangopipe** administrator, could perform this action. This example shows how a vertex from the *_dataset_* vertex collection is deleted.
```

FOR d IN datasets

    FILTER d.name == 'wine dataset'
  
    REMOVE d IN datasets
  
```


## Deleting a featureset from the database

A featureset can be deleted from the database in a similar manner. The AQL query to delete a featureset vertex with a particular name is shown below.

```
FOR f in featuresets

    FILTER f.name == 'wine_no_transformations'
    
    REMOVE f IN featuresets

```