from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union, Iterator, List


@dataclass
class Model(ABC):
    # ID of the model to use. This is sent to the Model API.
    id: str
    # Name for this Model. This is not sent to the Model API.
    name: Optional[str] = None
    # Provider for this Model. This is not sent to the Model API.
    provider: Optional[str] = None


    # True if the Model supports structured outputs natively (e.g. OpenAI)
    supports_native_structured_outputs: bool = False
    # True if the Model requires a json_schema for structured outputs (e.g. LMStudio)
    supports_json_schema_outputs: bool = False


    # System prompt from the model added to the Agent.
    system_prompt: Optional[str] = "You are a helpful assistant."
    # Instructions from the model added to the Agent.
    instructions: Optional[List[str]] = None


    # The role of the tool message.
    tool_message_role: str = "tool"
    # The role of the assistant message.
    assistant_message_role: str = "assistant"

    def __post_init__(self):
        if self.provider is None and self.name is not None:
            self.provider = f"{self.name} ({self.id})"

    def to_dict(self) -> Dict[str, Any]:
        fields = {"name", "id", "provider"}
        _dict = {field: getattr(self, field) for field in fields if getattr(self, field) is not None}
        return _dict

    def get_provider(self) -> str:
        return self.provider or self.name or self.__class__.__name__

    @abstractmethod
    def invoke(self, *args, **kwargs) -> Any:
        pass

    # @abstractmethod
    # async def ainvoke(self, *args, **kwargs) -> Any:
    #     pass

    # @abstractmethod
    # def invoke_stream(self, *args, **kwargs) -> Iterator[Any]:
    #     pass