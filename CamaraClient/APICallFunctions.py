import requests

qosProfiles = []

def createSession(profile):
    sessionData = {'ueIpv4addr':'10.45.0.2', 'asIpv4addr':profile[1], 'qosProfile':profile[0]}
    requests.post("http://10.8.0.1:8088/",data=sessionData)
    #print("CREATED NEW QOS FLOW IN OPEN5GS")
    print("NEW REQUEST SENT TO QOD CAMARA API")

#def deleteSessions():

def QoSmapping(streamsList):
    
    streamsList["end_interfaces"].pop(0)
    try:
        streamsList["traffic_classes"].remove(0)
    except:
        print("no pcp = 0")

    streamsList["traffic_classes"].sort()
    i = -1
    print ("STREAMS LIST --------------")
    print(streamsList)
    for stream in streamsList["traffic_classes"]:
        #print("DETECTED "+stream)
        if (stream == 1): #PCP = 1
            i+=1
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append(['QOS_E',streamsList["end_interfaces"][i]])
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        elif (stream == 2): #PCP = 2
            i+=1
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append(['QOS_E',streamsList["end_interfaces"][i]])
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        elif (stream == 3): #PCP = 3
            i+=1
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append(['QOS_E',streamsList["end_interfaces"][i]])
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        elif (stream == 4): #PCP = 4
            i+=1
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append(['QOS_E',streamsList["end_interfaces"][i]])
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        elif (stream == 5): #PCP = 5
            i+=1
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append(['QOS_E',streamsList["end_interfaces"][i]])
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        elif (stream == 6): #PCP = 6
            i+=1
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append(['QOS_E',streamsList["end_interfaces"][i]])
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        elif (stream == 7): #PCP = 7
            i+=1
            if ('QOS_E' not in qosProfiles):
                qosProfiles.append(['QOS_E',streamsList["end_interfaces"][i]])
            else: print("FOUND AN ALREADY EXISTING QOS_E FLOW")
        else: continue
    
    return qosProfiles