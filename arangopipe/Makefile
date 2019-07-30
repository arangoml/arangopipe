SRC = arangopipe/*.py
DOCKER_FILE = Dockerfile
DOCKER_IMAGE = docker_build_arangopipe
DOCKER_PASSWORD = <the password>
DOCKER_REPO = arangopipe

python_arangopipe:$(SRC)
	python3 setup.py sdist bdist_wheel
docker_build:$(DOCKER_FILE)
	docker-compose build
docker_publish_latest:
	@echo 'starting docker build...'
	docker login --username arangopipe --password $(DOCKER_PASSWORD)
	@echo 'pushing build...'
	docker tag docker_build_arangopipe $(DOCKER_REPO)/$(DOCKER_IMAGE):latest
	docker push arangopipe/docker_build_arangopipe:latest
	@echo 'done!'
clean:
	rm -rf arangopipe.egg-info build dist
