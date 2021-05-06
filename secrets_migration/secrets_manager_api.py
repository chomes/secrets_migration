from typing import Dict, Union, List
from botocore.exceptions import ParamValidationError
from secrets_migration.exceptions import PutSecretError, InvalidSecretError
from secrets_migration.secret import Secret
import boto3
import json


class SecretsManager:
    def __init__(self, aws_profile: Union[str, None] = None) -> None:
        if not aws_profile:
            self.secrets_manager_client = boto3.client(
                "secretsmanager"
            )
        else:
            self.secrets_manager_client = boto3.Session(
                profile_name=aws_profile).client("secretsmanager")

    @staticmethod
    def create_dict_string(secret: dict) -> str:
        return json.dumps(secret)
    
    @staticmethod
    def create_dict_byte(secret: dict) -> bytes:
        return json.dumps(secret).encode()


    def put_secret(
        self,
        secret_name: str,
        secret: Union[str, bytes],
        secret_description: str = "",
    ) -> Union[Exception, str]:
        try:
            if isinstance(secret, bytes):
                create_secret: Dict[
                    str, Union[str, List[str]]
                ] = self.secrets_manager_client.create_secret(
                    Name=secret_name, Description=secret_description, SecretBinary=secret
                )

            if isinstance(secret, str):
                create_secret: Dict[
                    str, Union[str, List[str]]
                ] = self.secrets_manager_client.create_secret(
                    Name=secret_name, Description=secret_description, SecretString=secret
                )
            
            return create_secret["ARN"]
        except (ParamValidationError, UnboundLocalError) as error:
            raise PutSecretError(error_message=error) from error

    def get_secret(
        self,
        secret_id: str 
    ) -> Union[Dict[str, str], Exception]:
        try:
            return Secret(**self.secrets_manager_client.get_secret_value(
                SecretId=secret_id
            ))
        except self.secrets_manager_client.exceptions.ResourceNotFoundException:
            raise InvalidSecretError

    def get_secrets(
        self
    ) -> List[Dict[str, str]]:
        full_secrets = list()
        next_token: Union[str, None] = None
        while True:
            if next_token:
                incomplete_secrets: Dict[str, Union[List[dict], str]] = self.secrets_manager_client.list_secrets(
                    MaxResults=100, NextToken=next_token)
            else:
                incomplete_secrets: Dict[str, Union[List[dict], str]] = self.secrets_manager_client.list_secrets(
                    MaxResults=100)
            
            full_secrets += incomplete_secrets["SecretList"]
            if "NextToken" in incomplete_secrets:
                next_token = incomplete_secrets["NextToken"]
                continue
            else:
                break
        
        return full_secrets
