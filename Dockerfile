FROM locustio/locust:2.12.1
RUN pip3 install pandas
RUN pip3 install locust_plugins
RUN pip3 install xmltodict

WORKDIR /mnt/locust

COPY . /mnt/locust/
