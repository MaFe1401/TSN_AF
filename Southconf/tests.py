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

async def getSreamConfig():
    async with httpx.AsyncClient(http1=False, http2=True) as client:
        response = await client.get(url, headers=headers)
        print(response.json())
        return response.json()
       


response=asyncio.run(getSreamConfig())
with open('streamsConfig.json', 'w') as f:
    f.write(json.dumps(response))
     # stringResponse =  json.dumps(response, ensure_ascii=False, indent=4)
     # json.dump(stringResponse, f, ensure_ascii=False, indent=4)

