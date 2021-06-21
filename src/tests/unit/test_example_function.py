# Need to append path to run tests on function code in a different directory
import sys
sys.path.append('../../')

import unittest
from unittest import mock

with mock.patch.dict('os.environ', {'AWS_REGION': 'us-east-1'}):
    from translate_file.app import lambda_handler

# Mock call to S3 to read file
def mocked_read_file(bucket_name, key_name):
    return "我爱写单元测试！"

# Mock call to Translate to translate text
def mocked_translate_text(original_text):
    return {'original_text': '我爱写单元测试！', 'translated_text': 'I love writing unit tests!', 'original_language': 'zh', 'target_language': 'en'}

class TranslateFileTest(unittest.TestCase):

    # Test for valid file type (.txt)
    @mock.patch('translate_file.app.read_file', side_effect=mocked_read_file)
    @mock.patch('translate_file.app.translate_text', side_effect=mocked_translate_text)
    def test_valid_file(self, translate_text_mock, read_file_mock):

        file_type = "valid file"
        response = lambda_handler(self.s3_upload_event(file_type), "")
        expected_response = {'original_text': '我爱写单元测试！', 'translated_text': 'I love writing unit tests!', 'original_language': 'zh', 'target_language': 'en'}

        self.assertEqual(read_file_mock.call_count, 1)
        self.assertEqual(translate_text_mock.call_count, 1)
        self.assertEqual(response, expected_response)
    
    # Test for invalid file type (.pdf)
    @mock.patch('translate_file.app.read_file', side_effect=mocked_read_file)
    @mock.patch('translate_file.app.translate_text', side_effect=mocked_translate_text)
    def test_invalid_file(self, translate_text_mock, read_file_mock):

        file_type = "invalid file"
        response = lambda_handler(self.s3_upload_event(file_type), "")
        expected_response = "Invalid file type. File must have .txt extension."

        self.assertEqual(read_file_mock.call_count, 0)
        self.assertEqual(translate_text_mock.call_count, 0)
        self.assertEqual(response, expected_response)

    # Mock S3 new file uploaded event
    def s3_upload_event(self, file_type):
        if file_type == "valid file":
            file_name = "test-file.txt"
        if file_type == "invalid file":
            file_name = "test-file.pdf"

        return {
            "Records":[
            {
                "eventVersion":"2.1",
                "eventSource":"aws:s3",
                "awsRegion":"us-east-1",
                "eventTime":"2021-06-18T16:03:17.567Z",
                "eventName":"ObjectCreated:Put",
                "userIdentity":{
                    "principalId":"AWS:AIDAI7123123XY"
                },
                "requestParameters":{
                    "sourceIPAddress":"12.21.123.69"
                },
                "responseElements":{
                    "x-amz-request-id":"D104123123BXXE",
                    "x-amz-id-2":"DJH/123123/123/76dtHg7yYQ+LHws0xBUmqUrM5bdW"
                },
                "s3":{
                    "s3SchemaVersion":"1.0",
                    "configurationId":"677496ca-4ead-123-123-123",
                    "bucket":{
                    "name":"my-bucket-name",
                    "ownerIdentity":{
                        "principalId":"A3123123AR5"
                    },
                    "arn":"arn:aws:s3:::my-bucket-name"
                    },
                    "object":{
                    "key":file_name,
                    "size":24,
                    "eTag":"06a83081d2bb215",
                    "sequencer":"0060CCC3C"
                    }
                }
            }
        ]
    }
