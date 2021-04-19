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
#     Decoding logs:
#
#         "evenName": "Invoke"
# ##################################################

with open("logEntry.json", "r") as currentLog:
    data = json.load(currentLog)

print(data)