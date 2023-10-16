FROM locustio/locust:2.17.0

RUN pip install --upgrade pip

RUN pip3 install --no-cache-dir locust_plugins==4.0.0

WORKDIR /mnt/locust

COPY . /mnt/locust/

RUN pip3 install --no-cache-dir -r requirements.txt
