from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from pymongo.results import InsertOneResult, InsertManyResult

from typing import Union

import os
from dotenv import load_dotenv

load_dotenv()


class DBHandler:
	def __init__(self, org_id: str, user_id: str, connection_string: Union[str, None] = None,
				 search_method: str = 'approximate'):
		"""
		Initialize the DBHandler class
		Args:
			org_id (str): The name of the collection containing the embeddings
			user_id (str): The name of the collection containing the chat histories
			connection_string (str): The connection string to the MongoDB database
		Raises:
			ValueError: If the connection string is not a non-empty string
			RuntimeError: If an error occurs while trying to connect to the database
		"""
		# constants
		self.embeddings_db = 'embeddings'
		self.histories_db = 'histories'
		self.exact_search = True if search_method == 'exact' else False

		if not connection_string:
			connection_string = os.getenv('MONGODB_CONNECTION_STRING')
		try:
			if not connection_string or not isinstance(connection_string, str):
				raise ValueError('Connection string must be a non-empty string.')
			else:
				self.client = MongoClient(connection_string)
		except Exception as e:
			raise f'An error occurred while trying to connect to the database: {e}'

		self.org_id = org_id
		self.embeddings_collection = self.client[self.embeddings_db][org_id]

		self.user_id = user_id
		self.history_collection = self.client[self.histories_db][user_id]

	def get_history(self) -> list:
		"""
		Get the chat history from the database
		Returns:
			formatted_messages (list): A list of strings containing the chat history in the format 'role: content'
		Raises:
			RuntimeError: If an error occurs while trying to get the chat history
		"""
		try:
			messages = self.history_collection.find()
		except Exception as e:
			raise RuntimeError(f'An error occurred while trying to get the chat history: {e}')

		# Format the messages in the desired 'role: content' format
		formatted_messages = [f"{message['role']}: {message['content']}" for message in messages]

		return formatted_messages

	def get_user_history(self) -> list:
		"""
		Get the chat history from the database
		Returns:
			formatted_messages (list): A list of strings containing the chat history in the format 'role: content'
		Raises:
			RuntimeError: If an error occurs while trying to get the chat history
		"""
		try:
			messages = self.history_collection.find()
		except Exception as e:
			raise RuntimeError(f'An error occurred while trying to get the chat history: {e}')

		formatted_messages = [f"{message['content'].replace('Rephrased question:', '')}" for message in messages
							  if message['role'] == 'user']
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
			RuntimeError: If an error occurs while trying to update the chat history
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
			raise RuntimeError(f'An error occurred while trying to update the chat history: {e}')

		return result

	def reset_history(self):
		"""
		Delete all the chat history from the collection
		Raises:
			RuntimeError: If an error occurs while trying to reset the chat history
		"""
		try:
			self.history_collection.delete_many({})
		except Exception as e:
			raise RuntimeError(f'An error occurred while trying to reset the chat history: {e}')

	def search(self, query_vector: list, n: int = 3) -> list:
		"""
		Use MongoDB's Atlas vector search to find the most similar embeddings to the query vector
		Args:
			query_vector (list): A list containing the query vector
			n (int): The number of most similar embeddings to return
		Returns:
			results (list): A list dicts containing the most similar items according to the cosine similarity
		Raises:
			RuntimeError: If an error occurs while trying to search for similar embeddings
		"""
		if not self.exact_search:
			# the parameter 'numCandidates' should be passed only for approximate search
			vector_search_config = {
				'exact': self.exact_search,
				'index': f'{self.org_id}_index',
				'limit': n,
				'numCandidates': n * 20,  # according to the documentation, should be 10-20 times the limit
				'path': 'embedding',
				'queryVector': query_vector,
			}
		else:
			vector_search_config = {
				'exact': self.exact_search,
				'index': f'{self.org_id}_index',
				'limit': n,
				'path': 'embedding',
				'queryVector': query_vector,
			}
		pipeline = [
			{
				'$vectorSearch': vector_search_config
			},
			{
				'$project': {
					'_id': 1,
					'text': 1,
					'embedding': 1,
					'score': {
						'$meta': 'vectorSearchScore'
					}
				}
			}
		]

		try:
			results = self.embeddings_collection.aggregate(pipeline)
		except Exception as e:
			raise RuntimeError(f'An error occurred while trying to search for similar embeddings: {e}')

		results_to_return = []
		for result in results:
			readable_result = {
				'text': result['text'],
				'embedding': result['embedding'],
				'score': result['score'],
				'_id': result['_id'],
			}
			results_to_return.append(readable_result)

		return results_to_return

	def __repr__(self):
		return f'DBHandler(org_id={self.org_id}, user_id={self.user_id})'
