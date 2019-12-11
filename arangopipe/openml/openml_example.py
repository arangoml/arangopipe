import openml
import os
OPENML_CACHE_DIR = "/home/admin2/arangopipe/openml/cache"
openml.config.cache_directory = os.path.expanduser(OPENML_CACHE_DIR)

def get_task(id = 403):
    task = openml.tasks.get_task(403)
    return task
