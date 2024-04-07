FROM python:3.8
ENV PYTHONBUFFERED 1
WORKDIR /sshserver
COPY /sshServer/requirements.txt /sshserver/requirements.txt
RUN echo "HostKeyAlgorithms = +ssh-rsa" >> /etc/ssh/ssh_config
RUN echo "PubkeyAcceptedAlgorithms = +ssh-rsa" >> /etc/ssh/ssh_config
ADD sshServer/main.py .
ADD sshServer/serverBase.py .
ADD sshServer/serverInterface.py .
ADD sshServer/sshServerConn.py .
ADD sshServer/shell.py .
RUN pip install -r requirements.txt
RUN ssh-keygen -t rsa -b 2048 -m PEM -f ./rsa
CMD ["python", "./main.py"]