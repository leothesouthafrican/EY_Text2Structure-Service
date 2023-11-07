# main.py

# Importing standard libraries
from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

# Importing custom libraries and functions
from langchain.agents import AgentExecutor, LLMSingleActionAgent
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from text_invoice_parser import parse_invoice
from dotenv import load_dotenv
from tools import ALL_TOOLS
from template import prompt
from output_parser import CustomOutputParser
from agent_description_parser import agent_output_parser

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Set up the LLM
llm = OpenAI(temperature=0)

# Define the route and the function to convert txt to JSON
@app.route('/convert-text-to-json', methods=['POST'])
def convert_text_to_json():
    # Check if the request has the part 'file'
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty part without a filename
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    try:
        # Save the file to a secure location and parse it
        filename = secure_filename(file.filename)
        text_file_path = os.path.join('/tmp', filename)
        file.save(text_file_path)
        
        # Parse the invoice
        parsed_invoice = parse_invoice(text_file_path, llm)

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

        # Prepare the executor input
        executor_input = {
            'input': f"Year: {parsed_invoice['Year']}, Month: {parsed_invoice['Month']}, Supplier: {parsed_invoice['Supplier']}, Country: {parsed_invoice['Country']}"
        }

        # Run the agent
        answer = agent_executor.run(executor_input)

        # Parse the agent output
        parsed_invoice = agent_output_parser(parsed_invoice, answer, llm)

        # Convert Year and Month to integers
        parsed_invoice['Year'] = int(parsed_invoice['Year'])
        parsed_invoice['Month'] = int(parsed_invoice['Month'])

        # Convert to JSON and return
        return jsonify(parsed_invoice)

    except Exception as e:
        return jsonify(error=str(e)), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
