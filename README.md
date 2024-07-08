# TSN_AF

sudo docker-compose build  
sudo docker-compose up -d  

### Docker container commands

sudo docker ps  
sudo docker inspect (id)  
sudo docker logs --tail 50 --follow --timestamps container_instance_name
sudo docker exec -it (id) bash

### Generate an SSH RSA keypair 

ssh-keygen -t rsa -b 2048 -m PEM -f ./sshServer/rsa  

### Edit config from netopeer server inside the container (for test purposes) 
netopeer2-cli  
connect  
edit-config --target running --config=/opt/dev/Netopeer2/example_configuration/qbv_config_1.xml  
