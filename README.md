# Text to Structured Data Microservice

This microservice is responsible for converting text files to structured JSON data using a Large Language Model (LLM).

## How It Works

The service listens for HTTP POST requests with a text payload. Upon receiving text, it uses an LLM to convert the text to structured data.

## Usage

To convert text to structured data, make a POST request to the `/convert` endpoint with the text in JSON format.

### Example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"text":"Your input text here"}' http://localhost:4002/convert

## Building and Running with Docker

To build and run the microservice using Docker, follow these steps:

1. Ensure Docker is installed on your system. You can download it from the [Docker website](https://www.docker.com/products/docker-desktop).

2. Build the Docker image by running the following command in your terminal:

```bash
docker build -t text-to-structured-data-microservice .
docker run -p 5003:5003 text-to-structured-data-microservice
