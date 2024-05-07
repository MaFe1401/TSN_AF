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
    #results = []
    #for key, value in json_repr.items():
        #temp = [key,value]
        #results.append(temp)
    #print("-------RESULTS---------")
    #print(results)
    #dicti = json.loads(json_repr)
    #result = []
    file = open(jsonFilePath)
    
    data = json.load(file)
    print("----DATA----")
    print(data)

    ports = data["lldp"]["interface"]
    print(ports)

    print(list(ports[0].keys()))
 
    for i in ports:
        print (list(i.keys()))
        if (list(i.keys())[0] == id):
            removedValue = list(i.keys())[0]
            del list(i.keys())[0]

            print(f"Removed '{id}' with value '{removedValue}'")
            print ("----PORTS----")
            print(ports)
        
            

    #if id in data["lldp"].keys():
        #removedValue = data[id]
        
        #print(f"Removed '{id}' with value '{removedValue}'")
    print(data)
    stringData = json.dumps(data)
    with open(jsonFilePath, 'w') as file:
        #file.truncate(0)
        for line in stringData:
            file.write(line)
        #json.dump(data, file, indent=2)
    
    return data
    ''''
    def _decode_dict(a_dict):
        try:
            for element in a_dict:
                if (element == a_dict[id]):
                    print("----FOUND----")
                else: 
                    result.append(element)
        except KeyError:
            print("NOT FOUND")
            print(element)
            print(a_dict[id])
            pass
        return a_dict
    
    
    json.loads(json_repr, object_hook=_decode_dict)
    #finalString= json.dumps(newjson,indent=2)
    #print(finalString)
    with open(jsonFilePath,'a') as f:
        f.truncate(0)
        for line in json_repr:
            f.write(line)

    return result
'''
fileNWTT = open('neighbors/dsttNeighbors.json','r')
jsonNWTT=json.load(fileNWTT)
stringNWTT=json.dumps(jsonNWTT)
#selectPort1 = find_values('PORT_1', stringNWTT)
#stringPORT1 = json.dumps(selectPort1)
print('''''''''''''''''''''''''''''''''''')
#print(stringPORT1)
filteredNWTT=delete_value('PORT_1','neighbors/nwttNeighbors.json')
