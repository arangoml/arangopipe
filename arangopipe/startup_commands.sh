#!/bin/bash
arangod --database.password="open sesame"&
jupyter notebook --allow-root --notebookdir=/workspace/experiments  --ip=0.0.0.0 --port=8888 --no-browser&
sleep 5
export PYTHONPATH=$PYTHONPATH:/workspace/experiments/examples/test_data_generator
python -c "from generate_model_data import generate_runs; generate_runs()"
npm start
