SRC = arangopipe/*.py
DOCKER_FILE = Dockerfile
DOCKER_PASSWORD = <the_password>
DOCKER_REPO = arangopipe
DOCKER_SI_FILE = Dockerfile_Prod
DOCKER_SI_IMG_NAME = apms_prod
TEST_PYPI_PASSWORD = arangopipe

python_arangopipe:$(SRC)
	find ./arangopipe -name '*.py' -print0 | xargs -0 yapf -i
	find ./arangopipe/arangopipe_storage -name '*.py' -print0 | xargs -0 yapf -i
	find ./arangopipe/arangopipe_analytics -name '*.py' -print0 | xargs -0 yapf -i
	find ./tests/mlflow -name '*.py' -print0 | xargs -0 yapf -i
	find ./tests/pytorch -name '*.py' -print0 | xargs -0 yapf -i
	find ./tests/test_data_generator -name '*.py' -print0 | xargs -0 yapf -i
	python3 setup.py sdist bdist_wheel
upload_test_pypi:
	twine upload --repository-url https://test.pypi.org/legacy/  -u rajiv.sambasivan -p $(TEST_PYPI_PASSWORD) dist/*
docker_APSI_build:$(DOCKER_SI_FILE)
	docker build  --no-cache -t $(DOCKER_SI_IMG_NAME) -f $(DOCKER_SI_FILE) .
docker_publish_SI_latest:
	@echo 'starting docker SI build...'
	docker login --username arangopipe --password $(DOCKER_PASSWORD)
	@echo 'pushing build...'
	docker tag docker_build_arangopipe $(DOCKER_REPO)/$(DOCKER_SI_IMG_NAME):latest
	docker push $(DOCKER_REPO)/$(DOCKER_SI_IMG_NAME)
	@echo 'done!'
clean:
	rm -rf arangopipe.egg-info build dist

rebuild_all: clean python_arangopipe upload_test_pypi docker_APSI_build docker_publish_SI_latest   
	

