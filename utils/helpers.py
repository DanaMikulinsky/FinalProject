
def rephrase_question(chat_history, question, llm_engine='openai'):
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