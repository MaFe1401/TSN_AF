import json

def find_values(id,json_repr):
    results = []

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[id])
        except KeyError:
            pass
        return a_dict
    
    json.loads(json_repr, object_hook=_decode_dict)
    return results

def delete_value(id,jsonFilePath):

    file = open(jsonFilePath,'r')
    fileJson = json.load(file)
    fileString = json.dumps(fileJson)
    data = json.loads(fileString)

    print("----DATA----")
    print(data)
    #print("----PORT----")
    #print(list(data["lldp"]["interface"][0].keys())[0])
    #print("----UPDATED DATA----")
    #data["lldp"]["interface"][0].pop(id)
    i = 0
    while i < len(data["lldp"]["interface"]):
        if (list(data["lldp"]["interface"][i].keys())[0]==id):

            print(f"Deleted {id} from {jsonFilePath}")

            del data["lldp"]["interface"][i]
        else: pass
        i+=1

    stringData = json.dumps(data,indent=3)
    with open(jsonFilePath, 'w') as file:
        file.truncate(0)
        for line in stringData:
            file.write(line)
    
    return data

fileNWTT = open('neighbors/dsttNeighbors.json','r')
jsonNWTT=json.load(fileNWTT)
stringNWTT=json.dumps(jsonNWTT)
#selectPort1 = find_values('PORT_1', stringNWTT)
#stringPORT1 = json.dumps(selectPort1)
#print(stringPORT1)
filteredNWTT=delete_value("PORT_1",'neighbors/nwttNeighbors.json')
