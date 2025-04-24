import requests
from .. config import EnvClient

class GroqAPIConnectError(Exception):
    """
    Custom exception class for errors during communication with the Groq API.
    """
    pass


class GroqAPIConnect:
    """
    A class to manage communication with the Groq API.

    Attributes:
        model (str): The machine learning model to be used for requests.
        env_path (str): The path to the environment file containing API credentials.
        env_client (EnvClient): An instance of EnvClient to retrieve API details.
        groq_api_key (str): The API key for authentication.
        endpoint (str): The API endpoint URL.
        headers (dict): HTTP headers for API requests.
    """

    def __init__(
            self,
            model: str = 'llama-3.3-70b-versatile',
            env_path: str = '.env'
    ) -> None:
        """
        Initializes the GroqAPIConnect instance.

        Args:
            model (str): The machine learning model to be used (default: 'llama-3.3-70b-versatile').
            env_path (str): Path to the environment file containing API credentials (default: '.env').
        """
        self.env_client: EnvClient = EnvClient(env_path)
        self.model: str = model
        self.groq_api_key: str = self.env_client.get_groq_api_key()
        self.endpoint: str = self.env_client.get_endpoint()
        self.headers: dict[str, str] = {
            'Authorization': f'Bearer {self.groq_api_key}',
            'Content-Type': 'application/json'
        }

    def send_chat(
            self,
            chat: str,
            db_content: str
    ) -> dict:
        """
        Sends a chat message to the Groq API with system instructions to always use database content.

        Args:
            chat (str): The user prompt to send to the API.
            db_content (str): The database content to be provided as system context.

        Returns:
            dict: The JSON response from the API.

        Raises:
            GroqAPIConnectError: If the API response status code is not 200.
        """
        data: dict = {
            'model': self.model,
            'messages': [
                {
                    'role': 'system',
                    'content': (
                        f'You must answer the user\'s questions strictly based on the following data available in the database:\n\n'
                        f'{db_content}\n\n'
                        'If the information is not in the database, respond that no data is available.'
                    )
                },
                {
                    'role': 'user',
                    'content': chat
                }
            ]
        }

        response: requests.Response = requests.post(
            self.endpoint,
            headers=self.headers,
            json=data
        )

        if response.status_code != 200:
            raise GroqAPIConnectError(
                f'Error connecting to Groq API: {response.text}'
            )

        return response.json()


    def __enter__(self) -> 'GroqAPIConnect':
        """
        Context manager entry method.

        Returns:
            GroqAPIConnect: The instance itself for use in a `with` block.
        """
        return self

    def __exit__(
            self,
            exc_type: type,
            exc_val: Exception,
            exc_tb: object
    ) -> None:
        """
        Context manager exit method. Handles exceptions raised within the `with` block.

        Args:
            exc_type (type): The exception type, if any.
            exc_val (Exception): The exception instance, if any.
            exc_tb (object): The traceback object, if any.

        Raises:
            Exception: Re-raises the exception if one occurred.
        """
        if exc_val:
            raise exc_val


if __name__ == '__main__':
    with GroqAPIConnect() as groq_api:
        response: dict = groq_api.send_chat('Explain the importance of fast language models')
        print(response)