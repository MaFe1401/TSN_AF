import requests

def createSession(profile):
    sessionData = {'ueIpv4addr':'10.45.0.2', 'asIpv4addr':'192.168.21.10', 'qosProfile':profile}
    requests.post("http://10.8.0.1:8088/",data=sessionData)
    print("CREATED NEW QOS FLOW IN OPEN5GS")

#def deleteSessions():

def QoSmapping(streamsList):
    qosProfiles = []
    for stream in streamsList:
        if (stream == '2'): #PCP = 1
            print("DETECTED "+stream)
            qosProfiles.append('QOS_E')
        elif (stream == '4'): #PCP = 2
            qosProfiles.append('QOS_E')
        elif (stream == '8'): #PCP = 3
            qosProfiles.append('QOS_E')
        elif (stream == '16'): #PCP = 4
            qosProfiles.append('QOS_E')
        elif (stream == '32'): #PCP = 5
            qosProfiles.append('QOS_E')
        elif (stream == '64'): #PCP = 6
            qosProfiles.append('QOS_E')
        elif (stream == '128'): #PCP = 7
            qosProfiles.append('QOS_E')
        else: continue
    
    return qosProfiles