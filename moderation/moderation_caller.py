from openai import OpenAI
import os

def create_client():
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current module
    api_file_path = os.path.join(current_dir, "API.txt")  # Construct the path to API.txt in the same directory
    with open(api_file_path, 'r') as file:
        api_key = file.read().strip()  # Read the API key from the file and strip any leading/trailing whitespace
    client = OpenAI(api_key=api_key)
    return client

def moderate(client, comment):
    response = client.moderations.create(input=comment)
    output = response.results[0]
    return output
