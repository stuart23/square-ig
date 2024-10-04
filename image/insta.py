from ensta import Web
from boto3 import client as Boto3Client
from os import getenv, environ
from os.path import join, exists
from json import loads


INSTAGRAM_CREDENTIALS_ARN_ENV = 'instagram_credentials_arn'
INSTAGRAM_SESSION_BUCKET_ID_ENV = 'instagram_session_bucket_id'
INSTAGRAM_SESSION_KEY_ENV = 'instagram_session_key'


class WebS3(Web):
    def __init__(self):
        self.bucket_id = getenv(INSTAGRAM_SESSION_BUCKET_ID_ENV)
        self.session_key = getenv(INSTAGRAM_SESSION_KEY_ENV)
        self.session_file = join('/tmp', self.session_key)
        credentials = self.getInstagramCredentials()
        if self.get_session_object():
            print(f'Session retrieved from {self.session_file}')
            super().__init__(
                identifier=credentials['username'],
                password=credentials['password'],
                file=self.session_file
            )
        else:
            print(f'No session found. Initiating from credentials.')
            super().__init__(
                identifier=credentials['username'],
                password=credentials['password'],
                file=self.session_file
            )
            print('New instagram session created.')
            self.put_session_object()

    def get_session_object(self):
        """
        Downloads the session object from S3. If the object cannot be retrieved,
        returns False. If the file already exists, it will be overwritten.
        """
        print(f'Retrieving object {self.session_key} from bucket {self.bucket_id}')
        s3 = Boto3Client('s3')
        try:
            s3.download_file(
                Bucket=self.bucket_id,
                Key=self.session_key,
                Filename=self.session_file
            )
        except Exception as e:
            print(f"Error retrieving object: {e}")
            return False
        return True

    def put_session_object(self):
        """
        Uploads the session object to S3.
        """
        if exists(self.session_file):
            print(f'Uploading object {self.session_file} to bucket {self.bucket_id}')
        else:
            raise IOError(f'File {self.session_file} not found.')
        s3 = Boto3Client('s3')
        try:
            s3.upload_file(
                Bucket=self.bucket_id,
                Key=self.session_key,
                Filename=self.session_file
            )
        except Exception as e:
            print(f"Error uploading object: {e}")
            return False
        return True

    @staticmethod
    def getInstagramCredentials():
        '''
        Gets the instagram username and password from AWS secrets manager.
        '''
        credentials_arn = getenv(INSTAGRAM_CREDENTIALS_ARN_ENV)
        secretsmanager_client = Boto3Client('secretsmanager')
        instagram_credentials = loads(
            secretsmanager_client.get_secret_value(SecretId=credentials_arn)['SecretString']
        )
        username = instagram_credentials['username']
        print(f'Retrieved credentials for user {username}')
        return instagram_credentials
