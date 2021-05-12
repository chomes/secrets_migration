from moto import mock_secretsmanager, mock_kms
from secrets_migration.secrets_migration import SecretsMigration
from secrets_migration.secret import Secret
from secrets_migration.exceptions import NoMigrationAccountError
from typing import List, Dict
import boto3
import botostubs
import unittest
import json


class TestSecretsMigration(unittest.TestCase):
    @staticmethod
    @mock_kms
    def create_cmk():
        kms = boto3.client("kms")  # type: botostubs.KMS
        kms_key_creation = kms.create_key(
            Description="test", KeyUsage="ENCRYPT_DECRYPT"
        )
        kms.create_alias(
            AliasName="alias/secretsmanager",
            TargetKeyId=kms_key_creation["KeyMetadata"]["KeyId"],
        )

    @mock_secretsmanager
    def test_fetching_current_account_secret_info(self):
        secrets_migration = SecretsMigration()
        self.create_cmk()
        total_secrets = 0
        while total_secrets < 30:
            secret = secrets_migration.current_account.create_dict_string(
                {"test": f"secret_{total_secrets}"}
            )
            secrets_migration.current_account.put_secret(
                secret_name=f"Secret{total_secrets}",
                secret=secret,
                secret_description=f"This is secret number {total_secrets}",
                kms_key_id="alias/secretsmanager",
            )
            total_secrets += 1
        self.assertEqual(
            len(secrets_migration.fetch_current_accounts_secret_info()), 30
        )

    @mock_secretsmanager
    def test_converting_secret_info_into_secret_helpers(self):
        secrets_migration = SecretsMigration()
        self.create_cmk()
        secret = secrets_migration.current_account.create_dict_string(
            {"test": "secret_fool"}
        )
        secrets_migration.current_account.put_secret(
            secret_name="Testsecret",
            secret=secret,
            secret_description="Testing secret",
            kms_key_id="alias/secretsmanager",
        )
        secret_info: List[
            Dict[str, str]
        ] = secrets_migration.fetch_current_accounts_secret_info()
        self.assertEqual(
            secrets_migration.convert_secret_info_to_secret_helpers(
                secret_info=secret_info
            )[0].secret_description,
            "Testing secret",
        )

    @mock_secretsmanager
    def input_secret(self, secret: Secret):
        secrets_migration = SecretsMigration(migrating_account="test")
        self.create_cmk()
        if secrets_migration.check_secret_exists(secret=secret):
            pass
        else:
            arn = secrets_migration.migrate_account.put_secret(
                secret_name=secret.name,
                secret_description=secret.secret_description,
                secret=secret.secret_string,
                kms_key_id="alias/secretsmanager",
            )
            return secrets_migration.migrate_account.get_secret(secret_id=arn)

    @mock_secretsmanager
    def test_migrating_secrets(self):
        secrets_migration = SecretsMigration()
        self.create_cmk()
        secret = secrets_migration.current_account.create_dict_string(
            {"test": "secret_fool"}
        )
        secrets_migration.current_account.put_secret(
            secret_name="Testsecret",
            secret=secret,
            secret_description="Testing secret",
            kms_key_id="alias/secretsmanager",
        )
        secret_info: List[
            Dict[str, str]
        ] = secrets_migration.fetch_current_accounts_secret_info()
        secret_helpers: List[
            Secret
        ] = secrets_migration.convert_secret_info_to_secret_helpers(
            secret_info=secret_info
        )
        created_secret = list()
        for secret in secret_helpers:
            created_secret.append(self.input_secret(secret=secret))
        self.assertEqual(
            created_secret[0].secret_string, json.dumps(
                {"test": "secret_fool"})
        )

    def test_migrating_account_not_existing(self):
        secrets_migration = SecretsMigration()
        with self.assertRaises(NoMigrationAccountError):
            secrets_migration.migrate_secrets(
                kms_key_id="alias/secretsmanager")


if __name__ == "__main__":
    unittest.main()
