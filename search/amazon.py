import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from environ import Env

env = Env()
env.read_env()

AWS_ACCESS_KEY = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
class Comprehend:

    def __init__(self):
        self.translate_client = boto3.client(
            'translate',
            region_name='ap-northeast-2',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        self.comprehend_client = boto3.client(
            'comprehend',
            region_name='ap-northeast-2',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            endpoint_url='https://comprehend.ap-northeast-2.amazonaws.com'
        )

    def translate(self, text):
        try:
            translate_text = self.translate_client.translate_text(
                Text=text,
                SourceLanguageCode='ko',
                TargetLanguageCode='en',
            )
            return translate_text['TranslatedText']
        except NoCredentialsError:
            return {"error": "Unable to locate credentials"}
        except PartialCredentialsError:
            return {"error": "Incomplete credentials provided"}

    def entities1(self, text):
        try:
            response = self.comprehend_client.detect_entities(
                Text=text,
                LanguageCode='en'
            )
            return response
        except NoCredentialsError:
            return {"error": "Unable to locate credentials"}
        except PartialCredentialsError:
            return {"error": "Incomplete credentials provided"}
        