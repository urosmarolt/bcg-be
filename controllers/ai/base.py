from abc import ABC
from abc import abstractmethod
from typing import Dict, Any


class BaseAIController(ABC):
    def __init__(self, config: Dict[str, Any]):
        """ __init__ (must be implemented)"""
        raise NotImplementedError

    def generate_response(
            self,
            user_prompt: str,
            system_prompt: str,
            ignore_defaults_params: bool = False,
            **kwargs
    ) -> str:
        """
        Generate AI response based on the input prompt.

        Args:
            user_prompt: Input text prompt
            system_prompt: System prompt
            ignore_defaults_params: Ignore default parameters (all params required by the service must be passed in)
            **kwargs: Service-specific parameters (e.g., temperature, max_tokens)

        Returns:
            Generated text response
            :param user_prompt:
            :param system_prompt:
            :param ignore_defaults_params:
        """
        raise NotImplementedError