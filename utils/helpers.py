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
            return ('When responding, simplify complex concepts into easy-to-understand language.'
                    'Use analogies and relatable examples, keeping explanations brief and straightforward.'
                    'Avoid discussing rough topics, such as genitals or abortion,'
                    'that may not be suitable for a child’s understanding.')
        elif style == 'elderly':
            return ('When addressing questions from elderly users, adopt a formal and respectful tone.'
                    'Provide clear, concise explanations to ensure understanding, especially for complex topics.'
                    'Use phrases like Let me clarify this for you or It\'s important to know that...'
                    'to guide them through the information.')
        elif style == 'emoji':
            return ('When responding to younger users, adopt a friendly and engaging tone and use Emojis.'
                    'Use clear explanations while incorporating some light slang to create a relatable vibe.'
                    'Include emojis after certain words where appropriate.'
                    'For example, use 🍔 for food, 🏥 for healthcare, 💡 for ideas, and 🧑‍⚕️ for doctors.')
        elif style == 'rhymes':
            return ('When responding, use rhymes to make the conversation fun and engaging.'
                    'Create playful and light-hearted responses to keep the user entertained.'
                    'Use simple rhyming words to make the conversation easy to follow and enjoyable.')

