from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

# Define the function that processes the invoice information
def agent_output_parser(invoice_data, agent_output, model):
    # Define the additional response schema for Description
    response_schemas = [
        ResponseSchema(name="Description", description="a short description of the services provided without mentioning the company name"),
    ]

    # Create the StructuredOutputParser for Description
    description_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    # Get the format instructions for Description
    format_instructions = description_parser.get_format_instructions()

    # Prepare the prompt template with the format instructions
    prompt_template = ("Please provide a short description of the services provided, "
                       "based on the invoice information, but do not include the company's name in the description:\n"
                       "{format_instructions}\n\n---\n\n{invoice_description}")
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["agent_output"],
        partial_variables={"format_instructions": format_instructions}
    )

    # Format the prompt with the actual invoice description but remove the company's name
    company_name = invoice_data.get('Supplier', '')
    agent_output_without_company_name = agent_output.replace(company_name, '[company]')  # Replace company name with a placeholder
    _input = prompt.format_prompt(invoice_description=agent_output_without_company_name)

    # Get the model's output for the description
    output = model(_input.to_string())

    # Parse the output to get the Description
    parsed_description_output = description_parser.parse(output)

    # Merge the parsed Description with the initial invoice_data
    invoice_data.update(parsed_description_output)

    # Return the merged dictionary
    return invoice_data
