# SecretsManager migration

This python module allows you to migrate all of your secrets from one aws account to another.  


## AWS requirements

* IAM roles / IAM users who have programmatic access to read/create secrets
* Have at least a [CMK](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/kms-example-encrypt-decrypt-file.html) on the migration account that can be used to encrypt secrets
<br>
For programmatic ways to create one see [create_key](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.create_key) and [create_alias](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client.delete_alias) documentation.  You can also see test_secrets_manager_api for examples.
* Minimum of 1 secret on the primary account 



## Python requirements

The following modules are required for run:

* boto3
* json

The following modules are required to run under test:

* boto3
* moto
* botostubs
* json

## How to use

Make sure that you have two aws profiles in your .aws/credentials

Once done import the module.

```python
from secrets_migration.secrets_migration import SecretsMigration

>>> secrets_migration = SecretsMigration(
        current_account="AWS PROFILE WITH SECRETS",
        migrating_account="AWS PROFILE YOU'RE MOVING SECRETS TO")

>>> secrets_migration.migrate_secrets(kms_key_id="alias/secrets_migration")
True
```

<br>

You  **must** provide a migrating_account parameter for the account to migrate otherwise an exception will be raised.  You do not have to specify a current_account parameter if you have your current_account as a default profile or it's in your environment variables.

## What else can you do with this module?

You can fetch your secrets and create them individually if you choose using the secrets_manager_api module.  When fetching a secret it returns a helper called secret which is a object that allows you to convert your binary or stringified secret back into something python can work with.

## I found a bug

While the tests should cover most use cases, there may be some bugs that are un-accounted for please feel free to raise an issue if you find one!
