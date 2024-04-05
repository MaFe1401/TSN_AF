FROM python:3.8
ENV PYTHONBUFFERED 1
WORKDIR /sshserver
COPY /sshServer/requirements.txt /sshserver/requirements.txt
RUN pip install -r requirements.txt
RUN ssh-keygen -t rsa -b 2048 -m PEM -f ./rsa
#CMD ["python", "./sshServer/main.py"]