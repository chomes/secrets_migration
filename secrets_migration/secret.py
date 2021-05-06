from typing import List, Dict, Union
import json


class Secret:
    def __init__(self, **kwargs: dict) -> None:
        self.arn: str = kwargs["ARN"]
        self.name: str = kwargs["Name"]
        self.version_id: str = kwargs["VersionId"]
        self.secret_binary: Union[bytes, None] = (
            kwargs["SecretBinary"] if "SecretBinary" in kwargs else None
        )
        self.secret_string: Union[str, None] = (
            kwargs["SecretString"] if "SecretString" in kwargs else None
        )
        self.secret_description: str = kwargs["Description"] if "Description" in kwargs else ""
        self.version_stages: List[str] = kwargs["VersionStages"]
        self.created_date = kwargs["CreatedDate"]

    def __dict__(self) -> Dict[str, Union[str, bytes]]:
        secret = {"ARN": self.arn, "Name": self.name}
        if self.secret_binary:
            secret["SecretBinary"] = self.secret_binary

        if self.secret_string:
            secret["SecretString"] = self.secret_string
        
        if self.secret_description:
            secret["Description"] = self.secret_description

        return secret

    def convert_secret(self) -> Union[dict, str]:
        """Generate a secret that can be manipulated in a pythonic way from JSON bytes or stringifed json

        Returns:
            Union[dict, str]: Could be a string or a dict
        """
        if self.secret_binary:
            return json.loads(self.secret_binary.decode())

        if self.secret_string:
            return json.loads(self.secret_string)
