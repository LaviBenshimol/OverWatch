import json
from neo4j import __version__ as neo4j_version, GraphDatabase
from pandas import DataFrame

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
def neo4j_add_new_log():

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
def userIdentity_Parser(data,dbconnection):
    query_string = '''
        CREATE (:Paper {id: line.paper_id, class: line.label})
        '''
    name = data['userIdentity']['invokedBy']
    # MERGE(n {name: '3'})
    dbconnection.query(query_string, db='logstesting')
    query_string = '''
        USING PERIODIC COMMIT 500
        LOAD CSV WITH HEADERS FROM
        'https://raw.githubusercontent.com/ngshya/datasets/master/cora/cora_cites.csv'
        AS line FIELDTERMINATOR ','
        MATCH (citing_paper:Paper {id: line.citing_paper_id}),(cited_paper:Paper {id: line.cited_paper_id})
        CREATE (citing_paper)-[:CITES]->(cited_paper)
        '''
    dbconnection.query(query_string, db='logstesting')
    return
def eventSource_Parser(data,dbconnection):

    return
def link_Parser(data,dbconnection):

    return

def TaxonomyLayer(data,dbconnection):
    dbconnection.query("CREATE OR REPLACE DATABASE logstesting")
    #Entity keys:
    userIdentity_Parser(data, dbconnection)
    eventSource_Parser(data, dbconnection)
    link_Parser(data, dbconnection)
    data_entries = data.keys()
    identity_entity = data.items()
    # for i in data.get(userIdentity)
    #     #if its AWSService
    #     #type -> type
    #     #invokedBy -> name
    #     entity.append = data.get("userIdentity")

    return

# Defining main function
def main():
    print("hey there")
    dbconnection = Neo4jConnection(uri="bolt://localhost:7687", user="superman", pwd="pizza")
    with open("logEntry.json", "r") as read_file:
        data = json.load(read_file)
    TaxonomyLayer(data, dbconnection)
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