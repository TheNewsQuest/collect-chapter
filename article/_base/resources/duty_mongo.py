from dagster import resource
from pymongo import MongoClient
from pymongo.database import Database

from common.config.env import EnvVariables


@resource
def get_duty_mongo_client():
  """Get Mongo client for Duty database
  """
  client = MongoClient(EnvVariables.DUTY_MONGO_URI)
  db_client: Database = client.get_default_database()
  return db_client
