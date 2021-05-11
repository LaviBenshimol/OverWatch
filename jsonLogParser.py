from neo4j import __version__ as neo4j_version, GraphDatabase
from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd
import json
import os
import gzip
from os.path import join, getsize


###############################################################################################
# START of working in neo4j
###############################################################################################
class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


import re

word_regex_pattern = re.compile("[^A-Za-z0-9]+")


def camel(chars):
    words = word_regex_pattern.split(chars)
    return "".join(w.lower() if i is 0 else w.title() for i, w in enumerate(words))


"""    
##################################################
    Taxonomy layer:
                      sample: "evenName": "Invoke"
    Graph data:

        Nodes:
            userIdentity:
            Type: user/resource/service.
            Priviledge learning ?
            Counters?
        Edges:
            Type: Relation(Trusted/Owned) / Event(type).
            Timestamp: convert time to specified format.
            Source IP:
            userAgent:
            status: ? what info to inspect and record?
##################################################
def nodeExist(lbl, node):
    matcher = NodeMatcher(graph)
    m = matcher.match(lbl, screen_name == node.screen_name).first()
    if m is None:
       return False
    else:
       return True
       """


def node_exist(data_base_connection, name):
    check_if_node_exist_query = f"""
        MATCH (j: {name} {{name: "{name}"}})
        RETURN j.name
        """
    res = data_base_connection.query(query=check_if_node_exist_query, db='overwatchDataBase')
    if res is None:
        return False
    else:
        return True


def print_node(data_base_connection, name):
    query_enter_identity = f"""
        MATCH (j {{name: '{name}'}})
        RETURN j.name
        """
    res = data_base_connection.query(query=query_enter_identity, db='overwatchDataBase')
    print("print node: " + str(res))
    return


def user_identity_parser(data_base_connection, entity_name, entity_type, arn, region):
    if not node_exist(data_base_connection, entity_name):
        return
    oldarn = arn
    arn = camel(arn)
    query_enter_identity = f"""
    CREATE (n:{str(arn)} {{type: '{str(entity_type)}', arn: '{str(arn)}, region: {str(region)}'}})
    """
    data_base_connection.query(query_enter_identity, db='overwatchDataBase')
    print_node(data_base_connection, entity_name)
    # query_enter_identity = f"""
    # MERGE({str(entity_name)}: Service{{name: {str(entity_name)}, type: {str(entity_type)}, arn: {str(arn)}, region: {str(region)} }})
    # ON CREATE
    # SET {str(entity_name)}.created = timestamp()
    # ON MATCH
    # SET
    # {str(entity_name)}.lastSeen = timestamp()
    # RETURN {str(entity_name)}.name, {str(entity_name)}.created, {str(entity_name)}.lastSeen
    # """
    return


def event_source_parser(data_base_connection, entity_source_name, arn, region):
    if not node_exist(data_base_connection, entity_source_name):
        return
    oldarn = arn
    arn = camel(arn)
    entity_type = "AWSService"  # TODO: how to figure out its entity type ? what label to put? to update?
    query_enter_identity = f"""
        CREATE (n:{str(arn)} {{type: '{str(entity_source_name)}', arn: '{str(arn)}, region: {str(region)}'}})
        """
    data_base_connection.query(query_enter_identity, db='overwatchDataBase')
    print_node(data_base_connection, entity_source_name)
    return


def link_parser(data_base_connection, arn_initiator, arn_actuator, entity_source_name, entity_name, event_type, timestamp, source_ip, user_agent):
    # TODO:retrive type ?
    arn_initiator=camel(arn_initiator)
    arn_actuator=camel(arn_actuator)
    entity_type = "AWSService"
    time_stamp = timestamp
    if event_type == "AwsApiCall":
        reltype = 'AWS_API_CALL'
    else:
        reltype = 'MANAGEMENT'

    query_enter_identity = f"""
    MATCH (a:{arn_initiator}),(b:{arn_actuator})
    WHERE a.type = '{entity_name}' AND b.name = '{entity_source_name}'
    CREATE (a)-[relation:{reltype}]->(b)
    SET relation = {{Attributes:['{str(source_ip)}','{str(user_agent)}','{str(time_stamp)}']}}
    """
    # SET relation = {{properties:[{str(time_stamp)},{str(source_ip).replace(".","--")},{str(user_agent).replace(".","--")}]}}
    # time: [{str(time_stamp)}],
    # srcIP: [{str(source_ip).replace(":","--")}],
    # user_agent:[{user_agent.replace(":","--")}]}}]->(b)
    # RETURN type(r)

    # (MATCH(Service:{str(entity_source_name)}) -
    # [:{str(event_type)}{{timestamp:{str(timestamp)},source_ip:{str(source_ip.replace(".","-"))},user_agent:{str(user_agent)}}}]
    # -> (MATCH(Service:{str(entity_name)}
    ans = data_base_connection.query(query_enter_identity, db='overwatchDataBase')
    return


