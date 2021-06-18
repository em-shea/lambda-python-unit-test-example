import sys
sys.path.insert(0, '/opt')

import os
import json
import boto3
from botocore import translate

# region_name specified in order to mock in unit tests
s3_client = boto3.client('s3', region_name=os.environ['AWS_REGION'])
translate_client = boto3.client('translate', region_name=os.environ['AWS_REGION'])

def lambda_handler(event, context):

    print(event)
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key_name = event['Records'][0]['s3']['object']['key']
    print(bucket_name, key_name)

    if key_name.endswith('.txt'):
        original_text = read_file(bucket_name, key_name)
        translated_text = translate_text(original_text)
    else:
        return "Invalid file type. File must have .txt extension."

    return translated_text

def read_file(bucket_name, key_name):

    s3_file = s3_client.get_object(Bucket=bucket_name, Key=key_name)
    s3_file_content = s3_file['Body'].read().decode('utf-8')
    print(s3_file_content)
    json_content = json.loads(s3_file_content)
    print(json_content)

    return json_content

def translate_text(original_text):

    response = translate_client.translate_text(
        Text='string',
        # Auto detect source language will call Amazon Comprehend to detect language
        SourceLanguageCode='auto',
        # Find other Translate language codes here: 
        # https://docs.aws.amazon.com/translate/latest/dg/what-is.html#what-is-languages
        TargetLanguageCode='en'
    )

    return response
