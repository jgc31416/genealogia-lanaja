from typing import List, Dict

from dash import dash
from python_gedcom_2.element.family import FamilyElement
from python_gedcom_2.element.individual import IndividualElement
from python_gedcom_2.parser import Parser
from dash import html
from dash import dcc
import visdcc
from dash.dependencies import Input, Output, State


# Path to your ".ged" file
gen_file_path = '../data/Lanaja_2021_sp_v2.ged'
prints_file_path = '../data/impresiones.csv'


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
            nodes.append((id, element.get_name()))
            edges.extend([((id, element.get_name()), (children.get_pointer(), children.get_name())) for children in
                          get_children(element, gedcom_parser)])
            count_individuals += 1
        elif type(element) == FamilyElement:
            husband_element = None
            wife_element = None
            children_elements = element.get_child_elements()
            for ce in children_elements:
                if ce.get_tag() == "HUSB":
                    husband_element = ce
                elif ce.get_tag() == "WIFE":
                    wife_element = ce
            if husband_element and wife_element:
                record = ((husband_element.get_value(), ""), (wife_element.get_value(), ""))
                edges.append(record)
            count_family += 1
        else:
            count_other += 1

    print(f"I {count_individuals}, F {count_family}, O {count_other}")
    print(f"Edges: {len(edges)} Nodes: {len(nodes)}")
    return nodes,list(set(edges))


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


if __name__ == "__main__":
    nodes, edges = get_edges_nodes()
    app = initialize_app(nodes, edges)

    app.run_server(debug=True)