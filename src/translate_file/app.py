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
        try:
            original_text = read_file(bucket_name, key_name)
        except Exception as e:
            print(e)
            return f"Failed to read file - {e}"
        try: 
            translated_text = translate_text(original_text)
        except Exception as e:
            print(e)
            return f"Failed to translate text - {e}"
    else:
        return "Invalid file type. File must have .txt extension."

    print(translated_text)
    return translated_text

def read_file(bucket_name, key_name):

    s3_file = s3_client.get_object(Bucket=bucket_name, Key=key_name)
    s3_file_content = s3_file['Body'].read().decode('utf-8')

    return s3_file_content

def translate_text(original_text):

    response = translate_client.translate_text(
        Text=original_text,
        # Auto detect source language will call Amazon Comprehend to detect language
        SourceLanguageCode='auto',
        # Find other Translate language codes here: 
        # https://docs.aws.amazon.com/translate/latest/dg/what-is.html#what-is-languages
        TargetLanguageCode='en'
    )

    parsed_response = {
        'original_text': original_text,
        'translated_text': response['TranslatedText'],
        'original_language': response['SourceLanguageCode'],
        'target_language': response['TargetLanguageCode']
    }

    return parsed_response