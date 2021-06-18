import sys
sys.path.append('../../')

import os
import json
import unittest
from unittest import mock

with mock.patch.dict('os.environ', {'AWS_REGION': 'us-east-1'}):
  from translate_file.app import lambda_handler

def mocked_read_file(bucket_name, key_name):

    return "我爱写单元测试！"

def mocked_translate_text(original_text):

    return

class TranslateFileTest(unittest.TestCase):

    @mock.patch('translate_file.app.read_file', side_effect=mocked_read_file)
    @mock.patch('translate_file.app.translate_text', side_effect=mocked_translate_text)
    def test_build(self, translate_text_mock, read_file_mock):

        response = lambda_handler(self.s3_upload_event(), "")

        self.assertEqual(read_file_mock.call_count, 1)
        self.assertEqual(translate_text_mock.call_count, 1)

    # Mock S3 new file uploaded event
    def s3_upload_event(self):
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
                    "key":"test-file.txt",
                    "size":24,
                    "eTag":"06a83081d2bb215",
                    "sequencer":"0060CCC3C"
                    }
                }
            }
        ]
    }
