from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from pymongo.results import InsertOneResult, InsertManyResult

from typing import Union

import os
from dotenv import load_dotenv

load_dotenv()


class DBHandler:
	def __init__(self, user_id: str, connection_string: Union[str, None] = None):
		"""
		Initialize the DBHandler class
		Args:
			user_id (str): The name of the collection containing the chat histories
			connection_string (str): The connection string to the MongoDB database
		"""
		# constants
		self.embeddings_db = 'embeddings'
		self.histories_db = 'histories'

		if not connection_string:
			connection_string = os.getenv('MONGODB_CONNECTION_STRING')
		try:
			if not connection_string or not isinstance(connection_string, str):
				raise ValueError('Connection string must be a non-empty string.')
			else:
				self.client = MongoClient(connection_string)
		except Exception as e:
			raise f'An error occurred while trying to connect to the database: {e}'

		self.embeddings_collection = self.client[self.embeddings_db][user_id]
		self.history_collection = self.client[self.histories_db][user_id]

	def get_history(self) -> list:
		"""
		Get the chat history from the database
		Returns:
			list: A list of strings containing the chat history in the format 'role: content'
		Raises:
			Exception: If an error occurs while trying to get the chat history
		"""
		try:
			messages = self.history_collection.find()
		except Exception as e:
			raise f'An error occurred while trying to get the chat history: {e}'

		# Format the messages in the desired 'role: content' format
		formatted_messages = [f"{message['role']}: {message['content']}" for message in messages]
		return formatted_messages

	def update(self, db: str, items: Union[dict, list]) -> Union[InsertOneResult, InsertManyResult]:
		"""
		Update the chat history in the database
		Args:
			db (str): The name of the db to update, either 'embeddings' or 'history'
			items (dict or list): A dictionary or a list of dictionaries containing the items to be added to the collection
		Returns:
			InsertOneResult or InsertManyResult: The ID of the inserted document or a list of IDs of the inserted documents
		Raises:
			ValueError: If the message is not a dictionary or a list of dictionaries
			Exception: If an error occurs while trying to update the chat history
		"""
		if db == 'embeddings':
			collection = self.embeddings_collection
		elif db == 'history':
			collection = self.history_collection
		else:
			raise ValueError('The db must be either "embeddings" or "history".')

		try:
			if isinstance(items, dict):
				result = collection.insert_one(items)
			elif isinstance(items, list):
				result = collection.insert_many(items)
			else:
				raise ValueError('items must be a dictionary or a list of dictionaries.')
		except BulkWriteError as bwe:
			raise RuntimeError(f'Duplicate key error occurred: {bwe.details}')
		except Exception as e:
			raise RuntimeError(f'An error occurred while trying to update the chat history: {str(e)}')

		return result

	def reset_history(self):
		"""
		Delete all the chat history from the collection
		Raises:
			Exception: If an error occurs while trying to reset the chat history
		"""
		try:
			self.history_collection.delete_many({})
		except Exception as e:
			raise f'An error occurred while trying to reset the chat history: {e}'

