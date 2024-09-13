from netconf_client.connect import connect_ssh
from netconf_client.ncclient import Manager
from lxml import etree
import xml.etree.ElementTree as ET
import math
import json
import httpx

#import httpx
'''
def createSession(profile):
    sessionData = {'ueIpv4addr':'10.45.0.2', 'asIpv4addr':'192.168.21.10', 'qosProfile':profile}
    requests.post("http://10.8.0.1:8088/",data=sessionData)
    #print("CREATED NEW QOS FLOW IN OPEN5GS")
'''
#Gets running TAS configuration from Netopeer server microservice and streams configuration from CNC's Jetconf
def getconfig(): 
    session = connect_ssh(host="netopeer", port=830, username="netconf", password="netconf")
    mgr = Manager(session, timeout=120)
    config = mgr.get_config("running").data_xml
    '''''
    url = "https://192.168.2.20:8443/restconf/data/ieee802-dot1q-tsn-types-upc-version:tsn-uni"
    headers = {'X-SSL-Client-CN': 'marc'}
    streamsConfig = httpx.get(url, headers=headers)
    '''
    return config.decode('utf-8')

#Filters obtained configuration (deletes keystore xml fragment)
def filterInterfaces(config):
    xml = etree.XML(config)
    #interfaces = xml.xpath("//interfaces")
    interfaces = xml.find("interfaces",{None : 'urn:ietf:params:xml:ns:yang:ietf-interfaces'})
    # Iterating through child tags
    '''
    for elem in interfaces.iter():
        tag_elements = elem.tag.split("}")
        
        # Removing name spaces and attributes
        elem.tag = tag_elements[1]
        elem.attrib.clear()

        updated_data = ET.tostring(interfaces, encoding="unicode")

    print(updated_data)
    '''
    #xml.remove(keystore)
    #xml.strip_elements(xml,"urn:ietf:params:xml:ns:yang:ietf-keystore")
    #print(ET.tostring(interfaces,encoding="unicode"))
    #print(etree.tostring(interfaces,encoding="unicode",pretty_print=True))
    return etree.tostring(interfaces,encoding="unicode")
#Edits configuration of TSN NICs placed at the edges of the 5G logical TSN bridge
def editconfig(ip, payload):
    session = connect_ssh(host=ip, port=830, username="sys-admin", password="sys-admin")
    mgr = Manager(session, timeout=120)
    mgr.edit_config(config=str(payload))

def prepareDstt(config): #dstt: PORT_1 nwtt: PORT_0
    # Parsear el XML
    root = etree.fromstring(config)

    # Definir los namespaces para el XPath
    namespaces = {
        'ietf': 'urn:ietf:params:xml:ns:yang:ietf-interfaces',
        'sched' : 'urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched'
    }

    # Encontrar y eliminar el elemento con name=PORT_0
    for interface in root.xpath('//ietf:interface', namespaces=namespaces):
        name = interface.find('ietf:name', namespaces=namespaces)
        if name is not None and name.text == 'PORT_0':
            root.remove(interface)
    
    # Encontrar y modificar el texto del elemento "operation-name" que por algun motivo se recibe con un "sched:" delante que sobra
    for gateControlEntry in root.xpath('////sched:gate-control-entry',namespaces=namespaces):
        operationName = gateControlEntry.find('operation-name', {None : 'urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched'})
        operationName.text = "set-gate-states"
    # Crear un nuevo xml que tenga como root "config (al anterior le falta)"
    configuration = etree.Element("config")
    configuration.append(root)

    #print(etree.tostring(configuration,encoding="unicode", pretty_print=True))
    return etree.tostring(configuration,encoding="unicode", pretty_print=True)

