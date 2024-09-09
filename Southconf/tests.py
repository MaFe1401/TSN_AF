import httpx
import asyncio
import json
'''
url = "https://192.168.2.20:8443/restconf/data/ieee802-dot1q-tsn-types-upc-version:tsn-uni"
headers = {'X-SSL-Client-CN': 'marc'}
streamsConfig = httpx.get(url, headers=headers)
print(streamsConfig)
'''
url = "http://192.168.2.20:8443/restconf/data/ieee802-dot1q-tsn-types-upc-version:tsn-uni"
headers = {'X-SSL-Client-CN': 'marc'}
#client = httpx.AsyncClient(http2=True)
#response = await client.get(url, headers=headers)

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


async def getStreamConfig():
    async with httpx.AsyncClient(http1=False, http2=True) as client:
        response = await client.get(url, headers=headers)
        print(response.json())
        return response.json()
       


response=asyncio.run(getStreamConfig())

def getEndInterfaces(streamConfig):
    responseString = json.dumps(streamConfig)
    listenersList = find_values('listeners-list', responseString)
    listenersListString = json.dumps(listenersList)
    endInterfaces = find_values('ip', listenersListString)
    print(endInterfaces)

with open('streamsConfig.json', 'w') as f:
    #f.write(json.dumps(response))
    responseString = json.dumps(response)
    listenersList = find_values('listeners-list', responseString)
    listenersListString = json.dumps(listenersList)
    endInterfaces = find_values('ip', listenersListString)
    print(endInterfaces)
    '''
    endIps = []
    for endInterface in endInterfaces:
        endInterfaceString = json.dumps(endInterface)
        endIp = find_values('ip', endInterfaceString)
        endIps.append(endIp)
    print("holaa1")
    print(endIps)
    print("holaa2")
    '''
     # stringResponse =  json.dumps(response, ensure_ascii=False, indent=4)
     # json.dump(stringResponse, f, ensure_ascii=False, indent=4)

