FROM locustio/locust:2.12.1

RUN pip3 install locust_plugins

WORKDIR /mnt/locust

COPY . /mnt/locust/

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt
