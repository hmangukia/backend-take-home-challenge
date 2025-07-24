FROM python:3.12

# Set working directory
WORKDIR /code
COPY . /code
COPY assets /code/assets

# Install dependencies
RUN pip install -r requirements.txt
