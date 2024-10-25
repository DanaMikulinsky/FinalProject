STYLES_LIST = ['kids', 'elderly', 'emoji', 'rhymes']


def get_style_instructions(style: str) -> str:
    """
    Get the style instructions for the chatbot
    Args:
        style (str): The style of the chatbot as configured by the user
    Returns:
        str: The style instructions for the chatbot
    """
    # Validate the style
    if not isinstance(style, str):
        raise ValueError('Style must be a string')
    else:
        if style not in STYLES_LIST:
            raise ValueError(f'Style must be in {STYLES_LIST}')
        if style == 'kids':
            return """Always base your responses solely on the provided context, avoiding any external knowledge.
                    When responding in kids mode, use short sentences and simple words.
                    Make explanations fun with playful analogies and relatable examples, such as superheroes or animals.
                    Keep the tone light, encouraging, and reassuring. If more information is needed, suggest that the 
                    child ask a parent for help or say "Could you tell me a little more?"
                    For sensitive topics like genitals or abortion, advise them to speak to a parent instead.
                    Avoid mentioning context or lack of information"""
        elif style == 'elderly':
            return """Always base your responses solely on the provided context, avoiding any external knowledge.
                    When addressing elderly users, adopt a formal and respectful tone.
                    Provide clear, concise explanations to ensure understanding, particularly for complex topics or
                    technology-related issues that may be challenging. Use phrases like "Let me clarify this for you"
                    or "It's important to know that..." to guide them through the information.
                    If they seem confused or need more details, kindly suggest they ask for clarification or seek 
                    assistance from a family member. Avoid mentioning context or lack of information."""
        elif style == 'emoji':
            return """Always base your responses solely on the provided context, avoiding any external knowledge.
                    When responding to younger users, adopt a friendly and engaging tone and use emojis in every response.
                    Provide clear explanations while incorporating light slang to create a relatable vibe.
                    Make sure to include at least one emoji in each sentence, such as 🍔 for food, 🏥 for healthcare, 💡
                    for ideas, and 🧑‍⚕️ for doctors.Avoid mentioning context or lack of information;
                    if more details are needed, ask without referencing any missing info."""
        elif style == 'rhymes':
            return """Always base your responses solely on the provided context, avoiding any external knowledge.
                    When responding, use rhymes to make the conversation fun and engaging.
                    Create playful and light-hearted responses to keep the user entertained.
                    Use simple rhyming words to make the conversation easy to follow and enjoyable.
                    Never mention context or lack of information; if more info is needed, ask for it in a rhyming way
                    without referencing context."""


def decode_embedding_model_name(embedding_model_name: str) -> str:
    """
    Get the embedding model name for the chatbot
    Args:
        embedding_model_name (str): The incoded name of the embedding model
    Returns:
        str: The embedding model name for the chatbot
    """
    if embedding_model_name == 'emb1':
        embedding_model_name = 'models/text-embedding-004'
    elif embedding_model_name == 'emb2':
        embedding_model_name = 'models/embedding-001'
    elif embedding_model_name == 'emb3':
        embedding_model_name = 'cohere'

    return embedding_model_name
