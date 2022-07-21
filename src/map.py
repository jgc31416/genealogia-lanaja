from copy import deepcopy

from python_gedcom_2.element.family import FamilyElement
from python_gedcom_2.element.individual import IndividualElement
from python_gedcom_2.parser import Parser
import networkx as nx
from itertools import combinations

# Path to your ".ged" file
gen_file_path = '../data/Lanaja_2021_v4.ged'


def get_children(element, gedcom_parser):
    individuals = []
    child_elements = gedcom_parser.get_children(element)

    for child in child_elements:
        if isinstance(child, IndividualElement):
            individuals.append(child)
    return individuals


def get_edges_nodes():
    # Initialize the parser
    gedcom_parser = Parser()
    # Parse your file
    gedcom_parser.parse_file(gen_file_path, False)

    list_child_elements = gedcom_parser.get_element_dictionary()
    count_individuals = 0
    count_family = 0
    count_other = 0
    nodes = []
    edges = []
    for id, element in list(list_child_elements.items()):
        if type(element) == IndividualElement:
            if element.get_tag() in ['SUBM']:
                continue
            nodes.append((id, {"name": " ".join(element.get_name())}))
            count_individuals += 1
        elif type(element) == FamilyElement:
            husband_element = None
            wife_element = None
            children_elements = element.get_child_elements()
            children_individuals = []
            for ce in children_elements:
                if ce.get_tag() == "HUSB":
                    husband_element = ce
                elif ce.get_tag() == "WIFE":
                    wife_element = ce
                elif ce.get_tag() == "CHIL":
                    children_individuals.append(ce)
                elif ce.get_tag() == "MARR":
                    marriage_element = ce
            if husband_element:
                # Children point to parent
                for children in children_individuals:
                    edges.append((children.get_value(), husband_element.get_value(), {"type":"children"}))
            if wife_element:
                for children in children_individuals:
                    edges.append((children.get_value(), wife_element.get_value(), {"type":"children"}))
            if husband_element and wife_element:
                edges.append((husband_element.get_value(), wife_element.get_value(), {"type":"spouse"}))
            # Brothers edges
            #brother_pairs = combinations(children_individuals, 2)
            #for brother_pair in brother_pairs:
            #    edges.append((brother_pair[0].get_value(), brother_pair[1].get_value(), {"type": "brother"}))
            count_family += 1
        else:
            count_other += 1

    print(f"I {count_individuals}, F {count_family}, O {count_other}")
    print(f"Edges: {len(edges)} Nodes: {len(nodes)}")
    return nodes,edges

# DASH attempt, cannot cope with the network size
"""
from typing import List, Dict
from dash import dash
from dash import html
import visdcc

def initialize_app(nodes, edges):
    app = dash.Dash()
    node_list = [{"id": node[0], "label": node[1], "shape": "dot", "size": 7} for node in nodes]
    edge_list = [{'id': f"{edge[0][0]}--{edge[1][0]}", 'from': edge[0][0], 'to':edge[1][0], 'width':2} for edge in edges]
    app.layout = html.Div(
        [
            visdcc.Network(id='net',
                           data={'nodes': node_list, 'edges': edge_list},
                           options={'height': '800px', 'width':'100%'})
        ]
    )
    return app
"""


def plot_graph(G, labels):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(150,150))
    fig.set_dpi=300
    pos = nx.spring_layout(G, k=1/5, iterations=100)
    # pos = nx.kamada_kawai_layout(G)
    nx.draw_networkx_nodes(G, pos=pos, ax=ax, alpha=0.5)
    nx.draw_networkx_edges(G, pos=pos, ax=ax, width=0.5, alpha=0.3)
    nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=6)
    plt.savefig("lanaja_map.png")


if __name__ == "__main__":
    nodes, edges = get_edges_nodes()
    #for node in nodes[:10]:
    #    print(node)
    #for edge in edges[:1000]:
    #    print(edge)
    node_labels = {}
    for id, label_dict in nodes:
        node_labels[id]=label_dict['name']
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    plot_graph(G, node_labels)


