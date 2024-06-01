import re
import json

def clean_text(text):
    """
    Clean the input text by removing extra whitespaces, tabs, newlines, and non-ASCII characters.
    
    Args:
        text (str): Input text to be cleaned.
    
    Returns:
        str: Cleaned text.
    """
    cleaned_text = re.sub(r'\s+', ' ', text)  # Remove extra whitespaces, tabs, and newlines
    cleaned_text = cleaned_text.encode('ascii', 'ignore').decode()  # Remove non-ASCII characters
    return cleaned_text.strip()

def extract_json(text):
    """
    Extract JSON format from the input text.
    
    Args:
        text (str): Input text containing JSON-like substrings.
    
    Returns:
        list: List of JSON objects extracted from the text.
    """
    json_strings = re.findall(r'\{(?:[^{}]|(?R))*\}', text)  # Find JSON-like substrings using regular expression
    extracted_json = []
    for json_string in json_strings:
        try:
            extracted_json.append(json.loads(json_string))  # Try to load each JSON-like substring
        except json.JSONDecodeError:
            pass
    return extracted_json
