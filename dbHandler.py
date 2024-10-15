"""
This module is responsible for handling all database operations.
"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from utils.helpers import rephrase_question

load_dotenv()

class DBHandler:
    def __init__(self):
        self.client = MongoClient(os.environ.get("MONGODB_CONNECTION_STRING"))

    def get_mongo_client(self):
        return self.client['chatbot_db']

    def get_or_create_chat_history(self, db_constants, org_id, workspace_id):
        """
        maybe get rid of the "db_constants" parameter and use the class attribute instead?
        """
        chat_histories = self.client[db_constants['db']][db_constants['histories_collection']]
        history = chat_histories.find_one({'_id': f'{org_id}_{workspace_id}_chat_history'})
        if history:
            return history.get('chat_history', [])
        else:
            chat_histories.insert_one({'_id': f'{org_id}_{workspace_id}_chat_history', 'chat_history': []})
            return []

    def update_chat_history(self, db_constants, org_id, workspace_id, chat_history):
        """
        maybe get rid of the "db_constants" parameter and use the class attribute instead?
        """
        chat_histories = self.client[db_constants['db']][db_constants['histories_collection']]

        filter_query = {'_id': f'{org_id}_{workspace_id}_chat_history'}
        update_query = {'$set': {'chat_history': chat_history}}
        chat_histories.update_one(filter_query, update_query)

    def interact(self, qa, question, db_constants, org_id, workspace_id):
        """
        maybe get rid of the "db_constants" parameter and use the class attribute instead?
        """
        chat_history = self.get_or_create_chat_history(db_constants, org_id, workspace_id)

        standalone_question = rephrase_question(chat_history, question)
        chat_history.append(f"User: {standalone_question}")
        response = qa.invoke({"query": standalone_question})["result"]
        chat_history.append(f"Chatbot: {response}")

        return response, chat_history

    def reset_chat_history(self, db_constants, org_id, workspace_id):
        """
        maybe get rid of the "db_constants" parameter and use the class attribute instead?
        """
        chat_histories = self.client[db_constants['db']][db_constants['histories_collection']]
        chat_histories.update_one({'_id': f'{org_id}_{workspace_id}_chat_history'}, {'$set': {'chat_history': []}})
