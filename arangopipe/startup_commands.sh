#!/bin/bash
arangod --database.password="open sesame"&
jupyter notebook --allow-root --notebookdir=/workspace/experiments  --ip=0.0.0.0 --port=8888 --no-browser&
while [[ "$(curl -sL -w "%{http_code}\\n" "http://localhost:8529" -o /dev/null)" != "200" ]]; do
echo "Waiting for arangod"
sleep 5
done
echo "arangod is up!"
export PYTHONPATH=$PYTHONPATH:/workspace/experiments/examples/test_data_generator
python -c "from generate_model_data import generate_runs; generate_runs()"
npm start
