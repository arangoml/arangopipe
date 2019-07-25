SRC = arangopipe/*.py
DOCKER_FILE = Dockerfile
DOCKER_IMAGE_TAG = docker_build_arangopipe
DOCKER_PASSWORD = arangopipe

python_arangopipe:$(SRC)
	python3 setup.py sdist bdist_wheel
docker_build:$(DOCKER_FILE)
	docker-compose build
docker_publish_latest:
	docker login --username arangopipe --password $(DOCKER_PASSWORD)
	@echo 'pushing build...'
	docker tag docker_build_arangopipe arangopipe/docker_build_arangopipe:latest
	docker push arangopipe/docker_build_arangopipe:latest
	@echo 'done!'
clean:
	rm -rf arangopipe.egg-info build dist
