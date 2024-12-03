# TSN AF

### Installation
sudo docker-compose build  
sudo docker-compose up  

### Docker container commands

sudo docker ps  
sudo docker inspect (id)  
sudo docker logs --tail 50 --follow --timestamps container_instance_name  
sudo docker exec -it (id) bash

### Generate an SSH RSA keypair 

ssh-keygen -t rsa -b 2048 -m PEM -f ./sshServer/rsa  

### Edit config from netopeer server inside the container (for test purposes) 
netopeer2-cli  
connect --login "user"   
edit-config --target running --config=/opt/dev/Netopeer2/example_configuration/qbv_config_1.xml  

### Operational diagram
![imagen](https://github.com/user-attachments/assets/a2f64be8-93f1-480b-86d7-6b6e79f8cf7d)  

### Limitations
TSN NIC IP addresses must be specified at TSN_AF/Southconf/__init\__.py and TSN_AF/sshServer/shell.py  
TSN NIC at DS-TT side (UERANSIM side) must use PORT_1 while TSN NIC at NW-TT side (Open5GS side) must use PORT_0  
Depends on an external private CAMARA API  
DS-TT TSN NIC configuration NETCONF messages are not being sent through the established GTP tunnel but instead go through common ETH interfaces. 



