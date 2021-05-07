from secrets_migration.secret import Secret
import unittest
import json



class TestSecret(unittest.TestCase): 
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.secret_data = {
            "ARN": "False arn",
            "Name": "Testname",
            "VersionId": "Version ID 5",
            "VersionStages": "Version number 5",
            "CreatedDate": "4555"
        }

    def test_string_dict(self):
        if "SecretBinary" in self.secret_data:
            del self.secret_data["SecretBinary"]

        self.secret_data["SecretString"] = json.dumps({"Test": "Two"})
        secret = Secret(**self.secret_data)
        self.assertEqual(secret.__dict__(),
         {
             "ARN": "False arn",
             "Name": "Testname",
             "SecretString": json.dumps({"Test": "Two"})
         })
        del self.secret_data["SecretString"]
    
    def test_bytes_dict(self):
        if "SecretString" in self.secret_data:
            del self.secret_data["SecretString"]
        
        self.secret_data["SecretBinary"] = json.dumps({"Test": "Two"}).encode()
        secret = Secret(**self.secret_data)
        self.assertEqual(secret.__dict__(),
        {
            "ARN": "False arn",
            "Name": "Testname",
            "SecretBinary": json.dumps({"Test": "Two"}).encode()
        }
        )
        del self.secret_data["SecretBinary"]
    
    def test_convert_secret_string(self):
        if "SecretBinary" in self.secret_data:
            del self.secret_data["SecretBinary"]

        self.secret_data["SecretString"] = json.dumps({"Test": "Two"})
        secret = Secret(**self.secret_data)
        self.assertEqual(secret.convert_secret(),
        {"Test": "Two"} )
        del self.secret_data["SecretString"]
    
    def test_convert_secret_bytes(self):
        if "SecretString" in self.secret_data:
            del self.secret_data["SecretString"]
        
        self.secret_data["SecretBinary"] = json.dumps({"Test": "Two"}).encode()
        secret = Secret(**self.secret_data)
        self.assertEqual(secret.convert_secret(),
        {"Test": "Two"} )
        del self.secret_data["SecretBinary"]
    

if __name__ == "__main__":
    unittest.main()