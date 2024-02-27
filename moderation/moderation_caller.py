from openai import OpenAI
import os

def create_client():
    api_key = os.environ['OPENAI_API_KEY']
    client = OpenAI(api_key=api_key)
    return client

def moderate(client, comment):
    response = client.moderations.create(input=comment)
    output = response.results[0]
    return output
