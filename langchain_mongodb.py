from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAI, OpenAIEmbeddings

from pymongo import MongoClient
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from bson import ObjectId

import os
from dotenv import load_dotenv

load_dotenv()


def create_vdb(db_constants, paths, org_id, workspace_id, embeddings_engine='openai'):
    """
    this should be splitted into sub-functions and placed in DBHandler.py
    """
    # connect to the database and create a collection
    OPENAI_API_KEY = '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'
    client = MongoClient(db_constants['connection_string'])
    db = client[db_constants['db']]
    embeddings_collection = db[f'{org_id}_{workspace_id}_vdb']

    # split the document in to chunks
    path = '../docs'
    documents = []
    if not paths:
        print('paths is empty, trying to load all files in docs folder')
        for file_name in os.listdir(path):
            print(f'file: {file_name}')
            doc = TextLoader(f'{path}/{file_name}').load()
            documents += doc
    else:
        for file_name in paths:
            print(f'file: {file_name}')
            doc = TextLoader(file_name).load()
            documents += doc

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    data = text_splitter.split_documents(documents)

    if embeddings_engine == 'openai':
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    else:
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-pro", google_api_key=OPENAI_API_KEY)

    # Generate embeddings for the documents and create the collection
    vectorStore = MongoDBAtlasVectorSearch.from_documents(data, embeddings, collection=embeddings_collection)
    retriever = vectorStore.as_retriever()

    return retriever


def create_chatbot(db_constants, org_id, workspace_id, llm_engine='openai', embeddings_engine='openai'):
    """
    this should be splitted into sub-functions and placed in DBHandler.py
    """
    OPENAI_API_KEY = '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'
    if llm_engine == 'openai':
        llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    else:
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv('GOOGLE_API_KEY'))

    if embeddings_engine == 'openai':
        embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    else:
        embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-pro", google_api_key=os.getenv('GOOGLE_API_KEY'))

    # creating vector search based on a collection
    vector_search = MongoDBAtlasVectorSearch.from_connection_string(
        db_constants['connection_string'],
        db_constants['db'] + "." + f'{org_id}_{workspace_id}_vdb',
        embeddings_model,
        index_name=db_constants['atlas_vector_search_index_name'],
    )

    qa_retriever = vector_search.as_retriever(search_type="similarity", search_kwargs={"k": 1}, )
    prompt_template = """
                    Use the following pieces of context to answer the question at the end. 
                    If you don't know the answer, just say that you don't know, don't try to make up an answer.

                    {context}

                    Question: {question}
                    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=qa_retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
    )
    return qa


def rephrase_question(chat_history, question, llm_engine='openai'):
    """
    i placed it in helpers.py
    """
    OPENAI_API_KEY = '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'
    prompt = """
            Given a chat history and the latest user question which might reference context in the chat history,
            formulate a standalone question which can be understood without the chat history.
            Do NOT answer the question, just reformulate it if needed and otherwise return it as is.
            """

    rephrase_question_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )

    if llm_engine == 'openai':
        llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    else:
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv('GOOGLE_API_KEY'))

    rephrase_question_chain = rephrase_question_prompt | llm | StrOutputParser()
    response = rephrase_question_chain.invoke({"chat_history": chat_history, "question": question})
    return response


def get_or_create_chat_history(db_constants, org_id, workspace_id):
    """
    moved to DBHandler.py
    """
    client = MongoClient(db_constants['connection_string'])
    chat_histories = client[db_constants['db']][db_constants['histories_collection']]
    history = chat_histories.find_one({'_id': f'{org_id}_{workspace_id}_chat_history'})
    if history:
        return history.get('chat_history', [])
    else:
        chat_histories.insert_one({'_id': f'{org_id}_{workspace_id}_chat_history', 'chat_history': []})
        return []


def update_chat_history(db_constants, org_id, workspace_id, chat_history):
    """
    moved to DBHandler.py
    """
    client = MongoClient(db_constants['connection_string'])
    chat_histories = client[db_constants['db']][db_constants['histories_collection']]

    filter_query = {'_id': f'{org_id}_{workspace_id}_chat_history'}
    update_query = {'$set': {'chat_history': chat_history}}
    chat_histories.update_one(filter_query, update_query)


def interact(qa, question, db_constants, org_id, workspace_id):
    """
    moved to DBHandler.py
    """
    chat_history = get_or_create_chat_history(db_constants, org_id, workspace_id)

    standalone_question = rephrase_question(chat_history, question)
    chat_history.append(f"User: {standalone_question}")
    response = qa.invoke({"query": standalone_question})["result"]
    chat_history.append(f"Chatbot: {response}")

    return response, chat_history


def reset_chat_history(db_constants, org_id, workspace_id):
    """
    moved to DBHandler.py
    """
    client = MongoClient(db_constants['connection_string'])
    chat_histories = client[db_constants['db']][db_constants['histories_collection']]
    chat_histories.update_one({'_id': f'{org_id}_{workspace_id}_chat_history'}, {'$set': {'chat_history': []}})

