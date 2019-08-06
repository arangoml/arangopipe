#!/bin/bash
arangod --database.password="open sesame"&

jupyter notebook --allow-root --notebookdir=/workspace/experiments  --ip=0.0.0.0 --port=8888 --no-browser
