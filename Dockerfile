FROM python:3.9.0
WORKDIR /
RUN sudo apt-get install redis-server
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY . /
CMD ["python", "rest_server.py"]