"""
Imports a Gedcom file into the database.
"""
from map import get_edges_nodes
from storage import store_neo4j
import logging
import argparse
logging.basicConfig(
    level=logging.INFO,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import Gedcom file.')
    parser.add_argument('--file', help='Gedcom file to import.')

    args = parser.parse_args()

    # Path to your ".ged" file
    gen_file_path = args.file

    nodes, edges = get_edges_nodes(gen_file_path)
    store_neo4j(nodes, edges)