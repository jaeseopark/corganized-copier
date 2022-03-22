FROM python:3.10-buster

# Install dependencies & app module
WORKDIR /tmp/install

# install big packages separeatly from requirements.txt to save build times
RUN pip install pyAesCrypt==0.4.3 pycryptodome==3.6.6

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
