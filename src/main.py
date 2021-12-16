from typing import List, Dict

from python_gedcom_2.element.individual import IndividualElement
from python_gedcom_2.parser import Parser
import csv

# Path to your ".ged" file
gen_file_path = '../data/Lanaja_2021_sp_v2.ged'
prints_file_path = '../data/impresiones.csv'


def read_prints_file(file_path)->List[Dict]:
    """
    :param file_path:
    :return: Dict {'nombre': 'Manuel ', 'apellidos': 'Abadias Claveria', 'nacimiento': '1793',
                   'etiqueta': '38', 'impresion': 'Impresión de 560m'}
    """
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        return [x for x in reader]


def search_by_full_name(target_person, root_elements):
    for element in root_elements:
        if isinstance(element, IndividualElement):
            if element.given_name_match(target_person['nombre'].strip()) and \
                element.surname_match(target_person['apellidos'].strip()):
                    return element
        #else:
        #    if child_elements := element.get_child_elements():
        #        if found_element:= search_by_full_name(target_person, child_elements):
        #            return found_element


def get_children(element, gedcom_parser):
    individuals = []
    child_elements = gedcom_parser.get_children(element)

    for child in child_elements:
        if isinstance(child, IndividualElement):
            individuals.append(child)
            individuals.extend(get_children(child, gedcom_parser))
    return individuals


if __name__ == "__main__":
    # Get the root individuals
    target_persons = read_prints_file(prints_file_path)

    # Initialize the parser
    gedcom_parser = Parser()
    # Parse your file
    gedcom_parser.parse_file(gen_file_path, False)

    list_child_elements = gedcom_parser.get_element_list()

    # Iterate through all root child elements
    for person in target_persons:
        head_element = search_by_full_name(person, list_child_elements)
        if head_element:
            children = get_children(head_element, gedcom_parser)
            for child in children:
                name, surname = child.get_name()
                print(f"{name},{surname},{person['etiqueta']},{person['impresion']},{child.get_birth_year()}")
        else:
            print(f"Error: We cannot find {person}")

