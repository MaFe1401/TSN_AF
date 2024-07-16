FROM python:3.8
ENV PYTHONBUFFERED 1
WORKDIR /southconf
COPY /Southconf/requirements.txt /southconf/requirements.txt
COPY /Southconf/__init__.py /southconf/__init__.py
RUN pip install -r requirements.txt
CMD ["python", "./__init__.py"]
