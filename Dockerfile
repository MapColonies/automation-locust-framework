FROM locustio/locust:2.15.1

RUN pip install --upgrade pip

RUN pip3 install --no-cache-dir locust_plugins==3.2.1

WORKDIR /mnt/locust

COPY . /mnt/locust/

RUN pip3 install --no-cache-dir -r requirements.txt
