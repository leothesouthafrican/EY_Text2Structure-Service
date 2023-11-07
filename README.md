# Text to Structured Data Microservice

This microservice is responsible for converting text files to structured JSON data using a Large Language Model (LLM).

## How It Works

The service listens for HTTP POST requests with a text payload. Upon receiving text, it uses an LLM to convert the text to structured data.

## Usage

To convert text to structured data, make a POST request to the `/convert` endpoint with the text in JSON format.

### Example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"text":"Your input text here"}' http://localhost:4002/convert
