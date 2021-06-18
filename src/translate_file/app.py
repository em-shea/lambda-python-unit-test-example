# import sys
# sys.path.insert(0, '/opt')

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

    original_file = validate_and_retrieve_file(bucket_name, key_name)

    if original_file == "invalid file type":
        return "Invalid file type. A .txt file is required."
    else:
        translated_text = translate_file(event)

    return translated_text

def validate_and_retrieve_file(bucket_name, key_name):

    s3_file = s3_client.get_object(Bucket=bucket_name, Key=key_name)

    if s3_file.endswith('.txt'):
        s3_file_content = s3_file['Body'].read().decode('utf-8')
        json_content = json.loads(s3_file_content)
        print(json_content)
        return json_content
    else:
        return "invalid file type"

def translate_file(event):

    response = translate_client.translate_text(
        Text='string',
        # Auto detect source language will call Amazon Comprehend to detect language
        SourceLanguageCode='auto',
        # Find other Translate language codes here: 
        # https://docs.aws.amazon.com/translate/latest/dg/what-is.html#what-is-languages
        TargetLanguageCode='en'
    )

    return response
