# TSN_AF

sudo docker-compose build  
sudo docker-compose up -d  

### Docker container IP address

sudo docker ps  
sudo docker inspect (id)  
sudo docker logs --tail 50 --follow --timestamps container_instance_name
### Generate an SSH RSA keypair 

ssh-keygen -t rsa -b 2048 -m PEM -f ./sshServer/rsa
