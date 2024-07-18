import boto3

class Comprehend:
    def translate(text):

        translate_client = boto3.client(
            'translate',
            region_name='ap-northeast-2',
        )

        translate_text = translate_client.translate_text(
            Text=text,
            SourceLanguageCode='ko',
            TargetLanguageCode='en',
        )

        return translate_text['TranslatedText']
    
    def entities1(text):

        comprehend_client = boto3.client(
            'comprehend',
            region_name='ap-northeast-2',
            endpoint_url='https://comprehend.ap-northeast-2.amazonaws.com'
        )

        response = comprehend_client.detect_entities(
            Text=text,
            LanguageCode='en'
        )

        return response