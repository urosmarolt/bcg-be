"""Service factory helpers for AI providers (currently AWS Bedrock).

This module exposes small factory functions that construct concrete controller
instances and higher-level prompt managers with sensible defaults for region
and model. Credentials can be provided explicitly or picked up from the
standard AWS provider chain.
"""

from controllers.ai.base import BaseAIController
from controllers.ai.bedrock import AWSBedrockService
from services.prompt.manager import PromptManager as BedrockPromptManager
from services.prompt.economic import EconomicPromptManager

def get_ai_service(provider: str, aws_access_key_id: str = None, aws_secret_access_key: str = None) -> BaseAIController:
    """Create a concrete AI controller for the specified provider.

    Args:
        provider: The AI provider identifier, currently only "bedrock".
        aws_access_key_id: Optional explicit AWS access key ID.
        aws_secret_access_key: Optional explicit AWS secret access key.

    Returns:
        BaseAIController: A controller capable of generating AI responses.

    Raises:
        ValueError: If an unknown provider is requested.
    """
    if provider == "bedrock":
        config = dict(
            region_name="eu-west-2",
            model_id="anthropic.claude-3-7-sonnet-20250219-v1:0",  # 20240229 (3) #20250219 (3-7)
            read_timeout=280,  # Increase read timeout to 280 seconds
            connect_timeout=10  # Optional: time to establish connection
        )

        # Add API key credentials if provided
        if aws_access_key_id and aws_secret_access_key:
            config["aws_access_key_id"] = aws_access_key_id
            config["aws_secret_access_key"] = aws_secret_access_key

        return AWSBedrockService(config=config)
    else:
        raise ValueError("Unknown provider: {}".format(provider))


def bedrock_prompt_service(aws_access_key_id: str = None, aws_secret_access_key: str = None):
    """Construct a PromptManager backed by AWS Bedrock.

    Args:
        aws_access_key_id: Optional explicit AWS access key ID.
        aws_secret_access_key: Optional explicit AWS secret access key.

    Returns:
        PromptManager: High-level helper for prompt-based operations.
    """
    return BedrockPromptManager(get_ai_service("bedrock", aws_access_key_id, aws_secret_access_key))

def bedrock_economic_prompt_service(aws_access_key_id: str = None, aws_secret_access_key: str = None):
    """Construct an EconomicPromptManager backed by AWS Bedrock.

    Args:
        aws_access_key_id: Optional explicit AWS access key ID.
        aws_secret_access_key: Optional explicit AWS secret access key.

    Returns:
        EconomicPromptManager: Helper dedicated to economic case prompts.
    """
    return EconomicPromptManager(get_ai_service("bedrock", aws_access_key_id, aws_secret_access_key))