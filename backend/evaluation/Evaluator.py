from backend.pipeline.Chatbot import Chatbot
from backend.pipeline.DBHandler import DBHandler
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import spacy
import warnings
import time
import os

from dotenv import load_dotenv
load_dotenv()

import torch



class Evaluator:
    def __init__(self, db_handler: DBHandler, style: str = '', llm_model_name: str = 'gemini-1.5-flash', embedding_model_name:str = 'models/text-embedding-004'):
        self.chatbot = Chatbot(db_handler, style=style, llm_model_name=llm_model_name, embedding_model_name=embedding_model_name)
        self.nlp = spacy.load("en_core_web_sm")

    def evaluate(self, ground_truth_data):
        results = pd.DataFrame(columns=['question', 'true_answer', 'chatbot_answer', 'cosine_similarity',
                                        'correctness_score', 'faithfulness_score',
                                        #'retriever_scores',
                                        'precision', 'recall', 'f1'
                                        ])
        for question, true_answer, rel_chunks_ids in ground_truth_data:
            chatbot_answer = self.chatbot.answer_question(question)
            result = self.compare_answers(question, true_answer, chatbot_answer, rel_chunks_ids)
            result['question'] = question
            result['true_answer'] = true_answer
            result['chatbot_answer'] = chatbot_answer
            enrty_to_add = pd.DataFrame([result])
            warnings.simplefilter(action='ignore', category=FutureWarning)
            results = pd.concat([results, enrty_to_add], ignore_index=True)
            time.sleep(5)
            self.chatbot.db_handler.reset_history()
        return results

    def get_correctness_score(self, true_answer, chatbot_answer):
        try:
            torch.cuda.empty_cache()
            os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

            # Semantic similarity (already implemented)
            with torch.no_grad():
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
        except Exception as e:
            print(f'Error in get_correctness_score: {e} for {true_answer}')
            return 0

    def get_cosine_similarity(self, true_answer, chatbot_answer):
        true_embedding = self.chatbot.embedding(true_answer)
        chatbot_embedding = self.chatbot.embedding(chatbot_answer)
        return cosine_similarity([true_embedding], [chatbot_embedding])[0][0]

    def get_retriever_score(self, question, relevant_chunks_id) -> dict:
        """
        compare the retrieved chunks with the relevant chunks to estimate the retriever's performance
        Args:
            question (str): The question from the ground truth data
            relevant_chunks_id (list): The relevant chunks id from the ground truth data
        Returns:
            Precision (float): how many of the retrieved chunks are relevant
            Recall (float): how many of the relevant chunks were retrieved
            F1 (float): harmonic mean of precision and recall
        """
        retrieved_chunks_id = [str(chunk['_id']) for chunk in self.chatbot.get_relevant_chunks(question)]

        # Calculate precision, recall, f1
        true_positives = len(set(retrieved_chunks_id).intersection(relevant_chunks_id))
        false_positives = len(set(retrieved_chunks_id).difference(relevant_chunks_id))
        false_negatives = len(set(relevant_chunks_id).difference(retrieved_chunks_id))

        precision = true_positives / (true_positives + false_positives) if true_positives + false_positives > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

        return {
            'precision': round(precision, 5),
            'recall': round(recall, 5),
            'f1': round(f1, 5)
        }

    def get_faithfulness_score(self, question, chatbot_answer):
        # Retrieve the context used for answering
        context = self.chatbot.get_relevant_context(question)

        # Compare chatbot's answer with the context
        context_embedding = self.chatbot.embedding(context)
        answer_embedding = self.chatbot.embedding(chatbot_answer)

        faithfulness_score = cosine_similarity([context_embedding], [answer_embedding])[0][0]
        return faithfulness_score

    def compare_answers(self, question, true_answer, chatbot_answer, rel_chunks_ids):
        retriever_scores_dict = self.get_retriever_score(question, rel_chunks_ids)
        return {
            'precision': retriever_scores_dict['precision'],
            'recall': retriever_scores_dict['recall'],
            'f1': retriever_scores_dict['f1'],
            'cosine_similarity': self.get_cosine_similarity(true_answer, chatbot_answer),
            'correctness_score': self.get_correctness_score(true_answer, chatbot_answer),
            'faithfulness_score': self.get_faithfulness_score(question, chatbot_answer)
        }