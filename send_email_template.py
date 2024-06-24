
import requests


def send_template(first_name,supplier,description,email_body,message_id):

    url = """https://prod-12.uksouth.logic.azure.com:443/workflows/54e720df7b1a477b8a1a3240802445a6/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=4MAqeDmaYSRq1yWm8xbR7w5HDcPv_X7tUd5KwvXymEk"""
    headers = {
        'Content-Type': 'application/json'
        }
    body = {
            "user_first_name": first_name,
            "supplier": supplier,
            "description": description,
            "message_id": message_id,
            "generated_email": email_body
        }
    output = requests.post(
        url=url,
        headers=headers,
        json=body)
    return {
        "message": "Email sent succesfully",
        "status_code": output.status_code
    }
