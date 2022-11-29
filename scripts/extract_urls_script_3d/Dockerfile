FROM python:3.8

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR urls

# Run the application:
COPY ./extract_url.py .

CMD ["python", "extract_url.py"]
