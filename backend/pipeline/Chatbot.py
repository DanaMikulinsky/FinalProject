import warnings
from backend.pipeline.DBHandler import DBHandler
from backend.utils.helpers import get_style_instructions
import google.generativeai as genai

import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


class Chatbot:
	# Todo: Support multiple LLMs
	def __init__(self, db_handler: DBHandler, style: str = '', llm_model_name: str = 'gemini-1.5-flash',
				 embedding_model_name: str = 'models/text-embedding-004'):
		"""
		Initializes the Chat object
		Args:
			db_handler (DBHandler): The database handler object
			style (str): The style of the chatbot's answers, chosen from the styles bank
			llm_model_name (str): The name of the model to use
			embedding_model_name (str): the name of the model to use for the embedding, either 'models/text-embedding-004' or 'models/embedding-001'
		Raises:
			ValueError: If the db_handler is not an instance of DBHandler
			ValueError: If the model name is not supported
			RuntimeError: If there was an error initializing the model
		"""

		# Validate the db_handler
		if not isinstance(db_handler, DBHandler):
			raise ValueError('db_handler must be an instance of DBHandler')
		else:
			self.db_handler = db_handler

		# Set the style of the chatbot's answers
		if style == '':
			self.style_instructions = '\n'
		else:
			self.style_instructions = get_style_instructions(style)

		# Initialize the LLM
		possible_models = []
		for option in genai.list_models():
			if 'generateContent' in option.supported_generation_methods:
				possible_models.append(option.name)
		if not llm_model_name and isinstance(llm_model_name, str) and f'models/{llm_model_name}' not in possible_models:
			raise ValueError(f'Model name must be one of the following: {possible_models}')
		try:
			self.llm = genai.GenerativeModel(llm_model_name)
		except Exception as e:
			raise RuntimeError(f'Error initializing model: {e}')

		# Validate the embedding model name
		if not embedding_model_name or embedding_model_name not in ['models/text-embedding-004',
																	'models/embedding-001']:
			raise ValueError('Invalid embedding model name')
		self.embedding_model_name = embedding_model_name

	def interact(self, query: str) -> str:
		"""
		Interacts with the model
		Args:
			query (str): The query to interact with
		Returns:
			str: The response from the model
		"""
		try:
			response = self.llm.generate_content(query)
			return response.text.strip('\n').strip(' ')
		except Exception as e:
			raise RuntimeError(f'Error interacting with model: {e}')

	def rephrase_question(self, query: str, history_length: int = 5) -> str:
		"""
		Rephrases the last user's question as a standalone question
		Args:
			query (str): The user's question
			history_length (int): The number of messages to consider in the chat history
		Returns:
			str: The rephrased question
		Raises:
			ValueError: If the query is not a non-empty string
		"""
		if not query or not isinstance(query, str):
			raise ValueError('Query must be a non-empty string')

		chat_history = self.db_handler.get_history()
		chat_history.append(f'user: {query}')

		# Only use the last 5 messages in the chat history to keep the context relevant
		prompt = f"""
				Your job is to rephrase the last user's question as a standalone question that can be understood without
				the context that is provided in the chat history.
				If the user's question is already standalone, just return it as it is.
				Chat history: {chat_history[-history_length:]}
				"""
		response = self.interact(prompt)
		return response

	def google_embedding(self, text: str) -> list:
		"""
		Embeds the text using the embedding model
		Args:
			text (str): the text to embed
		Returns:
			embedding (list): the embedding vector of the text
		Raises:
			Exception: if there is an error in embedding the text
		"""
		try:
			embedding = genai.embed_content(model=self.embedding_model_name, content=text,
											task_type='retrieval_document')
		except Exception as e:
			raise Exception(f'Error in embedding the text: {e}')

		return embedding['embedding']

	def get_relevant_chunks(self, query: str) -> list:
		"""
		Gets the relevant chunks from the database
		Args:
			query (str): The user's question
			similarity_threshold (float): The similarity threshold to consider a chunk relevant
		Returns:
			relevant_chunks (list): A list of relevant chunks
		"""
		query_vector = self.google_embedding(query)
		return self.db_handler.search(query_vector)

	def get_relevant_context(self, query: str, similarity_threshold: float = 0.3) -> str:
		"""
		Gets the relevant context from the database
		Args:
			query (str): The user's question
			similarity_threshold (float): The similarity threshold to consider a chunk relevant
		Returns:
			str: The relevant context
		"""
		relevant_chunks = self.get_relevant_chunks(query)
		if relevant_chunks:
			# Todo: Improve the logic for selecting the context
			context = '\n\n\n'.join([chunk['text'] for chunk in relevant_chunks if chunk['score'] > similarity_threshold])
		else:
			warnings.warn('No relevant context found in the database')
			context = ''
		return context

	def answer_question(self, query: str) -> str:
		"""
		Run a user's question through the RAG pipeline and return the answer
		Args:
			query (str): The user's question
		Returns:
			str: The answer to the user's question
		"""
		rephrased_query = self.rephrase_question(query)
		context = self.get_relevant_context(rephrased_query)

		# You are a health care provider's assistant. Your job is to answer the user's question based only on
		# the provided context.
		# If you are unable to answer the question based only on the relevant context provided, you can ask for more
		# information or said that you are unable to answer the question. Do not base on any other previous knowledge.
		# When answering questions, respond directly and confidently without mentioning any context or sources.
		# Under no circumstances should you mention, refer to, or indicate that you're answering based on
		# context, context provided, provided information or lack of information in the context.
		# Under no circumstances should you include sentences like "in the context provided" or "based on the information given".

		rag_prompt = f"""
					You are a health care provider's assistant.
					Answer the user's question based solely on the provided information.
					If you can't answer, ask for more details or say you're unable to respond.
					Do not reference context, sources, or previous knowledge in your answer.
					Avoid phrases like "based on the information given" or anything that implies context awareness.			
					User's question: {rephrased_query}
					Context: {context}
					{self.style_instructions}
					"""

		response = self.interact(rag_prompt)

		messages_to_append = [
			{
				'role': 'user',
				'content': rephrased_query
			},
			{
				'role': 'bot',
				'content': response
			}
		]

		self.db_handler.update('history', messages_to_append)

		return response

	def __repr__(self):
		return (f'Chat(org_id={self.db_handler.org_id}, user_id={self.db_handler.user_id}, llm_model_name={self.llm.model_name},'
				f'embedding_model_name={self.embedding_model_name})')

