"""
Imports a Gedcom file into the database.
"""
from map import get_edges_nodes
from storage import store_neo4j
import logging

logging.basicConfig(
    level=logging.INFO,
)

if __name__ == "__main__":
    nodes, edges = get_edges_nodes()
    store_neo4j(nodes, edges)