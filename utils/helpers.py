STYLES_LIST = ['friendly', 'formal', 'neutral']


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
        if style == 'formal':
            return 'write in a formal style'
        elif style == 'friendly':
            return 'write in a friendly style'
        elif style == 'neutral':
            return 'write in a neutral style'

