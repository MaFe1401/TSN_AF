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

def merge_neighbors(dsttPath, nwttPath):
    fileDSTT = open(dsttPath,'r')
    dataDSTT = json.load(fileDSTT)

    fileNWTT = open(nwttPath,'r')
    dataNWTT = json.load(fileNWTT)
    print("-----DATA DSTT-----")
    print(dataDSTT["lldp"]["interface"][0])
    try:
        mergedData = dataNWTT["lldp"]["interface"].append(dataDSTT["lldp"]["interface"][0])
        print("added one neighbor to the merged json")
    except: 
        print("No neighbors merged")
    try:
        mergedData = dataNWTT["lldp"]["interface"].append(dataDSTT["lldp"]["interface"][1])
        print("added two neighbor")
    except:
        print("No more neighbors")
    print("----MERGED DATA-----")
    print(dataNWTT)
    mergedDataJSON = json.dumps(dataNWTT,indent=3)
    with open('neighbors/mergedNeighbors.json','a') as file:
        file.truncate(0)
        for line in mergedDataJSON:
            file.write(line)
    return mergedDataJSON

fileNWTT = open('neighbors/dsttNeighbors.json','r')
jsonNWTT=json.load(fileNWTT)
stringNWTT=json.dumps(jsonNWTT)
#selectPort1 = find_values('PORT_1', stringNWTT)
#stringPORT1 = json.dumps(selectPort1)
#print(stringPORT1)
delete_value('PORT_1','neighbors/nwttNeighbors.json')
updatedNWTT=delete_value('PORT_PCIe','neighbors/nwttNeighbors.json') 
delete_value('PORT_0','neighbors/dsttNeighbors.json')
updatedDSTT=delete_value('PORT_PCIe','neighbors/dsttNeighbors.json')
merge_neighbors('neighbors/dsttNeighbors.json','neighbors/nwttNeighbors.json')
#print("---value---")
#print(find_values('RELY-TSN4',stringNWTT))
