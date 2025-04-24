from dotenv import load_dotenv
import os
from typing import Optional
from .path_manager import PathManager


class EnvError(Exception):
    """
    Custom exception for environment variable-related errors.
    """
    pass


class EnvClient:
    """
    A client to manage environment variables loaded from a .env file.

    Attributes:
        env_path (str): Path to the .env file.
    """

    def __init__(self, env_path: str = PathManager.ROOT/'.env') -> None:
        """
        Initialize the EnvClient and load environment variables from the specified file.

        Args:
            env_path (str): Path to the .env file. Default is '.env'.
        """
        self.env_path: str = env_path
        self.load_env()

    def load_env(self) -> None:
        """
        Load environment variables from the specified .env file.
        """
        load_dotenv(self.env_path)

    def get_username(self) -> str:
        """
        Retrieve the database username from environment variables.

        Returns:
            str: The database username.

        Raises:
            EnvError: If the username is not found in the environment variables.
        """
        username: Optional[str] = os.getenv('DBUSER')
        if not username:
            raise EnvError('Username not found in environment')
        return username

    def get_password(self) -> str:
        """
        Retrieve the database password from environment variables.

        Returns:
            str: The database password.

        Raises:
            EnvError: If the password is not found in the environment variables.
        """
        password: Optional[str] = os.getenv('PASSWORD')
        if not password:
            raise EnvError('Password not found in environment')
        return password

    def get_port(self) -> str:
        """
        Retrieve the database port from environment variables.

        Returns:
            str: The database port.

        Raises:
            EnvError: If the port is not found in the environment variables.
        """
        port: Optional[str] = os.getenv('PORT')
        if not port:
            raise EnvError('Port not found in environment')
        return port

    def get_host(self) -> str:
        """
        Retrieve the database host from environment variables.

        Returns:
            str: The database host.

        Raises:
            EnvError: If the host is not found in the environment variables.
        """
        host: Optional[str] = os.getenv('HOST')
        if not host:
            raise EnvError('Host not found in environment')
        return host

    def get_dbname(self) -> str:
        """
        Retrieve the database name from environment variables.

        Returns:
            str: The database name.

        Raises:
            EnvError: If the database name is not found in the environment variables.
        """
        dbname: Optional[str] = os.getenv('DBNAME')
        if not dbname:
            raise EnvError('DBNAME not found in environment')
        return dbname

    def get_groq_api_key(self) -> str:
        """
        Retrieve the Groq API key from environment variables.

        Returns:
            str: The Groq API key.

        Raises:
            EnvError: If the Groq API key is not found in the environment variables.
        """
        groq_api_key: Optional[str] = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            raise EnvError('GROQ_API_KEY not found in environment')
        return groq_api_key

    def get_base_url(self) -> str:
        """
        Retrieve the base URL for the API from environment variables.

        Returns:
            str: The base URL for the API.

        Raises:
            EnvError: If the base URL is not found in the environment variables.
        """
        base_url: Optional[str] = os.getenv('BASE_URL')
        if not base_url:
            raise EnvError('BASE_URL not found in environment')
        return base_url

    def get_endpoint(self) -> str:
        """
        Retrieve the full API endpoint by combining the base URL and the endpoint path.

        Returns:
            str: The full API endpoint.

        Raises:
            EnvError: If the endpoint path is not found in the environment variables.
        """
        endpoint: Optional[str] = os.getenv('CHAT_ENDPOINT')
        if not endpoint:
            raise EnvError('CHAT_ENDPOINT not found in environment')
        return self.get_base_url() + endpoint
    
    def get_pinecone_api_key(self) -> str:
        """
        Retrieve the Pinecone API key from environment variables.

        Returns:
            str: The Pinecone API key.

        Raises:
            EnvError: If the Pinecone API key is not found in the environment variables.
        """
        pinecone_api_key: Optional[str] = os.getenv('PINECONE_API_KEY')
        if not pinecone_api_key:
            raise EnvError('PINECONE_API_KEY not found in environment')
        return pinecone_api_key


    def autentication_token(self) -> str:
        """
        Retrieve the authentication token from environment variables.

        Returns:
            str: The authentication token.

        Raises:
            EnvError: If the authentication token is not found in the environment variables.
        """
        token: Optional[str] = os.getenv('TOKEN')
        if not token:
            raise EnvError('TOKEN not found in environment')
        return token

if __name__ == '__main__':
    env_client = EnvClient()
    print(env_client.get_username())
    print(env_client.get_password())
    print(env_client.get_port())
    print(env_client.get_host())
    print(env_client.get_dbname())
    print(env_client.get_groq_api_key())
    print(env_client.get_base_url())
    print(env_client.get_endpoint())
    print(env_client.get_pinecone_api_key())
    print(env_client.autentication_token())