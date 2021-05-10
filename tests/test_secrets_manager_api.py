from moto import mock_secretsmanager, mock_kms
from secrets_migration.secrets_manager_api import SecretsManager, InvalidSecretError
from secrets_migration.secret import Secret
from secrets_migration.exceptions import PutSecretError
import boto3, botostubs
import unittest
import json


class TestSecretManager(unittest.TestCase):
    def test_create_dict_string(self):
        sm = SecretsManager()
        self.assertEqual(sm.create_dict_string({"test": "two"}), '{"test": "two"}')

    def test_create_dict_byte(self):
        sm = SecretsManager()
        self.assertEqual(
            sm.create_dict_byte({"test": "two"}), json.dumps({"test": "two"}).encode()
        )

    @staticmethod
    @mock_kms
    def create_cmk():
        kms = boto3.client("kms") # type: botostubs.KMS
        kms_key_creation = kms.create_key(
            Description="test",
            KeyUsage="ENCRYPT_DECRYPT")
        kms.create_alias(AliasName="alias/secretsmanager", TargetKeyId=kms_key_creation["KeyMetadata"]["KeyId"])

    @mock_secretsmanager
    def test_put_secret_string(self):
        sm = SecretsManager()
        secret = sm.create_dict_string({"test": "two"})
        self.create_cmk()
        self.assertIsInstance(
            sm.put_secret(
                secret_name="Testsecret",
                secret=secret,
                secret_description="Testing secret",
                kms_key_id="alias/secretsmanager"
            ),
            str,
        )

    @mock_secretsmanager
    def test_put_secret_bytes(self):
        sm = SecretsManager()
        secret = sm.create_dict_byte({"test": "two"})
        self.create_cmk()
        self.assertIsInstance(
            sm.put_secret(
                secret_name="Testsecret",
                secret=secret,
                secret_description="Testing secret",
                kms_key_id="alias/secretsmanager"
            ),
            str,
        )

    @mock_secretsmanager
    def test_failing_put_secret(self):
        sm = SecretsManager()
        self.create_cmk()
        with self.assertRaises(PutSecretError):
            sm.put_secret(
                secret_name="Testsecret",
                secret=None,
                secret_description="Testing secret",
                kms_key_id="alias/secretsmanager"
            )

    @mock_secretsmanager
    def test_getting_secret(self):
        sm = SecretsManager()
        secret = sm.create_dict_string({"test": "two"})
        self.create_cmk()
        sm.put_secret(
            secret_name="Testsecret", secret=secret, 
            secret_description="Testing secret", kms_key_id="alias/secretsmanager"
        )
        self.assertEqual(
            sm.get_secret(secret_id="Testsecret").secret_string,
            json.dumps({"test": "two"}),
        )

    @mock_secretsmanager
    def test_wrong_secret(self):
        sm = SecretsManager()
        with self.assertRaises(InvalidSecretError):
            sm.get_secret(secret_id="yoursoulismine")

    @mock_secretsmanager
    def test_getting_secrets(self):
        sm = SecretsManager()
        self.create_cmk()
        secret = sm.create_dict_string({"test": "two"})
        sm.put_secret(
            secret_name="Testsecret", secret=secret, 
            secret_description="Testing secret", kms_key_id="alias/secretsmanager"
        )
        self.assertEqual(len(sm.get_secrets()), 1)

    @mock_secretsmanager
    def test_next_token_getting_secrets(self):
        sm = SecretsManager()
        self.create_cmk()
        total_secrets = 0
        while total_secrets < 120:
            secret = sm.create_dict_string({"test": f"secret_{total_secrets}"})
            sm.put_secret(
                secret_name=f"Secret{total_secrets}",
                secret=secret,
                secret_description=f"This is secret number {total_secrets}",
                kms_key_id="alias/secretsmanager"
            )
            total_secrets += 1

        self.assertEqual(len(sm.get_secrets()), 120)


if __name__ == "__main__":
    unittest.main()
