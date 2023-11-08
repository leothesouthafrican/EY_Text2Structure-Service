# main.py

# Importing standard libraries
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

# Importing necessary modules from your script
from langchain.agents import AgentExecutor, LLMSingleActionAgent
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from text_invoice_parser import parse_invoice
from dotenv import load_dotenv
from tools import ALL_TOOLS
from template import prompt
from output_parser import CustomOutputParser
from agent_description_parser import agent_output_parser

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set up the LLM
llm = OpenAI(temperature=0)

# Set up the output parser
output_parser = CustomOutputParser()

# LLM chain consisting of the LLM and a prompt
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Set up the agent
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservation:"],
    allowed_tools=ALL_TOOLS[0],
)

# Set up the agent executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=ALL_TOOLS, verbose=True
)

@app.route('/parse-invoice', methods=['POST'])
def parse_invoice_api():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('/tmp', filename)
        file.save(file_path)

        # Parse the invoice
        try:
            parsed_invoice = parse_invoice(file_path, llm)

            # Prepare the executor input
            executor_input = {
                'input': f"Year: {parsed_invoice['Year']}, Month: {parsed_invoice['Month']}, Supplier: {parsed_invoice['Supplier']}, Country: {parsed_invoice['Supplier Country']}"
            }

            # Run the agent
            answer = agent_executor.run(executor_input)

            # Parse the agent output
            parsed_invoice = agent_output_parser(parsed_invoice, answer, llm)

            # Clean up the uploaded file
            os.remove(file_path)

            return jsonify(parsed_invoice)

        except Exception as e:
            return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