def taxonomy_layer(data, data_base_connection):
    # Entity keys:
    user_identity_parser(data_base_connection=data_base_connection,
                         entity_name=data['userIdentity']['invokedBy'].partition('.')[0],
                         entity_type=data['userIdentity']['type'],
                         arn=data['requestParameters']['sourceArn'].replace(":", "--"),
                         region=data['awsRegion'])
    event_source_parser(data_base_connection=data_base_connection,
                        entity_source_name=data['eventSource'].partition('.')[0],
                        arn=data['resources'][0]['ARN'].replace(":", "--"),
                        region=data['awsRegion'])
    link_parser(data_base_connection=data_base_connection,
                arn_initiator=data['requestParameters']['sourceArn'].replace(":", "--"),
                arn_actuator=data['resources'][0]['ARN'].replace(":", "--"),
                entity_source_name=data['eventSource'].partition('.')[0],
                entity_name=data['userIdentity']['invokedBy'].partition('.')[0],
                event_type=data['eventType'],
                timestamp=data['eventTime'],
                source_ip=data['sourceIPAddress'],
                user_agent=data['userAgent'])
    return


def print_nodes(data_base_connection):
    print_all_nodes_query = f"""
    MATCH (n) RETURN (n)
    """
    nodes = data_base_connection.query(print_all_nodes_query, db='overwatchDataBase')
    print("nodes:\n")
    print(str(nodes).replace(", ", "\n"))
    print("\n")
    return


def create_CSV_with_logs(path_to_logs_folder):
    dfs = []
    # C:\Users\lavi1\PycharmProjects\OverWatch\logFolder\AWSLogs\696714140038\CloudTrail\ca - central - 1\2021
    for root, dirs, files in os.walk(path_to_logs_folder, topdown=False):
        for filename in files:
            logpath = os.path.basename(filename)
            pathroot = root
            print(logpath)
            with gzip.open(join(root, filename), "rb") as f:
                data = json.loads(f.read().decode('utf-8'))
            df = pd.DataFrame(data['Records'])
            dfs.append(df)

    all_dfs = pd.concat(dfs)
    all_dfs.to_csv("logsInTable.csv")


def print_all_files_names(path_to_logs_folder):
    for root, dirs, files in os.walk(path_to_logs_folder, topdown=False):
        for filename in files:
            print(os.path.join(root, filename))
        for dir_name in dirs:
            print(os.path.join(root, dir_name))


def insert_single_log_entry(log_name, data_base_connection):
    show_me_the_databases = f"""
       SHOW
       DATABASES
       """
    ans = data_base_connection.query(query=show_me_the_databases, db="neo4j")
    print("show database Before: CREATE OR REPLACE \n" + str(ans))

    data_base_connection.query("CREATE OR REPLACE DATABASE overwatchDataBase")
    ans = data_base_connection.query(query=show_me_the_databases, db="overwatchDataBase")
    print("show database After: CREATE OR REPLACE \n" + str(ans))
    print("\n")
    print("Taxonomy for 1 log entry")
    # graph = Graph("bolt://localhost:7687", auth=("superman", "pizza"))

    with open(log_name, "r") as read_file:
        data = json.load(read_file)
    test = data['requestParameters']['sourceArn'].partition(":")[2]
    test = f"""{test}"""
    test.replace(":", "--")
    # print(test)
    print("Before taxonomy layer")
    print_nodes(data_base_connection)
    taxonomy_layer(data, data_base_connection)
    print("After taxonomy layer")
    print_nodes(data_base_connection)
    print("complete")
    return


def main():
    print("hello world")
    path_to_logs = "logFolder\\AWSLogs\\696714140038\\CloudTrail\\eu-central-1\\2021"
    # print_all_files_names(path_to_logs)
    # create_CSV_with_logs(path_to_logs)

    print("Connecting to neo4j DB...")
    data_base_connection = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="1234")
    print("Connected")

    insert_single_log_entry("logEntry.json", data_base_connection)

    return


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
