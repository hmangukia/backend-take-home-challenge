FROM python:3.12

# Set working directory
WORKDIR /code
COPY . /code

# Install dependencies
RUN pip install -r requirements.txt
