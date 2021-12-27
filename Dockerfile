FROM python:3.10-slim-buster

# Install dependencies & app module
WORKDIR /tmp/install
COPY requirements.txt setup.py ./
RUN pip install -r requirements.txt
COPY copier/ copier/
RUN python setup.py install

# Cleanup
RUN rm -rf /tmp/install

WORKDIR /app
COPY entrypoint.sh .

# Remove DOS newline
RUN sed -i 's/\r$//' entrypoint.sh