def prepareNwtt(config):
    # Parsear el XML
    root = etree.fromstring(config)

    # Definir los namespaces para el XPath
    namespaces = {
        'ietf': 'urn:ietf:params:xml:ns:yang:ietf-interfaces',
        'sched' : 'urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched'
    }

    # Encontrar y eliminar el elemento con name=PORT_0
    for interface in root.xpath('//ietf:interface', namespaces=namespaces):
        name = interface.find('ietf:name', namespaces=namespaces)
        if name is not None and name.text == 'PORT_1':
            root.remove(interface)

    # Encontrar y modificar el texto del elemento "operation-name" que por algun motivo se recibe con un "sched:" delante que sobra
    for gateControlEntry in root.xpath('////sched:gate-control-entry',namespaces=namespaces):
        operationName = gateControlEntry.find('operation-name', {None : 'urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched'})
        operationName.text = "set-gate-states"

    # Crear un nuevo xml que tenga como root "config (al anterior le falta)"   
    configuration = etree.Element("config")
    configuration.append(root)

    #print(etree.tostring(configuration,encoding="unicode", pretty_print=True))
    return etree.tostring(configuration,encoding="unicode", pretty_print=True)

def countStreams(config):
    root = etree.fromstring(config)
    streamsTrafficClass = []
    # Definir los namespaces para el XPath
    namespaces = {
        'ietf': 'urn:ietf:params:xml:ns:yang:ietf-interfaces',
        'sched' : 'urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched'
    }
    # Encontrar y modificar el texto del elemento "operation-name" que por algun motivo se recibe con un "sched:" delante que sobra
    for gateControlEntry in root.xpath('////sched:gate-control-entry',namespaces=namespaces):
        gateStates = gateControlEntry.findall('gate-states-value', {None : 'urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched'}) #Encontrar los gate states
        for entry in gateStates:
            trafficClass = round(math.log2(int(entry.text)))
            if (trafficClass not in streamsTrafficClass and int(entry.text) != 255):
                #print("New stream: "+entry.text)
                streamsTrafficClass.append(trafficClass)
                print("New flow detected with PCP = "+str(trafficClass))
    
    return streamsTrafficClass

####RESTCONF-------------
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
    
def getEndInterfaces(streamConfig):
    responseString = json.dumps(streamConfig)
    listenersList = find_values('listeners-list', responseString)
    listenersListString = json.dumps(listenersList)
    endInterfaces = find_values('ip', listenersListString)
    print(endInterfaces)   
    return endInterfaces    
####RESTCONF-------------

