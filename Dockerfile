
FROM locustio/locust:latest

RUN pip3 install --no-cache-dir locust_plugins==4.5.1

WORKDIR /mnt/locust

COPY . /mnt/locust/

RUN pip3 install --no-cache-dir -r requirements.txt