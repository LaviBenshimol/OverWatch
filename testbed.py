import requests
import base64
end_point = 'https://5gmvb78aqi.execute-api.eu-central-1.amazonaws.com/testbed/upload'

file_name = 'virus.pdf'
# file_name = '5G-Security-White-Paper_8.15.pdf'
# file_name = 'InDesign-Transition-Toward-Open-Interoperable-Networks-2020.pdf'
folder = 'C:\\Users\\lavi1\\Desktop\\'
file_path = folder + file_name
encoded_pdf = 'JVBERi0xLjcNCiW1tbW1DQoxIDAgb2JqDQo8PC9UeXBlL0NhdGFsb2cvUGFnZXMgMiAwIFIvTGFuZyhlbi1VUykgL1N0cnVjdFRyZWVSb290IDEwIDAgUi9NYXJrSW5mbzw8L01hcmtlZCB0cnVlPj4vTWV0YWRhdGEgMjAgMCBSL1ZpZXdlclByZWZlcmVuY2VzIDIxIDAgUj4+DQplbmRvYmoNCjIgMCBvYmoNCjw8L1R5cGUvUGFnZXMvQ291bnQgMS9LaWRzWyAzIDAgUl0gPj4NCmVuZG9iag0KMyAwIG9iag0KPDwvVHlwZS9QYWdlL1BhcmVudCAyIDAgUi9SZXNvdXJjZXM8PC9Gb250PDwvRjEgNSAwIFI+Pi9FeHRHU3RhdGU8PC9HUzcgNyAwIFIvR1M4IDggMCBSPj4vUHJvY1NldFsvUERGL1RleHQvSW1hZ2VCL0ltYWdlQy9JbWFnZUldID4+L01lZGlhQm94WyAwIDAgNjEyIDc5Ml0gL0NvbnRlbnRzIDQgMCBSL0dyb3VwPDwvVHlwZS9Hcm91cC9TL1RyYW5zcGFyZW5jeS9DUy9EZXZpY2VSR0I+Pi9UYWJzL1MvU3RydWN0UGFyZW50cyAwPj4NCmVuZG9iag0KNCAwIG9iag0KPDwvRmlsdGVyL0ZsYXRlRGVjb2RlL0xlbmd0aCAxNTE+Pg0Kc3RyZWFtDQp4nKWNuwrCQBRE+wv3H6ZUi83d+NgshBTZxKAQULJgIZYaLBRM0O93DSm0doqBgcMcRDukaVS7TQHJMuSFw4NJlHxidQzBKrSxMboz02GGO1PumaK1hhZlE/gLkw6cQMMEVKxawt8CUjUGbR/u0A4rGVfFdJy8rt2zn57gt0xlONwz/WO2c7X4lg/OUYVfDcra4Q1VJTCbDQplbmRzdHJlYW0NCmVuZG9iag0KNSAwIG9iag0KPDwvVHlwZS9Gb250L1N1YnR5cGUvVHJ1ZVR5cGUvTmFtZS9GMS9CYXNlRm9udC9CQ0RFRUUrQ2FsaWJyaS9FbmNvZGluZy9XaW5BbnNpRW5jb2RpbmcvRm9udERlc2NyaXB0b3IgNiAwIFIvRmlyc3RDaGFyIDMyL0xhc3RDaGFyIDExOC9XaWR0aHMgMTggMCBSPj4NCmVuZG9iag0KNiAwIG9iag0KPDwvVHlwZS9Gb250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eG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgIHhtbG5zOnBkZj0iaHR0cDovL25zLmFkb2JlLmNvbS9wZGYvMS4zLyI+CjxwZGY6UHJvZHVjZXI+TWljcm9zb2Z0wq4gV29yZCBmb3IgT2ZmaWNlIDM2NTwvcGRmOlByb2R1Y2VyPjwvcmRmOkRlc2NyaXB0aW9uPgo8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIj4KPGRjOmNyZWF0b3I+PHJkZjpTZXE+PHJkZjpsaT5sYXZpIGJlbnNoaW1vbDwvcmRmOmxpPjwvcmRmOlNlcT48L2RjOmNyZWF0b3I+PC9yZGY6RGVzY3JpcHRpb24+CjxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iPgo8eG1wOkNyZWF0b3JUb29sPk1pY3Jvc29mdMKuIFdvcmQgZm9yIE9mZmljZSAzNjU8L3htcDpDcmVhdG9yVG9vbD48eG1wOkNyZWF0ZURhdGU+MjAyMS0wNC0yMVQxNDo1MToyOSswMzowMDwveG1wOkNyZWF0ZURhdGU+PHhtcDpNb2RpZnlEYXRlPjIwMjEtMDQtMjFUMTQ6NTE6MjkrMDM6MDA8L3htcDpNb2RpZnlEYXRlPjwvcmRmOkRlc2NyaXB0aW9uPgo8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iPgo8eG1wTU06RG9jdW1lbnRJRD51dWlkOkM4RjMwMDhBLTE3MjctNDI4RC04Qzk0LTVDMEVGOTc1MUNCQTwveG1wTU06RG9jdW1lbnRJRD48eG1wTU06SW5zdGFuY2VJRD51dWlkOkM4RjMwMDhBLTE3MjctNDI4RC04Qzk0LTVDMEVGOTc1MUNCQTwveG1wTU06SW5zdGFuY2VJRD48L3JkZjpEZXNjcmlwdGlvbj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCjwvcmRmOlJERj48L3g6eG1wbWV0YT48P3hwYWNrZXQgZW5kPSJ3Ij8+DQplbmRzdHJlYW0NCmVuZG9iag0KMjEgMCBvYmoNCjw8L0Rpc3BsYXlEb2NUaXRsZSB0cnVlPj4NCmVuZG9iag0KMjIgMCBvYmoNCjw8L1R5cGUvWFJlZi9TaXplIDIyL1dbIDEgNCAyXSAvUm9vdCAxIDAgUi9JbmZvIDkgMCBSL0lEWzw4QTAwRjNDODI3MTc4RDQyOEM5NDVDMEVGOTc1MUNCQT48OEEwMEYzQzgyNzE3OEQ0MjhDOTQ1QzBFRjk3NTFDQkE+XSAvRmlsdGVyL0ZsYXRlRGVjb2RlL0xlbmd0aCA4NT4+DQpzdHJlYW0NCnicLcs9AkBADEThyf6gdROty6xe4zAaJ3AVer3SNVbMSJGvSB7gU6v57oGPXdzEHhIOEheSiljF6XfmQUSRRBYm/s/Gu3wxbyfSDaSMZN6AF+9tCzINCmVuZHN0cmVhbQ0KZW5kb2JqDQp4cmVmDQowIDIzDQowMDAwMDAwMDEwIDY1NTM1IGYNCjAwMDAwMDAwMTcgMDAwMDAgbg0KMDAwMDAwMDE2NiAwMDAwMCBuDQowMDAwMDAwMjIyIDAwMDAwIG4NCjAwMDAwMDA0ODYgMDAwMDAgbg0KMDAwMDAwMDcxMSAwMDAwMCBuDQowMDAwMDAwODc5IDAwMDAwIG4NCjAwMDAwMDExMTggMDAwMDAgbg0KMDAwMDAwMTE3MSAwMDAwMCBuDQowMDAwMDAxMjI0IDAwMDAwIG4NCjAwMDAwMDAwMTEgNjU1MzUgZg0KMDAwMDAwMDAxMiA2NTUzNSBmDQowMDAwMDAwMDEzIDY1NTM1IGYNCjAwMDAwMDAwMTQgNjU1MzUgZg0KMDAwMDAwMDAxNSA2NTUzNSBmDQowMDAwMDAwMDE2IDY1NTM1IGYNCjAwMDAwMDAwMTcgNjU1MzUgZg0KMDAwMDAwMDAwMCA2NTUzNSBmDQowMDAwMDAxODg3IDAwMDAwIG4NCjAwMDAwMDIwOTYgMDAwMDAgbg0KMDAwMDAyNDEyMSAwMDAwMCBuDQowMDAwMDI3Mjg4IDAwMDAwIG4NCjAwMDAwMjczMzMgMDAwMDAgbg0KdHJhaWxlcg0KPDwvU2l6ZSAyMy9Sb290IDEgMCBSL0luZm8gOSAwIFIvSURbPDhBMDBGM0M4MjcxNzhENDI4Qzk0NUMwRUY5NzUxQ0JBPjw4QTAwRjNDODI3MTc4RDQyOEM5NDVDMEVGOTc1MUNCQT5dID4+DQpzdGFydHhyZWYNCjI3NjE3DQolJUVPRg0KeHJlZg0KMCAwDQp0cmFpbGVyDQo8PC9TaXplIDIzL1Jvb3QgMSAwIFIvSW5mbyA5IDAgUi9JRFs8OEEwMEYzQzgyNzE3OEQ0MjhDOTQ1QzBFRjk3NTFDQkE+PDhBMDBGM0M4MjcxNzhENDI4Qzk0NUMwRUY5NzUxQ0JBPl0gL1ByZXYgMjc2MTcvWFJlZlN0bSAyNzMzMz4+DQpzdGFydHhyZWYNCjI4MjMzDQolJUVPRg=='

file_content = base64.b64decode(encoded_pdf)
with open('my_file.pdf', 'w+b') as f:
    f.write(file_content)
#
# with open(file_path, 'rb') as f:
#     data = f.read()
#
# # files = {'file': data}
#
# # res = requests.post(url=end_point,
# #                     files=files,
# #                     headers={'Content-Type': 'application/pdf'})
#
# params = {'filename': file_name, 'test5000': 'param2'}
#
# res = requests.post(url=end_point,
#                     data=data,
#                     headers={'Content-Type': 'application/pdf'},
#                     params=params)
# # headers={'Content-Type': 'application/octet-stream'})
#
# print(res.text)

# import json
# import base64
# assert base64.b64decode(res.json()['data'][len('data:application/octet-stream;base64,'):]) == data


# "content": "$input.body",
# "params": "$util.escapeJavaScript($input.params('querystring))"