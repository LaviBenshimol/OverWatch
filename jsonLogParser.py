import json

from neo4j import __version__ as neo4j_version, GraphDatabase
from pandas import DataFrame
from py2neo import Graph, Node, Relationship, NodeMatcher

print(neo4j_version)


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


def neo4j_add_new_log(conn):
    conn.query("CREATE OR REPLACE DATABASE coradb")

    query_string = '''
    USING PERIODIC COMMIT 500
    LOAD CSV WITH HEADERS FROM
    'https://raw.githubusercontent.com/ngshya/datasets/master/cora/cora_content.csv'
    AS line FIELDTERMINATOR ','
    CREATE (:Paper {id: line.paper_id, class: line.label})
    '''
    conn.query(query_string, db='coradb')
    query_string = '''
    USING PERIODIC COMMIT 500
    LOAD CSV WITH HEADERS FROM
    'https://raw.githubusercontent.com/ngshya/datasets/master/cora/cora_cites.csv'
    AS line FIELDTERMINATOR ','
    MATCH (citing_paper:Paper {id: line.citing_paper_id}),(cited_paper:Paper {id: line.cited_paper_id})
    CREATE (citing_paper)-[:CITES]->(cited_paper)
    '''
    conn.query(query_string, db='coradb')
    query_string = '''
    MATCH (p:Paper)
    RETURN DISTINCT p.class
    ORDER BY p.class
    '''
    conn.query(query_string, db='coradb')
    query_string = '''
    MATCH ()-->(p:Paper) 
    RETURN id(p), count(*) as indegree 
    ORDER BY indegree DESC LIMIT 10
    '''
    conn.query(query_string, db='coradb')
    query_string = '''
    CALL gds.graph.create(
      'coraGraph',
      'Paper',
      'CITES'
    )
    '''
    conn.query(query_string, db='coradb')
    query_string = '''
    CALL gds.pageRank.write('coraGraph', {
      writeProperty: 'pagerank'
    })
    YIELD nodePropertiesWritten, ranIterations
    '''
    conn.query(query_string, db='coradb')

    query_string = '''
    CALL gds.betweenness.write('coraGraph', { 
      writeProperty: 'betweenness' })
    YIELD minimumScore, maximumScore, scoreSum, nodePropertiesWritten
    '''
    conn.query(query_string, db='coradb')
    query_string = '''
    MATCH (p:Paper)
    RETURN DISTINCT p.id, p.class, p.pagerank, p.betweenness
    '''
    dtf_data = DataFrame([dict(_) for _ in conn.query(query_string, db='coradb')])
    dtf_data.sample(10)
    print(dtf_data.sample(10))
    conn.close()
    return


###############################################################################################
# END of working in neo4j
# conn = Neo4jConnection(uri="bolt://localhost:7687", user="superman", pwd="pizza")
###############################################################################################
###################################################
#     Taxonomy layer:
#
#                       sample: "evenName": "Invoke"
#     Graph data:
#
#         Nodes:
#             userIdentity:
#             Type: user/resource/service.
#             Priviledge learning ?
#             Counters?
#         Edges:
#             Type: Relation(Trusted/Owned) / Event(type).
#             Timestamp: convert time to specified format.
#             Source IP:
#             userAgent:
#             status: ? what info to inspect and record?
###################################################
# def nodeExist(lbl, node):
#     matcher = NodeMatcher(graph)
#     m = matcher.match(lbl, screen_name == node.screen_name).first()
#     if m is None:
#        return False
#     else:
#        return True
def user_identity_parser(data_base_connection, entity_name, entity_type, arn, region):
    #
    # name = data['userIdentity']['invokedBy']
    # name = name.partition('.')[0]
    # type = data['userIdentity']['type']
    # a = Node(name, name=name, type=type) #py2Neo
    query_enter_identity = f"""
    MERGE({str(entity_name)}: Service{{name: {str(entity_name)}, type: {str(entity_type)}, arn: {str(arn)}, region: {str(region)} }})
    ON CREATE
    SET {str(entity_name)}.created = timestamp()
    ON MATCH
    SET
    {str(entity_name)}.lastSeen = timestamp()
    RETURN {str(entity_name)}.name, {str(entity_name)}.created, {str(entity_name)}.lastSeen
    """

    ans = data_base_connection.query(query_enter_identity, db='loglake')
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

    ans = data_base_connection.query(query_enter_identity, db='loglake')
    return


