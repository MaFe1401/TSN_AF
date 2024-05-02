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

def delete_values(id,json_repr,jsonFilePath):
    results = []

    def _decode_dict(a_dict):
        try:
            pass
        except KeyError:
            results.append(a_dict[id])
        return a_dict
    
    json.loads(json_repr, object_hook=_decode_dict)
    with open(jsonFilePath,'a') as f:
        f.truncate(0)
        f.write(results)

    return results

def mergeNeighbors(neighborsDSTT, neighborsNWTT):
    jsonDSTT = json.load(neighborsDSTT)
    jsonNWTT = json.load(neighborsNWTT)
    stringDSTT = json.dumps(jsonDSTT)
    stringNWTT = json.dumps(jsonNWTT)
    delete_values('PORT_1',stringNWTT,'neighbors/dsttNeighbors.json')
    
