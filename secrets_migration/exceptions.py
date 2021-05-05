class PutSecretError(Exception):
    def __init__(self, error_message: str) -> None:
        self.error_message = error_message
    
    def __str__(self) -> str:
        return f"Failed to create secret see error message {self.error_message}"
    
class InvalidSecretError(Exception):
    def __str__(self) -> str:
        return "The secret you tried to get was not a valid secret, please try again."