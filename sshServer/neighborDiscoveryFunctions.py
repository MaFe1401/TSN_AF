import paramiko
import os
import json
def checkNeighborsNWTT(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='sys-admin', password='sys-admin')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo lldpcli show neighbors -f json',get_pty=True)
    ssh_stdin.write('sys-admin\n')
    ssh_stdin.flush()
    data=ssh_stdout.readlines()
    print(os.getcwd())
    with open('neighbors/nwttNeighbors.json', 'a') as f:
        f.truncate(0)
        del data[0:2]
        for line in data:
            f.write(str(line)+'\n')
    print (data)
    return data

def checkNeighborsDSTT(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='sys-admin', password='sys-admin')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo lldpcli show neighbors -f json',get_pty=True)
    ssh_stdin.write('sys-admin\n')
    ssh_stdin.flush()
    data=ssh_stdout.readlines()
    print(os.getcwd())
    with open('neighbors/dsttNeighbors.json', 'a') as f:
        f.truncate(0)
        del data[0:2]
        for line in data:
            f.write(str(line)+'\n')
    print (data)
    return data
#exec = checkNeighborsNWTT("192.168.4.52")

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

def mergeNeighbors(neighborsDSTT, neighborsNWTT):
    jsonDSTT = json.load(neighborsDSTT)
    jsonNWTT = json.load(neighborsNWTT)
    stringDSTT = json.dumps(jsonDSTT)
    stringNWTT = json.dumps(jsonNWTT)
    delete_value('PORT_1','neighbors/nwttNeighbors.json')
    
