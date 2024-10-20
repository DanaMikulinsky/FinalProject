from pipeline.Chatbot import Chatbot
from pipeline.DBHandler import DBHandler
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import spacy

import os
from dotenv import load_dotenv
load_dotenv()

from cohere import Client
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np


class Evaluator:
    def __init__(self, db_handler: DBHandler):
        self.chatbot = Chatbot(db_handler)
        self.nlp = spacy.load("en_core_web_sm")
        self.cohere_client = Client(os.getenv('COHERE_API_KEY'))

    def evaluate(self, ground_truth_data):
        results = pd.DataFrame(columns=['question', 'true_answer', 'chatbot_answer', 'cosine_similarity',
                                        'correctness_score', 'faithfulness_score', 'retriever_scores'])
        for question, true_answer in ground_truth_data:
            chatbot_answer = self.chatbot.answer_question(question)
            result = self.compare_answers(question, true_answer, chatbot_answer)
            result['question'] = question
            result['true_answer'] = true_answer
            result['chatbot_answer'] = chatbot_answer
            enrty_to_add = pd.DataFrame([result])
            results = pd.concat([results, enrty_to_add], ignore_index=True)
        return results

    def get_correctness_score(self, true_answer, chatbot_answer):
        # Semantic similarity (already implemented)
        cosine_sim = self.get_cosine_similarity(true_answer, chatbot_answer)

        # Keyword matching
        true_keywords = set(self.nlp(true_answer).noun_chunks)
        chatbot_keywords = set(self.nlp(chatbot_answer).noun_chunks)
        keyword_overlap = len(true_keywords.intersection(chatbot_keywords)) / len(true_keywords)

        # Named Entity Recognition
        true_entities = set([ent.text for ent in self.nlp(true_answer).ents])
        chatbot_entities = set([ent.text for ent in self.nlp(chatbot_answer).ents])
        entity_overlap = len(true_entities.intersection(chatbot_entities)) / len(
            true_entities) if true_entities else 1.0

        # Combine scores (you can adjust weights)
        correctness_score = (cosine_sim + keyword_overlap + entity_overlap) / 3
        return correctness_score

    def get_cosine_similarity(self, true_answer, chatbot_answer):
        true_embedding = self.chatbot.google_embedding(true_answer)
        chatbot_embedding = self.chatbot.google_embedding(chatbot_answer)
        return cosine_similarity([true_embedding], [chatbot_embedding])[0][0]

    def get_retriever_score(self, question, true_answer):
        """
        iterate over all chunks in the db, and mark the chunk that were retrieved by the retriever.
        prompt cohere to grade each chunk as relevant or not.
        precision - how many of the retrieved chunks are relevant
        recall - how many of the relevant chunks were retrieved
        f1 - harmonic mean of precision and recall
        """
        retrieved_chunks = [chunk['text'] for chunk in self.chatbot.get_relevant_chunks(question)]
        embeddings_collection = self.chatbot.db_handler.embeddings_collection.find()
        all_chunks = [chunk['text'] for chunk in embeddings_collection]

        #TODO: finish this!

        return {
            'precision': precision,
            'recall': recall,
            'f1': f1
        }

    def get_faithfulness_score(self, question, chatbot_answer):
        # Retrieve the context used for answering
        context = self.chatbot.get_relevant_context(question)

        # Compare chatbot's answer with the context
        context_embedding = self.chatbot.google_embedding(context)
        answer_embedding = self.chatbot.google_embedding(chatbot_answer)

        faithfulness_score = cosine_similarity([context_embedding], [answer_embedding])[0][0]
        return faithfulness_score

    def compare_answers(self, question, true_answer, chatbot_answer):
        return {
            'retriever_scores': self.get_retriever_score(question, true_answer),
            'cosine_similarity': self.get_cosine_similarity(true_answer, chatbot_answer),
            'correctness_score': self.get_correctness_score(true_answer, chatbot_answer),
            'faithfulness_score': self.get_faithfulness_score(question, chatbot_answer)
        }