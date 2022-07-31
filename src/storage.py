from dateutil.parser import parse
from neo4j import GraphDatabase, Transaction
from neo4j.exceptions import ConstraintError

from map import Person, Edge, EdgeType
import settings

import logging

logger = logging.getLogger()


def clear_db(tx: Transaction):
    """
    Clears the neo4j database.
    :param tx:
    :return:
    """
    tx.run("MATCH (n) DETACH DELETE n")


def create_person(tx: Transaction, person: Person):
    """
    Creates a person in the neo4j database.
    :param tx:
    :param person:
    :return:
    """
    try:

        query_birth_date = ""
        if person.birth_date:
            query_birth_date = "birth_date: date($birth_date),"
        query_death_date = ""
        if person.death_date:
            query_death_date = "death_date: date($death_date),"

        query = f"""CREATE (a:Person {{name: $name, id: $id,  
            birth_place: $birth_place, death_place: $death_place, 
            {query_birth_date}
            {query_death_date}
            gender: $gender}})"""

        tx.run(query,
               name=person.name,
               id=person.id,
               birth_date=person.birth_date,
               birth_place=person.birth_place,
               death_date=person.death_date,
               death_place=person.death_place,
               gender=person.gender)
    except ConstraintError as ex:
        logger.debug(ex)


def create_child_of(tx: Transaction, id_parent, id_child):
    """
    Creates a child relationship between two people.
    :param tx:
    :param id_parent:
    :param id_child:
    :return:
    """
    try:
        tx.run("MATCH (a:Person) WHERE a.id = $id_parent "
               "MATCH (b:Person) WHERE b.id = $id_child "
               "CREATE (b)-[:CHILD]->(a)",
                id_parent=id_parent, id_child=id_child)
    except ConstraintError as ex:
        logger.debug(ex)


def create_spouse_of(tx: Transaction, id_parent_source, id_parent_target):
    """
    Creates a spouse relationship between two people.
    :param tx:
    :param id_parent_source:
    :param id_parent_target:
    :return:
    """
    try:
        tx.run("MATCH (a:Person) WHERE a.id = $id_parent_source "
           "MATCH (b:Person) WHERE b.id = $id_parent_target "
           "CREATE (a)-[:SPOUSE]->(b)",
           id_parent_source=id_parent_source, id_parent_target=id_parent_target)
    except ConstraintError as ex:
        logger.debug(ex)


def store_neo4j(nodes: list[Person], edges: list[Edge]):
    """
    Stores the nodes and edges in the neo4j database.
    :param nodes:
    :param edges:
    :return:
    """
    uri = settings.NEO4J_URI
    driver = GraphDatabase.driver(uri, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

    with driver.session() as session:
        for node in nodes:
            try:
                session.write_transaction(create_person, node)
            except Exception as ex:
                logger.exception(ex)

        for edge in edges:
            try:
                if edge.type == EdgeType.CHILDREN:
                    session.write_transaction(create_child_of, edge.source, edge.target)
                elif edge.type == EdgeType.SPOUSE:
                    session.write_transaction(create_spouse_of, edge.source, edge.target)
            except Exception as ex:
                logger.exception(ex)
    driver.close()