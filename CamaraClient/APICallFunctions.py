import requests

qosProfiles = []

def createSession(profile):
    sessionData = {'ueIpv4addr':'10.45.0.2', 'asIpv4addr':'192.168.21.10', 'qosProfile':profile}
    requests.post("http://10.8.0.1:8088/",data=sessionData)
    #print("CREATED NEW QOS FLOW IN OPEN5GS")

#def deleteSessions():

def QoSmapping(streamsList):
    
    for stream in streamsList:
        #print("DETECTED "+stream)
        if (stream == '1'): #PCP = 1
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append('QOS_E')
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        elif (stream == '2'): #PCP = 2
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append('QOS_E')
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        elif (stream == '3'): #PCP = 3
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append('QOS_E')
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        elif (stream == '4'): #PCP = 4
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append('QOS_E')
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        elif (stream == '5'): #PCP = 5
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append('QOS_E')
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        elif (stream == '6'): #PCP = 6
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append('QOS_E')
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        elif (stream == '7'): #PCP = 7
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append('QOS_E')
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        else: continue
    
    return qosProfiles