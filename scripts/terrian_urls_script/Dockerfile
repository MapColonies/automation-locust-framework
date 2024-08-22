FROM python:3.8-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR terrain_script

# Run the application:
COPY ./generate_terrian_urls.py .

CMD ["python", "generate_terrian_urls.py"]