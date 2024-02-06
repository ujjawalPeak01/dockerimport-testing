# Use an official Python runtime as a parent image
FROM python:3.10.13

# Set the working directory in the container
WORKDIR /app

COPY ./requirements.txt requirements.txt

COPY . /app

RUN pip3 install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8080

# Define an environment variable
# This variable will be used by Uvicorn as the binding address
ENV HOST 0.0.0.0

# Run the FastAPI application using Uvicorn when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
