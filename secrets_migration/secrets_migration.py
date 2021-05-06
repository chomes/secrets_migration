from secrets_migration.secrets_manager_api import SecretsManager
from secrets_migration.secret import Secret
from typing import List, Dict, Union
from secrets_migration.exceptions import (
    PutSecretError,
    InvalidSecretError,
    NoMigrationAccountError,
    FailedToMigrateSecretsError,
)


class SecretsMigration:
    def __init__(
        self,
        current_account: Union[str, None] = None,
        migrating_account: Union[str, None] = None,
    ) -> None:
        if not current_account:
            self.current_account: SecretsManager = SecretsManager()
        else:
            self.current_account: SecretsManager = SecretsManager(
                aws_profile=current_account
            )

        if not migrating_account:
            self.migrate_account: Union[SecretsManager, None] = None
        else:
            self.migrate_account: Union[SecretsManager, None] = SecretsManager(
                aws_profile=migrating_account
            )

    def fetch_current_accounts_secret_info(self) -> List[Dict[str, str]]:
        """Get all of the details apart from the secret itself for all your secrets in your
        existing account

        Returns:
            List[Dict[str, str]]: Returns all of your secret details
        """
        return self.current_account.get_secrets()

    def convert_secret_info_to_secret_helpers(
        self, secret_info: List[Dict[str, str]]
    ) -> List[Secret]:
        """Using the list from fetch_current_accounts_secret_info
        Loop over each secret and fetch the actual secret along with adding the description
        for the secret so we can get it ready to migrate.

        Args:
            secret_info (List[Dict[str, str]]): [description]

        Returns:
            List[Secret]: [description]
        """
        secret_helpers = list()
        for secret_data in secret_info:
            secret: Secret = self.current_account.get_secret(
                secret_id=secret_data["ARN"]
            )
            secret.secret_description = secret_data["Description"]
            secret_helpers.append(secret)

        return secret_helpers

    def migrate_secrets(self) -> Union[Exception, bool]:
        """Migrate your secrets from current_account to migrate_account

        Raises:
            NoMigrationAccountError: Raised when you have not specified an aws profile
            for the migration_account
            FailedToMigrateSecretsError: This first one fails due to parameter problems
            provided code isn't change this should not be raised.
            FailedToMigrateSecretsError: Raised when a secret does not exist, 
            this should not happen unless you delete secrets during the migration process
            on the current account.

        Returns:
            Union[Exception, bool]: Returns either True or Exception that was raised
        """
        if not self.migrate_account:
            raise NoMigrationAccountError

        try:
            secret_info: List[
                Dict[str, str]
            ] = self.fetch_current_accounts_secret_info()
            secret_helpers: List[Secret] = self.convert_secret_info_to_secret_helpers(
                secret_info=secret_info
            )
            for secret in secret_helpers:
                self.migrate_account.put_secret(
                    secret_name=secret.name,
                    secret=secret.secret_string
                    if "SecretString" in secret.__dict__()
                    else secret.secret_binary,
                    secret_description=secret.secret_description,
                )

            return True
        except PutSecretError as error:
            raise FailedToMigrateSecretsError(error_message=str(error)) from error
        except InvalidSecretError as error:
            raise FailedToMigrateSecretsError(error_message=str(error)) from error
