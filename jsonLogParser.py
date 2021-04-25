import json
from neo4j import __version__ as neo4j_version, GraphDatabase
from pandas import DataFrame
from py2neo import Graph, Node, Relationship, NodeMatcher


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


def user_identity_parser(data_base_connection, entity_name, entity_type, arn, region):
    #
    # name = data['userIdentity']['invokedBy']
    # name = name.partition('.')[0]
    # type = data['userIdentity']['type']
    # a = Node(name, name=name, type=type) #py2Neo]
    query_enter_identity = f"""
    MATCH (j {{name: '{entity_name}'}})
    RETURN j.name
    """
    res = data_base_connection.query(query=query_enter_identity, db='overwatchDataBase')
    if res is None:
        return
    query_enter_identity = f"""
    CREATE (n:{str(entity_name)} {{name: '{str(entity_name)}', arn: '{str(arn)}, region: {str(region)}'}})
    """

    ans = data_base_connection.query(query_enter_identity, db='overwatchDataBase')
    query_enter_identity = f"""
    MATCH (j {{name: '{entity_name}'}})
    RETURN j.name
    """
    res = data_base_connection.query(query=query_enter_identity, db='overwatchDataBase')
    if res is None:
        return
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
    query_enter_identity = f"""
       MERGE({str(entity_source_name)}: Service{{name: {str(entity_source_name)},, arn: {str(arn)}, region: {str(region)} }})
       ON CREATE
       SET {str(entity_source_name)}.created = timestamp()
       ON MATCH
       SET
       {str(entity_source_name)}.lastSeen = timestamp()
       RETURN {str(entity_source_name)}.name, {str(entity_source_name)}.created, {str(entity_source_name)}.lastSeen
       """

    ans = data_base_connection.query(query_enter_identity, db='overwatchDataBase')
    return


def link_parser(data_base_connection, entity_name, entity_source_name, event_type, timestamp, source_ip, user_agent):
    query_enter_identity = f""""
    (MATCH(Service:{str(entity_source_name)}) - 
    [:{str(event_type)}{{timestamp:{str(timestamp)},source_ip:{str(source_ip)},user_agent:{str(user_agent)}}}] 
    -> (MATCH(Service:{str(entity_name)}
    """
    ans = data_base_connection.query(query_enter_identity, db='overwatchDataBase')
    return


def taxonomy_layer(data, data_base_connection):
    # Entity keys:
    user_identity_parser(data_base_connection=data_base_connection,
                         entity_name=data['userIdentity']['invokedBy'].partition('.')[0],
                         entity_type=data['userIdentity']['type'],
                         arn=data['requestParameters']['sourceArn'].replace(":","--"),
                         region=data['awsRegion'])
    # event_source_parser(data_base_connection=data_base_connection,
    #                     entity_source_name=data['eventSource'],
    #                     arn=data['resources'][0]['ARN'].replace(":","--"),
    #                     region=data['awsRegion'])
    # link_parser(data_base_connection=data_base_connection,
    #             entity_name=data['userIdentity']['invokedBy'].partition('.')[0],
    #             entity_source_name=data['eventSource'],
    #             event_type=data['eventType'],
    #             timestamp=data['eventTime'],
    #             source_ip=data['sourceIPAddress'],
    #             user_agent=data['userAgent'])
    return


# Defining main function
def main():
    print("Connecting to neo4j DB...")
    data_base_connection = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="1234")
    print("Connected")
    print("show DataBases")
    show_me_the_databases = f"""
    SHOW
    DATABASES
    """
    ans = data_base_connection.query(query=show_me_the_databases, db="neo4j")

    print(ans)
    data_base_connection.query("CREATE OR REPLACE DATABASE overwatchDataBase")
    ans = data_base_connection.query(query=show_me_the_databases, db="overwatchDataBase")

    print(ans)
    print("Taxonomy for 1 log entry")
    # graph = Graph("bolt://localhost:7687", auth=("superman", "pizza"))



    with open("logEntry.json", "r") as read_file:
        data = json.load(read_file)
    test = data['requestParameters']['sourceArn'].partition(":")[2]
    test = f"""{test}"""
    test.replace(":", "--")
    print(test)
    taxonomy_layer(data, data_base_connection)
    print("complete")
    return


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
