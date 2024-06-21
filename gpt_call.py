import json
import os
import ast
import logging
import warnings
from openai import AzureOpenAI
warnings.filterwarnings("ignore")  # Suppressing warnings

# Configure logging..
if len(logging.getLogger().handlers) > 0:
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)


def handling_gpt_ouput(gpt_response):
    try:
        # Try parsing the variable as a list
        parsed_variable = ast.literal_eval(gpt_response)
        logging.info('GPT response parsed successfully.')
        if isinstance(parsed_variable, list):
            # If it's already a list, return it as is
            logging.info('GPT response is already a JSON inside list.')
            return parsed_variable
    except (ValueError, SyntaxError):
        pass

    # Extract content between first and last curly braces
    start_index = gpt_response.find('{')
    end_index = gpt_response.rfind('}')

    if start_index != -1 and end_index != -1:
        extracted_content = gpt_response[start_index:end_index + 1]
        logging.info(f'Extracted GPT response as JSON in string format: {extracted_content}')
        output = eval(extracted_content)
        logging.info(f'Evaluated(eval()) string JSON response inside list: {[output]}')
        return  [output]  # Return the extracted content as a list
    logging.exception(f'handling_gpt_output_failed() - returning empty list :{gpt_response}')
    return []  # Return an empty list if extraction fails


def analyze_email_reply_by_gpt(email_reply,description,supplier,amount,tone):
    try:

        client = AzureOpenAI(
                azure_endpoint = os.getenv("azure_endpoint"),
                api_key = os.getenv("api_key"),
                api_version = os.getenv("api_version")
            )

        raw_json = {"generated_email_template" : "email_template_body"}
        system_message = f''' You are a Email template generator bot whose task is to generate an email template based on the requirements of the user email text
                    to negotiate the amount of the purchase order raised for the supplier {supplier}.
                    Email template will be generated based on the user email sleected tactics if any.
                    We have asked user also to select template tone also on a scale of 1 to 10, where towards 1 means soft and towards 10 means aggresive.
                    Tone of that email would be {tone}.
                    User purchase order details are below:
                    Description of purchase order is: {description}
                    Supplier name from we need to request negotiation is: {supplier}
                    Amount of purchase order is: {amount}. Do not add any currency symbol in amount.
                    User email content which you need to analyse is: {email_reply} .

                    Your final output should be in this JSON format with proper <br> tag to maintain paragraph spacing: {raw_json}

            '''

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Email template should be <br> format to maintain correct paragraph formatting."},
            {"role": "user", "content": f"Return only JSON format, do not write anything other than Filled JSON."},
        ]


        response = client.chat.completions.create(
            model='gpt-4-32k',
            messages=messages,
            temperature=0,
            n=1,
            stop=None,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        logging.info(response)
        jsonify_response = response.choices[0].message.content
        output = handling_gpt_ouput(jsonify_response)
        logging.info(output)
        return output[0]
    except Exception as exp:
        logging.exception(f"Something is wrong with  gpt_call_to_fill_raw_json: {exp}")
        return None
