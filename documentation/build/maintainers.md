# Build Instructions
The following instructions show you how to build the different supported packages.
These instructions include build instructions for:
 * Building the Arangopipe package
 * Building Arangopipe Docker images with TensorFlow & PyTorch
 * Building a production ready Docker image
 * Building a frontend-only Docker image for the ArangoML WebUI

## Building Arangopipe

It is recommended that you create a build directory for the purpose of building **Arangopipe**. Creating a python environment for **Arangopipe** is also recommended. Having a separate environment for **Arangopipe**  provides the benefit of isolating **Arangopipe** dependencies from other python applications you may be developing or working with.

**Note**: The **Arangopipe** build requires `make`. The build procedure below has been verified on `Linux` environments. 

(1) Create new conda environment: `conda create -n apbuild python=3.7`

(2) Activate conda environment: `conda activate apbuild`

(3) Install dependencies: `pip install -r requirements.txt`

(4) run `git clone https://github.com/arangoml/arangopipe.git`

(5) `cd arangopipe`

(6) Build `make clean && make python_arangopipe`

## Building the Docker Images
**Arangopipe** provides the following docker images:

1. A TensorFlow docker image (Dockerfile_TFFE)
2. A Pytorch docker image (Dockerfile_Torch_FE)
3. A thin production docker image  with no  development tools. The production image contains only **Arangopipe** and dependencies. An ipython shell is also provided. (Dockerfile_Prod)
4. A frontend-only Docker image for the ArangoML WebUI.

The docker file populates the **Arangopipe** with test data. This is the data used by the UI. You will need to put in the root password for the database used with the docker container to create the database. You will need to edit the `test_datagen_config.yaml` file in the `test_config` directory for this purpose. In particular, you need to edit the following entries:

  (1) root_user_password : Put in the root user password for the database used
  
  (2) DB_service_host: Put in `localhost` if you want to create the database on the local host. Alternatively, if you are using OASIS, this will be the host name for managed services. For example, `arangoml.arangodb.cloud`.

 (3)conn_protocol: If you are using the container provided database, you may want to use `http`. If you are using SSL, you will have to have the certificate installed as per the requirements of your specific environment.

  (3) dbName: The database name for arangopipe. Defaults to `arangopipe`.

  (4) password: The password you want to use with the **Arangopipe** database. Default value is `open sesame`

  (5) username: The user account name used for the **Arangopipe** database. Default value is `arangopipe`.

You will need to edit the file prior to building the docker image.
  
To build the Docker images, we will have to use the makefile in the **Arangopipe** directory (step 6 in the previous section). **You will need to work from the Arangopipe directory (see step 6 of the previous section) to build the docker images**. The docker images will take some time to build, especially the torch image.



### Building the Tensorflow Docker Image
Edit the the `makefile` to make the following changes:

1. Set `DOCKER_SI_FILE = Dockerfile_TFFE`

2. Set `DOCKER_SI_IMG_NAME = ap_tensor_flow`

3. Run `make docker_APSI_build`


### Building the Torch Docker Image
Edit the the `makefile` to make the following changes:

1. Set `DOCKER_SI_FILE = Dockerfile_Torch_FE`

2. Set `DOCKER_SI_IMG_NAME = ap_torch`

3. Run `make docker_APSI_build`


### Building the Production Docker Image
Edit the the `makefile` to make the following changes:

1. Set `DOCKER_SI_FILE = Dockerfile_Prod`

2. Set `DOCKER_SI_IMG_NAME = apms_prod`

3. Run `make docker_APSI_build`


### Building a frontend-only Docker image for the ArangoML WebUI 
These steps show you how to build the ArangoML React Frontend and update the URL necessary to connect to your ArangoDB instance. 
In order to sign-in to the ArangoML WebUI, a running ArangoDB instance is required. The default port the WebUI looks for is `6529`.

1. Navigate to `arangopipe/arangopipe_frontend/app`

2. Run `npm install` 

3. Run `docker-compose build`

4. Update `REACT_APP_API_ROOT_URL` in the following command to be your desired ArangoDB endpoint:
 `docker run -p 3000:3000 -e REACT_APP_API_ROOT_URL=http://localhost:8529/_db/arangopipe/ arangopipe_frontend_app`

5. To confirm successful configuration, attempt to login at http://localhost:3000



