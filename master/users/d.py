import json
string ="🟩🟨⬛"
jsonstring = json.dumps(string)
print(jsonstring)
string = json.loads(jsonstring)
print(string)