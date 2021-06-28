import os
import boto3

# Explicitly specifying where the default AWS region is found 
# (as an environment variable) to be able to mock it in the test
s3_client = boto3.client('s3', region_name=os.environ['AWS_REGION'])
translate_client = boto3.client('translate', region_name=os.environ['AWS_REGION'])

def lambda_handler(event, context):
    print(event)

    # Get S3 bucket and key name from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key_name = event['Records'][0]['s3']['object']['key']
    print(bucket_name, key_name)

    # If valid .txt file, read S3 file and translate text
    if key_name.endswith('.txt'):
        try:
            original_text = read_file(bucket_name, key_name)
        except Exception as e:
            print(e)
            return {
                "success": False,
                "response": f"Failed to read file - {e}"
            }
        try: 
            translated_text = translate_text(original_text)
        except Exception as e:
            print(e)
            return {
                "success": False,
                "response": f"Failed to translate text - {e}"
            }
    else:
        return {
            "success": False,
            "response": "Invalid file type. File must have .txt extension."
        }

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
        'success': True,
        'original_text': original_text,
        'translated_text': response['TranslatedText'],
        'original_language': response['SourceLanguageCode'],
        'target_language': response['TargetLanguageCode']
    }

    return parsed_response