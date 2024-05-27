FROM python:3.8

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR urls

# Run the application:
COPY ./big_json_file.py .

CMD ["python", "big_json_file.py"]
