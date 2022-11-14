FROM locustio/locust:2.12.1

RUN pip3 install --no-cache-dir locust_plugins==2.6.12

WORKDIR /mnt/locust

COPY . /mnt/locust/

RUN pip3 install -r requirements.txt
