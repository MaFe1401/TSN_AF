FROM python:3.8
ENV PYTHONBUFFERED 1
WORKDIR /camaraclient
COPY /CamaraClient/requirements.txt /camaraclient/requirements.txt
RUN pip install -r requirements.txt
#RUN pip install pika
CMD ["python", "./__init__.py"]