config = """<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"><interface><name>PORT_0</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><bridge-port xmlns="urn:ieee:std:802.1Q:yang:ieee802-dot1q-bridge"><gate-parameter-table xmlns="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched"><gate-enabled>true</gate-enabled><admin-gate-states>255</admin-gate-states><admin-control-list><gate-control-entry><index>0</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>12000</time-interval-value><gate-states-value>4</gate-states-value></gate-control-entry><gate-control-entry><index>1</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>12000</time-interval-value><gate-states-value>255</gate-states-value></gate-control-entry><gate-control-entry><index>2</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>12000</time-interval-value><gate-states-value>2</gate-states-value></gate-control-entry><gate-control-entry><index>3</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>4964000</time-interval-value><gate-states-value>255</gate-states-value></gate-control-entry><gate-control-entry><index>4</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>12000</time-interval-value><gate-states-value>4</gate-states-value></gate-control-entry><gate-control-entry><index>5</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>12000</time-interval-value><gate-states-value>255</gate-states-value></gate-control-entry><gate-control-entry><index>6</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>12000</time-interval-value><gate-states-value>255</gate-states-value></gate-control-entry><gate-control-entry><index>7</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>1000</time-interval-value><gate-states-value>255</gate-states-value></gate-control-entry></admin-control-list><admin-cycle-time><numerator>1000000</numerator><denominator>1000000000</denominator></admin-cycle-time><admin-cycle-time-extension>0</admin-cycle-time-extension><admin-base-time><seconds>0</seconds><nanoseconds>0</nanoseconds></admin-base-time><config-change>true</config-change><supported-list-max>90</supported-list-max><supported-cycle-max><numerator>99999999</numerator><denominator>999999999</denominator></supported-cycle-max><supported-interval-max>999999999</supported-interval-max></gate-parameter-table></bridge-port></interface><interface><name>PORT_1</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><bridge-port xmlns="urn:ieee:std:802.1Q:yang:ieee802-dot1q-bridge"><gate-parameter-table xmlns="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched"><gate-enabled>true</gate-enabled><admin-gate-states>255</admin-gate-states><admin-control-list><gate-control-entry><index>0</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>12000</time-interval-value><gate-states-value>4</gate-states-value></gate-control-entry><gate-control-entry><index>1</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>4963000</time-interval-value><gate-states-value>255</gate-states-value></gate-control-entry><gate-control-entry><index>2</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>12000</time-interval-value><gate-states-value>2</gate-states-value></gate-control-entry><gate-control-entry><index>3</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>13000</time-interval-value><gate-states-value>255</gate-states-value></gate-control-entry><gate-control-entry><index>4</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>12000</time-interval-value><gate-states-value>4</gate-states-value></gate-control-entry><gate-control-entry><index>5</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>4951000</time-interval-value><gate-states-value>255</gate-states-value></gate-control-entry><gate-control-entry><index>6</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>12000</time-interval-value><gate-states-value>1</gate-states-value></gate-control-entry><gate-control-entry><index>7</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>12000</time-interval-value><gate-states-value>255</gate-states-value></gate-control-entry><gate-control-entry><index>8</index><operation-name xmlns:sched="urn:ieee:std:802.1Q:yang:ieee802-dot1q-sched">sched:set-gate-states</operation-name><time-interval-value>13000</time-interval-value><gate-states-value>255</gate-states-value></gate-control-entry></admin-control-list><admin-cycle-time><numerator>1000000</numerator><denominator>1000000000</denominator></admin-cycle-time><admin-cycle-time-extension>0</admin-cycle-time-extension><admin-base-time><seconds>0</seconds><nanoseconds>0</nanoseconds></admin-base-time><config-change>true</config-change><supported-list-max>90</supported-list-max><supported-cycle-max><numerator>99999999</numerator><denominator>999999999</denominator></supported-cycle-max><supported-interval-max>999999999</supported-interval-max></gate-parameter-table></bridge-port></interface></interfaces><keystore xmlns="urn:ietf:params:xml:ns:yang:ietf-keystore"><asymmetric-keys><asymmetric-key><name>genkey</name><algorithm>rsa2048</algorithm><public-key>MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsKs9JB7+4mXV0qmEmmE8r3bU2sifGKrtwYai1kLqbFEVp5EicfF1LFLcEjr04hIjTwi/FDkGmli9zizsiqpXQj/bmX0k3f+Oztu7Ozk5tdGyrC095k5Ntfm8y7JT4Fp7caxU2Sc6RtByI1H9FjWGcCBNx2PG2QGHXQ4t/JEttKEawY3VmwtF1MZsglQ4fKLnHoDi4R49dsPWuYgUhCqLMdE+t5miFa/DNCFOx52kNbKffzgSZsoCOa/hBVoe2qNu/Vvb/6R+ZjEh2Z2CBbYVqc6TtCTKJLElyJLTQRZHwFY2a//jbzY+7avF3epSCx61gXXqmN5I0x+wYjKDYy2tDQIDAQAB</public-key></asymmetric-key></asymmetric-keys></keystore><netconf-server xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-server"><listen><endpoint><name>default-ssh</name><ssh><tcp-server-parameters><local-address>0.0.0.0</local-address><keepalives><idle-time>1</idle-time><max-probes>10</max-probes><probe-interval>5</probe-interval></keepalives></tcp-server-parameters><ssh-server-parameters><server-identity><host-key><name>default-key</name><public-key><keystore-reference>genkey</keystore-reference></public-key></host-key></server-identity><client-authentication><supported-authentication-methods><publickey/><passsword/></supported-authentication-methods></client-authentication></ssh-server-parameters></ssh></endpoint></listen></netconf-server></data>"""
interfaces = filterInterfaces(config)
dsttConfig = prepareDstt(interfaces)
countStreams(dsttConfig)
#editconfig("192.168.4.51", dsttConfig)