def link_parser(data_base_connection,entity_name,entity_source_name, event_type, timestamp, source_ip, user_agent):
    query_enter_identity = f""""
    (MATCH(Service:{str(entity_source_name)}) - 
    [:{str(event_type)}{{timestamp:{str(timestamp)},source_ip:{str(source_ip)},user_agent:{str(user_agent)}}}] 
    -> (MATCH(Service:{str(entity_name)}
    """
    ans = data_base_connection.query(query_enter_identity, db='loglake')
    return


def TaxonomyLayer(data, data_base_connection):
    data_base_connection.query("CREATE OR REPLACE DATABASE logslake")
    # Entity keys:
    user_identity_parser(data_base_connection=data_base_connection,
                         entity_name=data['userIdentity']['invokedBy'].partition('.')[0],
                         entity_type=data['userIdentity']['type'],
                         arn=data['requestParameters']['sourceArn'],
                         region=data['awsRegion'])
    event_source_parser(dbconnection=data_base_connection,
                        entity_source_name=data['eventSource'],
                        arn=data['resources']['ARN'],
                        region=data['awsRegion'])
    link_parser(data_base_connection=data_base_connection,
                entity_name=data['userIdentity']['invokedBy'].partition('.')[0],
                entity_source_name=data['eventSource'],
                event_type=data['eventType'],
                timestamp=data['eventTime'],
                source_ip=data['sourceIPAddress'],
                user_agent=data['userAgent'])
    return


# Defining main function
def main():
    print("Connecting to neo4j DB...")
    data_base_connection = Neo4jConnection(uri="bolt://localhost:7687", user="superman", pwd="pizza")
    print("Connected")
    print("Taxonomy for 1 log entry")
    graph = Graph("bolt://localhost:7687", auth=("superman", "pizza"))

    with open("logEntry.json", "r") as read_file:
        data = json.load(read_file)
    TaxonomyLayer(data, data_base_connection)
    return


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
# print("hello")
#
# data = {
#     "president": {
#         "name": "Zaphod Beeblebrox",
#         "species": "Betelgeusian"
#     }
# }
# with open("data_file.json", "w") as write_file:
#     json.dump(data, write_file)
# with open("data_file.json", "r") as read_file:
#     data = json.load(read_file)
#
#
# # ##################################################
# #
# #     Taxonomy layer:
# #
# #         "evenName": "Invoke"
#     Node Format:
#
#
#     Edge Format:
# # ##################################################
#
# def TaxonomyLayer(data):
#     #Entity keys:
#     data_entries = data.keys()
#     identity_entity = data.items()
#     for i in data.get(userIdentity)
#         #if its AWSService
#         #type -> type
#         #invokedBy -> name
#         entity.append = data.get("userIdentity")
#
#     return ans
#
#
# # ##################################################
# #
# #     Decoding logs:
# #
# #         "evenName": "Invoke"
# # ##################################################
#
# with open("logEntry.json", "r") as currentLog:
#     data = json.load(currentLog)
#
# print(data)
# # ##################################################
# #
# #     Graph data:
# #
# #         Nodes:
# #             userIdentity:
# #             Type: user/resource/service.
# #             Priviledge learning ?
# #             Counters?
# #         Edges:

# #             Type: Relation(Trusted/Owned) / Event(type).
# #             Timestamp: convert time to specified format.
# #             Source IP:
# #             userAgent:
# #             status: ? what info to inspect and record?
# #
# # ##################################################
#
# nodes, edges = TaxonomyLayer(data)
# #update DB (create/update new nodes/edges)
