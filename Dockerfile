FROM python:3.6
WORKDIR /
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY . /
CMD ["python", "rest_server.py"]