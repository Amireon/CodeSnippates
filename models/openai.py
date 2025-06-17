import httpx
from dataclasses import dataclass
from os import getenv
from typing import Any, Dict, Optional, Union, Iterator, List

from models.base import Model

try:
    from openai import APIConnectionError, APIStatusError, RateLimitError
    # from openai.types.responses import Response as TextGenerationResponse 
    from openai import AsyncOpenAI as AsyncOpenAIClient
    from openai import OpenAI as OpenAIClient
except (ImportError, ModuleNotFoundError):
    raise ImportError("`openai` not installed. Please install using `pip install openai`")





@dataclass
class OpenAIChat(Model):
    """
    A class for interacting with OpenAI models using the Chat completions API.

    For more information, see: https://platform.openai.com/docs/api-reference/chat/create
    """

    id: str = "gpt-4o"
    name: str = "OpenAIChat"
    provider: str = "OpenAI"
    supports_native_structured_outputs: bool = True

    # Request parameters
    store: Optional[bool] = None
    reasoning_effort: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Any] = None
    logprobs: Optional[bool] = None
    top_logprobs: Optional[int] = None
    max_tokens: Optional[int] = None
    max_completion_tokens: Optional[int] = None
    modalities: Optional[List[str]] = None  # "text" and/or "audio"
    audio: Optional[Dict[str, Any]] = (
        None  # E.g. {"voice": "alloy", "format": "wav"}. `format` must be one of `wav`, `mp3`, `flac`, `opus`, or `pcm16`. `voice` must be one of `ash`, `ballad`, `coral`, `sage`, `verse`, `alloy`, `echo`, and `shimmer`.
    )
    presence_penalty: Optional[float] = None
    seed: Optional[int] = None
    stop: Optional[Union[str, List[str]]] = None
    temperature: Optional[float] = None
    user: Optional[str] = None
    top_p: Optional[float] = None
    request_params: Optional[Dict[str, Any]] = None
    role_map: Optional[Dict[str, str]] = None

    # Client parameters
    api_key: Optional[str] = None
    base_url: Optional[Union[str, httpx.URL]] = None
    timeout: Optional[float] = None
    max_retries: Optional[int] = None
    client_params: Optional[Dict[str, Any]] = None

    # The role to map the message role to.
    default_role_map = {
        "system": "developer",
        "user": "user",
        "assistant": "assistant",
        "tool": "tool",
        "model": "assistant",
    }

    def _get_client_params(self) -> Dict[str, Any]:
        # Fetch API key from env if not already set
        if not self.api_key:
            self.api_key = getenv("OPENAI_API_KEY")
            if not self.api_key:
                print("OPENAI_API_KEY not set. Please set the OPENAI_API_KEY environment variable.")

        # Define base client params
        base_params = {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
        }

        # Create client_params dict with non-None values
        client_params = {k: v for k, v in base_params.items() if v is not None}

        # Add additional client params if provided
        if self.client_params:
            client_params.update(self.client_params)
        return client_params

    def get_client(self) -> OpenAIClient:
        """
        Returns an OpenAI client.

        Returns:
            OpenAIClient: An instance of the OpenAI client.
        """
        client_params: Dict[str, Any] = self._get_client_params()
        if self.http_client is not None:
            client_params["http_client"] = self.http_client
        return OpenAIClient(**client_params)

    def get_async_client(self) -> AsyncOpenAIClient:
        """
        Returns an asynchronous OpenAI client.

        Returns:
            AsyncOpenAIClient: An instance of the asynchronous OpenAI client.
        """
        client_params: Dict[str, Any] = self._get_client_params()
        if self.http_client:
            client_params["http_client"] = self.http_client
        else:
            # Create a new async HTTP client with custom limits
            client_params["http_client"] = httpx.AsyncClient(
                limits=httpx.Limits(max_connections=1000, max_keepalive_connections=100)
            )
        return AsyncOpenAIClient(**client_params)


    def invoke(
        self, 
        input: Union[str, List[Dict[str, str]]],
        instructions: Optional[str] = None,
        mode: int = 0,
        **kwargs
    ) -> Any:

        if not isinstance(input, Union[str, List[Dict[str, str]]]):
            raise ValueError(f"Invalid input: {input}. Expected one of [Str, List[Dict[str, str]]].")

        pass

    def text_generation(
        self, 
        input: Union[str, List[Dict[str, str]]],
        instructions: Optional[str] = None
    ) -> str:
        """
        Generate text from a prompt
        https://platform.openai.com/docs/guides/text?api-mode=responses&lang=python

        Returns:
            Str: The response from API.
        """
        client: OpenAIClient = self.get_client()
        response = client.responses.create(
            mdoel=self.id,
            input=input,
            instructions=instructions,
        )
        text: str = response.output_text
        return text

    def chat_completion(
        self,
        input: Union[str, List[Dict[str, str]]],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        
        client: OpenAIClient = self.get_client()
        messages: List
        
        if isinstance(input, str) and system_prompt and isinstance(system_prompt, str):
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": input
                }
            ]
        else:
            messages = input
            

        completion = client.chat.completions.create(
            model=self.id,
            messages=messages
        )

        text: str = completion.choices[0].message.content

        return text





@dataclass
class OpenAILike(OpenAIChat):
    """
    A class for to interact with any provider using the OpenAI API schema.

    Args:
        id (str): The id of the OpenAI model to use. Defaults to "not-provided".
        api_key (Optional[str]): The API key to use. Defaults to "not-provided".
        base_url (Optional[str]): The Base url to use. Defaults to "not-provided".
        name (str): The name of the OpenAI model to use. Defaults to "OpenAILike".
    """

    id: str = "not-provided" # really used
    name: str = "OpenAILike" # not used
    api_key: Optional[str] = "not-provided"
    # base_url is in OpenAIChat
    # base_url: Optional[str] = "not-provided"

    default_role_map = {
        "system": "system",
        "user": "user",
        "assistant": "assistant",
        "tool": "tool",
    }