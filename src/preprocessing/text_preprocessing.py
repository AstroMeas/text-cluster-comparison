import logging
from itertools import chain

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def replace_chars(text, chars_to_replace=None):
    """
    Replaces specified characters in a text using a translation table.
    
    Args:
        text (str): The input text where characters will be replaced.
        chars_to_replace (list of tuples, optional): A list of (original_char, replacement_char) 
                                                   tuples. Defaults to an empty list.
    
    Returns:
        str: The text with characters replaced according to the provided mapping.
    
    Example:
        replace_chars("Hello", [('H', 'h'), ('o', 'O')])
        # Output: 'hellO'
    """
    if chars_to_replace is None:
        chars_to_replace = []
        logger.info('No characters to replace provided.')
    else:
        # Replace characters in the text
        translation_table = str.maketrans(dict(chars_to_replace))
        text = text.translate(translation_table)
    return text


def convert_to_list(text, sep=None):
    """
    Cleans and tokenizes a given text by splitting it based on specified separators.

    Args:
        text (str): The input text to be processed.
        sep (list, optional): A list of separator characters used to split the text. 
                              Defaults to [' ', ',', '.'] if not provided.
       
    Returns:
        list: A list of cleaned and tokenized strings derived from the input text, 
              with empty strings removed.

    Example:
        convert_to_list("Hello, world!", sep=[',', ' '])
        # Output: ['Hello', 'world!']
    """
    # Set default values if parameters were not passed
    if sep is None:
        sep = [' ', ',', '.']  # Example separators
        logger.info(f'No separator given. Standard values used: {sep}')

    logger.debug(f'Using separators: {sep}')
    
    # Split by separators
    result = [text]
    for separator in sep:
        try:
            # Split all previous entries based on the current separator
            result = list(chain.from_iterable(part.split(separator) for part in result))
        except Exception as e:
            logger.warning(f"Error while splitting with separator '{separator}': {str(e)}")
    
    # Remove empty strings and trim whitespace
    result = [item.strip() for item in result if item.strip()]

    return result


def cluster_preprocess(text, sep=None, chars_to_replace=None):
    """
    Preprocesses text for clustering by replacing specified characters and 
    converting to a list of tokens.
    
    Args:
        text (str): The input text to be preprocessed.
        sep (list, optional): A list of separator characters used to split the text.
                              Defaults to None, which will use default separators.
        chars_to_replace (list of tuples, optional): A list of (original_char, replacement_char) 
                                                   tuples. Defaults to None.
    
    Returns:
        list: A list of preprocessed tokens derived from the input text.
    
    Example:
        cluster_preprocess("Hello, world!", sep=[',', ' '], chars_to_replace=[('H', 'h')])
        # Output: ['hello', 'world!']
    """
    # Replace chars, for example wrong letter because of OCR issues
    preprocessed_text = replace_chars(text, chars_to_replace)
    # Convert text to a list
    preprocessed_text = convert_to_list(preprocessed_text, sep)
    return preprocessed_text