# Installing Boto3 and Botocore from ZIP Files

This guide provides steps to unzip `botocore.zip` and `boto3.zip` into their own respective directories, and then install all of the `.whl` files using `pip3`.

## Prerequisites

- Ensure you have Python 3 and `pip3` installed.
- Ensure you have `unzip` installed on your system.

## Steps

### 1. Unzip the Files

First, unzip the `botocore.zip` and `boto3.zip` files into their own respective directories.

```sh
# Unzip botocore.zip
unzip botocore.zip -d botocore

# Unzip boto3.zip
unzip boto3.zip -d boto3
```
### 2. Change into the botocore directory
```sh
cd botocore
```

### 3. Install all .whl files in the botocore directory
```sh
pip3 install *.whl
```

### 4. Repeat the same steps for boto3