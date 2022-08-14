"""
Create the edges and nodes for the graph

Gedcom tags:
https://www.tamurajones.net/GEDCOMTags.xhtml
"""

import dataclasses
from datetime import datetime
from enum import Enum
from typing import Optional, Tuple
import unidecode
from dateutil.parser import parse, ParserError

from python_gedcom_2.element.family import FamilyElement
from python_gedcom_2.element.individual import IndividualElement
from python_gedcom_2.parser import Parser

import logging
logger = logging.getLogger()



@dataclasses.dataclass
class Person:
    id: str
    name: str
    birth_date: Optional[str]
    birth_place: Optional[str]
    death_date: Optional[str]
    death_place: Optional[str]
    gender: Optional[str]

    def __str__(self):
        return f"{self.name} {self.id}"


@dataclasses.dataclass
class Edge:
    """
    An edge in the graph
    """
    source: str
    target: str
    type: str

    def __str__(self):
        return f"{self.source} {self.target} {self.type}"


class EdgeType(Enum):
    """
    Edge types
    """
    CHILDREN = "children"
    SPOUSE = "spouse"


def get_children(element, gedcom_parser):
    individuals = []
    child_elements = gedcom_parser.get_children(element)

    for child in child_elements:
        if isinstance(child, IndividualElement):
            individuals.append(child)
    return individuals



def parse_date(date_string: str)->datetime:
    """
    Parse a date string in Spanish and return a datetime
    :param date_string:
    :return:
    """
    if date_string == "":
        return None
    try:
        return parse(date_string)
    except Exception as ex:
        logger.warning(f"Could not parse date {date_string}")
        return None

def parse_individual(individual_element: IndividualElement)->Person:
    """
    Parse an individual element and return a dictionary with the following keys:
    :param individual_element:
    :return:
    """
    name = individual_element.get_name()
    gender = individual_element.get_gender()
    bdate, bplace, bsources = individual_element.get_birth_data()
    ddate, dplace, dsources = individual_element.get_death_data()

    bdate = parse_date(bdate)
    ddate = parse_date(ddate)

    element_parsed = {"name": unidecode.unidecode(" ".join(name).lower()),
                      "id": individual_element.get_pointer(),
                      "birth_date": bdate,
                      "birth_place": bplace,
                      "death_date": ddate,
                      "death_place": dplace,
                      "gender": gender
                    }

    person = Person(**element_parsed)
    return person


def get_edges_nodes(gen_file_path: str) -> Tuple[list[Person],list[Edge]]:
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
            if element.get_tag() in ['SUBM']: # Skip submitter
                continue
            nodes.append(parse_individual(element))
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
                elif ce.get_tag() in ["RIN","_UID"]: # Resource Identifier/UUID
                    continue
                else:
                    logger.info(f"Unknown tag for children {ce.get_tag()}")
            if husband_element:
                # Children point to parent
                for children in children_individuals:
                    edges.append(Edge(source=husband_element.get_value(),
                                      target=children.get_value(),
                                      type=EdgeType.CHILDREN))
            if wife_element:
                for children in children_individuals:
                    edges.append(Edge(source=wife_element.get_value(),
                                      target=children.get_value(),
                                      type=EdgeType.CHILDREN))
            if husband_element and wife_element:
                edges.append(Edge(source=husband_element.get_value(),
                                  target=wife_element.get_value(),
                                  type=EdgeType.SPOUSE))

            count_family += 1
        else:
            logger.warning(f"Found unknown element type: {type(element)}")
            count_other += 1

    logger.info(f"Individuals: {count_individuals}, Family: {count_family}, Others: {count_other}")
    logger.info(f"Edges: {len(edges)} Nodes: {len(nodes)}")
    return nodes,edges


