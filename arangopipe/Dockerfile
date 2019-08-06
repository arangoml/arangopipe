FROM tensorflow/tensorflow:latest-py3 
MAINTAINER Joerg Schad <info@arangodb.com>
ENV GIT_PYTHON_REFRESH=quiet
RUN apt-get install -y python-pip
#RUN pip install --upgrade pip
RUN pip install conda mlflow hyperopt sklearn2 jsonpickle python-arango==4.4.0
RUN pip install -i https://test.pypi.org/simple/ arangopipe
RUN mkdir -p /workspace
RUN pip install jupyter
RUN pip install matplotlib
RUN pip install tensorflow-data-validation
RUN pip install PyYAML==5.1.1 
#RUN git clone git@github.com:arangoml/arangopipe.git /workspace
WORKDIR /workspace/experiments
COPY tests/ examples/
COPY getting_started.ipynb .
RUN export PYTHONPATH=$PYTHONPATH:`pwd`
RUN jupyter notebook --generate-config --allow-root
RUN echo "c.NotebookApp.password = u'sha1:6a3f528eec40:6e896b6e4828f525a6e20e5411cd1c8075d68619'" >> /root/.jupyter/jupyter_notebook_config.py
EXPOSE 8888 8529
CMD ["jupyter", "notebook", "--allow-root", "--notebook-dir=/workspace/experiments", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
