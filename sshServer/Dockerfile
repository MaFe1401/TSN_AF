FROM python:3.8
ENV PYTHONBUFFERED 1
WORKDIR /sshserver
COPY /sshServer/requirements.txt /sshserver/requirements.txt
ADD main.py .
ADD serverBase.py .
ADD serverInterface.py .
ADD shell.py .
ADD sshServer.py .
RUN pip install -r requirements.txt
RUN ssh-keygen -t rsa -b 2048 -m PEM -f ./rsa
CMD ["python", "./main.py"]