import json
import os

import boto3
from dataclasses_json import DataClassJsonMixin
from smart_open import open as s_open
from vnexpress.common.enums.aws import AWSServices


def upload_file_s3(filename: str, bucket: str, object_name=None):
  """Upload a file to a bucket in S3

  Args:
      filename (str): _description_
      bucket (str): _description_
      object_name (_type_, optional): _description_. Defaults to None.
  """
  if object_name is None:
    object_name = os.path.basename(filename)
  # Upload the file
  s3_client = boto3.client(AWSServices.S3)
  s3_client.upload_file(filename, bucket, object_name)


def write_file_s3(data: object, uri: str):
  """Write data into file on S3 Bucket via URI and filename.

  Args:
      data (object): Data
      uri (str): URI of S3 bucket
  """
  with s_open(uri, 'w', encoding='utf-8') as file:
    file.write(data)


def write_json_file_s3(data: object, uri: str):
  """Write Python object(s) into a JSON file on S3 Bucket via URI.

  Args:
      data (object): Data
      uri (str): URI of S3 bucket resource
  """
  with s_open(uri, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)


def read_dataclass_json_file_s3(dataclass: DataClassJsonMixin, uri: str,
                                many: bool) -> object:
  """Read json file as dataclass.

  Args:
      dataclass (DataClassJsonMixin): Dataclass
      uri (str): S3 URI
      many (bool): (True) Parse many into list | (False) Parse one into object

  Returns:
      object: Data object(s)
  """
  data = None
  with s_open(uri, 'r') as file:
    data = dataclass.schema().loads(file.read(), many=many)
  return data
