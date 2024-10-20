from pipeline.Chatbot import Chatbot
from sklearn.metrics.pairwise import cosine_similarity
from bert_score import score
import pandas as pd
import spacy


class Evaluator:
    def __init__(self, user_id, llm_model_name, embedding_model_name):
        self.chatbot = Chatbot(user_id, llm_model_name, embedding_model_name)
        self.nlp = spacy.load("en_core_web_sm")

    def evaluate(self, ground_truth_data):
        results = pd.DataFrame(columns=['question', 'true_answer', 'chatbot_answer', 'cosine_similarity',
                                        'bert_score', 'correctness_score', 'faithfulness_score'])
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

    def get_bert_score(self, true_answer, chatbot_answer):
        P, R, F1 = score([chatbot_answer], [true_answer], lang="en", verbose=False)
        return {
            'precision': P.item(),
            'recall': R.item(),
            'f1': F1.item()
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
            'cosine_similarity': self.get_cosine_similarity(true_answer, chatbot_answer),
            'bert_score': self.get_bert_score(true_answer, chatbot_answer),
            'correctness_score': self.get_correctness_score(true_answer, chatbot_answer),
            'faithfulness_score': self.get_faithfulness_score(question, chatbot_answer)
        }