from netconf_functions import *
import time
import lxml
from rabbitmq_queues import *
import json

nwttIp="192.168.4.52"
dsttIp="192.168.4.51"
if __name__ == "__main__":
    currentConfig = []

    while (True):
        time.sleep(3)
        #print("hola")
        config = getconfig()
        #config = """<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><keystore xmlns="urn:ietf:params:xml:ns:yang:ietf-keystore"><asymmetric-keys><asymmetric-key><name>genkey</name><algorithm>rsa2048</algorithm><public-key>MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsKs9JB7+4mXV0qmEmmE8r3bU2sifGKrtwYai1kLqbFEVp5EicfF1LFLcEjr04hIjTwi/FDkGmli9zizsiqpXQj/bmX0k3f+Oztu7Ozk5tdGyrC095k5Ntfm8y7JT4Fp7caxU2Sc6RtByI1H9FjWGcCBNx2PG2QGHXQ4t/JEttKEawY3VmwtF1MZsglQ4fKLnHoDi4R49dsPWuYgUhCqLMdE+t5miFa/DNCFOx52kNbKffzgSZsoCOa/hBVoe2qNu/Vvb/6R+ZjEh2Z2CBbYVqc6TtCTKJLElyJLTQRZHwFY2a//jbzY+7avF3epSCx61gXXqmN5I0x+wYjKDYy2tDQIDAQAB</public-key></asymmetric-key></asymmetric-keys></keystore><netconf-server xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-server"><listen><endpoint><name>default-ssh</name><ssh><tcp-server-parameters><local-address>0.0.0.0</local-address><keepalives><idle-time>1</idle-time><max-probes>10</max-probes><probe-interval>5</probe-interval></keepalives></tcp-server-parameters><ssh-server-parameters><server-identity><host-key><name>default-key</name><public-key><keystore-reference>genkey</keystore-reference></public-key></host-key></server-identity><client-authentication><supported-authentication-methods><publickey/><passsword/></supported-authentication-methods></client-authentication></ssh-server-parameters></ssh></endpoint></listen></netconf-server></data>"""
        if (config not in currentConfig):
            print("----NEW TAS CONFIG DETECTED----")
            currentConfig.clear()
            #print(config)
            currentConfig.append(config)
            print("----Waiting for new config----") 
            try:
                interfaces = filterInterfaces(config)
                print(interfaces)
            except Exception as e:
                print("No TAS configuration found yet")
                #print (e)
                continue
            print("---------------------------------------")
            print("---- DS-TT TAS CONFIGURATION EDITED----")
            dsttConfig = prepareDstt(interfaces)
            editconfig(dsttIp, dsttConfig)
            print("---- NW-TT TAS CONFIGURATION EDITED----")
            nwttConfig = prepareNwtt(interfaces)
            editconfig(nwttIp, nwttConfig)
            trafficClassesList = countStreams(dsttConfig)
            
            streamsData = {}
            streamsData["traffic_classes"] = trafficClassesList
            json_streams_data = json.dumps(streamsData, indent = 4)
            send_message(json_streams_data, 'south-cam')

