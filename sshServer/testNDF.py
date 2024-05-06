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

def delete_values(id,json_repr,jsonFilePath):
    #results = []
    #for key, value in json_repr.items():
        #temp = [key,value]
        #results.append(temp)
    #print("-------RESULTS---------")
    #print(results)
    dicti = json.loads(json_repr)
    result = []
    try:
        for element in dicti:
            if (element == dicti[id]):
                pass
            else: 
                result.append(element)
    except KeyError:
        print("NOT FOUND")
        pass
    
    
    newjson = json.dumps(result)
    #finalString= json.dumps(newjson,indent=2)
    #print(finalString)
    with open(jsonFilePath,'a') as f:
        f.truncate(0)
        for line in newjson:
            f.write(line)

    return result

fileNWTT = open('neighbors/dsttNeighbors.json','r')
jsonNWTT=json.load(fileNWTT)
stringNWTT=json.dumps(jsonNWTT)
selectPort1 = find_values('PORT_1', stringNWTT)
stringPORT1 = json.dumps(selectPort1)
print('''''''''''''''''''''''''''''''''''')
print(stringPORT1)
filteredNWTT=delete_values('PORT_1',stringNWTT,'neighbors/nwttNeighbors.json')
