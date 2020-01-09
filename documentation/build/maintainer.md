# Build Instrcutions

## Building Arangopipe

It is recommended that you create a build directory for the purpose of building **Arangopipe**. Creating a python environment for **Arangopipe** is also recommended. Having a separate environment for **Arangopipe**  provides the benefit of isolating **Arangopipe** dependencies from other python applications you may be developing or working with.

**Note**: The **Arangopipe** build requires `make`. The build procedure below has been verified on `Linux` environments. 

(1) conda create -n apbuild python=3.7

(2) conda activate apbuild

(3) pip install -r requirements.txt

(4) run git init .

(5) run git pull git@github.com:arangoml/arangopipe.git

(6) change directory to arangopipe

(7) run make clean

(8) run make python_arangopipe

## Building the Docker Images
**Arangopipe** provides the following docker images:

1. A Tensorflow docker image
2. A Pytorch docker image
3. A thin production docker image  with no  development tools. The production image contains only **Arangopipe** and dependencies. An ipython shell is also provided.

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



