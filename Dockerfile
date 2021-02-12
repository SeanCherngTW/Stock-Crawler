FROM python:3.9.0
WORKDIR /
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY . /
CMD ["python", "rest_server.py"]