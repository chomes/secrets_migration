class PutSecretError(Exception):
    def __init__(self, error_message: str) -> None:
        self.error_message = error_message
    
    def __str__(self) -> str:
        return f"Failed to create secret see error message {self.error_message}"
    
class InvalidSecretError(Exception):
    def __str__(self) -> str:
        return "The secret you tried to get was not a valid secret, please try again."

class NoMigrationAccountError(Exception):
    def __str__(self) -> str:
        return "The migration account hasn't been instantiated, please specify a profile and try again"

class FailedToMigrateSecretsError(Exception):
    def __init__(self, error_message: str) -> None:
        self.error_message = error_message
    
    def __str__(self) -> str:
        return f"Failed to migrate secrets due to the following error: {self.error_message}"