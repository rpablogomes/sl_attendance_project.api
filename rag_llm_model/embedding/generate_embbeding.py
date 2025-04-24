from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Union
import numpy as np


class Embedding:
    """
    A class for generating text embeddings using the SentenceTransformer model.
    """

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the embedding model.

        Parameters:
        -----------
        model_name : str, optional
            The name of the pre-trained SentenceTransformer model to be used (default: 'all-MiniLM-L6-v2').
        """
        self.model = SentenceTransformer(model_name)

    def _generate_embedding(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Generates embeddings for the given text(s).

        Parameters:
        -----------
        texts : Union[str, List[str]]
            A single text string or a list of text strings to be embedded.

        Returns:
        --------
        np.ndarray
            The generated embedding(s) as a NumPy array.
        """
        return self.model.encode(texts)

    def get_embedding_shape(self, texts: Union[str, List[str]]) -> Tuple[int, ...]:
        """
        Returns the shape of the generated embedding(s).

        Parameters:
        -----------
        texts : Union[str, List[str]]
            A single text string or a list of text strings.

        Returns:
        --------
        Tuple[int, ...]
            The shape of the generated embedding(s).
        """
        return self._generate_embedding(texts).shape

    def get_embedding(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Returns the generated embedding(s) for the given text(s).

        Parameters:
        -----------
        texts : Union[str, List[str]]
            A single text string or a list of text strings.

        Returns:
        --------
        np.ndarray
            The generated embedding(s).
        """
        return self._generate_embedding(texts)
