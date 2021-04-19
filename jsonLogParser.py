import json

print("hello")

data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}
with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)
with open("data_file.json", "r") as read_file:
    data = json.load(read_file)


# ##################################################
#
#     Taxonomy layer:
#
#         "evenName": "Invoke"
# ##################################################

def TaxonomyLayer(data):
    #Entity keys:
    data_entries = data.keys()
    identity_entity = data.items()
    for i in data.get(userIdentity)
        #if its AWSService
        #type -> type
        #invokedBy -> name
        entity.append = data.get("userIdentity")

    return ans


# ##################################################
#
#     Decoding logs:
#
#         "evenName": "Invoke"
# ##################################################

with open("logEntry.json", "r") as currentLog:
    data = json.load(currentLog)

print(data)
nodes, edges = TaxonomyLayer(data)
#update DB (create/update new nodes/edges)