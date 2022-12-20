from arangopipe.arangopipe_storage.arangopipe_api import ArangoPipe
from arango import ArangoClient

# Initialize the client for ArangoDB.
client = ArangoClient(hosts="http://localhost:8529")
# Connect to "test" database as root user.
test_db = client.db("arangopipe_test", username="root", password="qwerty")

#Create ArangoPipe passing the test_db for database ops
ap = ArangoPipe(db = test_db, graph_name = "enterprise_ml_graph")