import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="secrets_migration", # Replace with your own username
    version="1.4",
    author="chomes",
    author_email="jaayjay@gmail.com",
    description="A way to migrate your secrets from one aws account to another",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chomes/secrets_migration",
    packages=setuptools.find_packages(include=["boto3", "moto", "botostubs"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)