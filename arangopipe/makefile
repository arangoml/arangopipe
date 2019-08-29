SRC = arangopipe/*.py
DOCKER_FILE = Dockerfile
DOCKER_PASSWORD = arangopipe
DOCKER_REPO = arangopipe
DOCKER_SI_FILE = Dockerfile_Single_Image
DOCKER_SI_IMG_NAME = apsi
TEST_PYPI_PASSWORD = shriya217

python_arangopipe:$(SRC)
	python3 setup.py sdist bdist_wheel
upload_test_pypi:
	twine upload --repository-url https://test.pypi.org/legacy/  -u rajiv.sambasivan -p $(TEST_PYPI_PASSWORD) dist/*
docker_APSI_build:$(DOCKER_SI_FILE)
	docker build --no-cache -t $(DOCKER_SI_IMG_NAME) -f $(DOCKER_SI_FILE) .
docker_publish_SI_latest:
	@echo 'starting docker SI build...'
	docker login --username arangopipe --password $(DOCKER_PASSWORD)
	@echo 'pushing build...'
	docker tag docker_build_arangopipe $(DOCKER_REPO)/$(DOCKER_SI_IMG_NAME):latest
	docker push $(DOCKER_REPO)/$(DOCKER_SI_IMG_NAME)
	@echo 'done!'
clean:
	rm -rf arangopipe.egg-info build dist
	

