import spacy
from typing import List

def split_text(text: str) -> List[str]:
    """
    Splits a given text into sentences using spaCy's NLP model.

    Parameters:
    -----------
    text : str
        The input text to be split into sentences.

    Returns:
    --------
    List[str]
        A list of extracted sentences, with leading and trailing spaces removed.

    Notes:
    ------
    - If the input text is empty or contains only whitespace, an empty list is returned.
    - If no sentences are extracted, a message is printed.
    """
    if not text.strip():
        print("Empty text provided for segmentation.")
        return []

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    if not sentences:
        print("No sentences were extracted.")

    return sentences