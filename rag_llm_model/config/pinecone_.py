import numpy as np
from .env_client import EnvClient
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any

class PineconeClient:
    """
    Client for managing interactions with the Pinecone vector database.
    """

    def __init__(self):
        """
        Initializes the Pinecone client, retrieves the API key, and ensures the index exists.
        """
        self.env_client = EnvClient()
        self.pinecone_api_key: str = self.env_client.get_pinecone_api_key()

        self.pinecone = Pinecone(api_key=self.pinecone_api_key)

        self.index_name: str = 'doctorchatbot'
        self.dimension: int = 384

        self._check_index()

    def _check_index(self) -> None:
        """
        Checks if the specified index exists in Pinecone; if not, creates it.
        """
        existing_indexes = self.pinecone.list_indexes().names()
        if self.index_name not in existing_indexes:
            self.pinecone.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
        else:
            print(f"Index '{self.index_name}' already exists.")

    def normalize_embedding(self, embedding: np.array) -> np.array:
        """
        Normalizes an embedding vector to the range [-1, 1].

        Parameters:
        -----------
        embedding : np.array
            The input embedding vector.

        Returns:
        --------
        np.array
            The normalized embedding vector.
        """
        norm = np.linalg.norm(embedding)
        if norm == 0:
            return np.zeros_like(embedding)

        normalized_embedding = embedding / norm  

        normalized_embedding = np.clip(normalized_embedding, -1, 1)

        return normalized_embedding

    def insert_embedding(self, embeddings: np.array, texts: List[str]) -> None:
        """
        Inserts multiple embedding vectors associated with texts into the Pinecone index.

        Parameters:
        -----------
        embeddings : np.array
            A matrix containing text embeddings (each row is a 384-dimensional vector).
        texts : List[str]
            A list of original texts associated with the embeddings.

        Raises:
        -------
        ValueError
            If the number of embeddings does not match the number of texts.
        """
        index = self.pinecone.Index(self.index_name)

        if len(embeddings) != len(texts):
            raise ValueError("The number of embeddings does not match the number of texts.")

        formatted_vectors = []

        for i, (embedding, text) in enumerate(zip(embeddings, texts)):
            normalized_embedding = self.normalize_embedding(embedding)
            formatted_vectors.append({
                "id": str(i + 1),  
                "values": normalized_embedding.tolist(),
                "metadata": {"text": text}
            })

        index.upsert(vectors=formatted_vectors)
        print(f"{len(formatted_vectors)} embeddings successfully inserted.")

    def search_embedding(
        self, 
        embedding: np.array, 
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Performs a similarity search for a given embedding and returns the associated original text.

        Parameters:
        -----------
        embedding : np.array
            Query vector for similarity search.
        top_k : int, optional
            Number of top results to return (default: 5).

        Returns:
        --------
        List[Dict[str, Any]]
            A list of results containing ID, score, and the associated original text.

        Raises:
        -------
        ValueError
            If the index does not exist in Pinecone.
        """
        if self.index_name not in self.pinecone.list_indexes().names():
            raise ValueError(f"The index '{self.index_name}' does not exist in Pinecone.")

        index = self.pinecone.Index(self.index_name)

        normalized_embedding = self.normalize_embedding(embedding)

        response = index.query(
            namespace="",
            vector=normalized_embedding.tolist(),
            top_k=top_k,
            include_metadata=True  
        )

        results = [
            {
                "id": match["id"],
                "score": match["score"],
                "text": match["metadata"]["text"] if "metadata" in match and "text" in match["metadata"] else None
            }
            for match in response["matches"]
        ]

        return results

    def get_next_id(self) -> str:
        """
        Retrieves the highest stored numeric ID and returns the next available value.

        Returns:
        --------
        str
            The next available unique ID.
        """
        index = self.pinecone.Index(self.index_name)

        stats = index.describe_index_stats()
        
        if stats['total_vector_count'] > 0:
            response = index.fetch(ids=[str(i) for i in range(1, stats['total_vector_count'] + 1)])
            
            if response and 'vectors' in response and response['vectors']:
                existing_ids = [int(id) for id in response['vectors'].keys()]
                return str(max(existing_ids) + 1) 
        return '1'
