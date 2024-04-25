FROM python:3.8
ENV PYTHONBUFFERED 1
WORKDIR /sshserver
COPY /sshServer/requirements.txt /sshserver/requirements.txt
RUN echo "HostKeyAlgorithms = +ssh-rsa" >> /etc/ssh/ssh_config
RUN echo "PubkeyAcceptedAlgorithms = +ssh-rsa" >> /etc/ssh/ssh_config
#####OPENSSH
#RUN apt-get update && apt-get install -y openssh-server
#RUN mkdir /var/run/sshd
#RUN echo 'root:root' | chpasswd
#RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
#RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
#RUN echo "export VISIBLE=now" >> /etc/profile
#EXPOSE 22
#CMD ["sshd", "-D"]
#####
ADD sshServer/main.py .
ADD sshServer/serverBase.py .
ADD sshServer/serverInterface.py .
ADD sshServer/sshServerConn.py .
ADD sshServer/shell.py .
ADD sshServer/neighborDiscoveryFunctions.py .
ADD sshServer/neighbors/ .
RUN pip install -r requirements.txt
RUN ssh-keygen -t rsa -b 2048 -m PEM -f ./rsa
CMD ["python", "./main.py"]