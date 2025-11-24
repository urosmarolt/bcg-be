import json
from typing import Any
from typing import Dict

import boto3

from controllers.ai.base import BaseAIController


class AWSBedrockService(BaseAIController):
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize AWS Bedrock client

        Config Keys:
            region_name: AWS region (i.e. 'eu-west-2')
            model_id: Bedrock model ID (i.e. 'anthropic.claude-3-sonnet-20240229-v1:0')
            aws_access_key_id: AWS access key ID (optional)
            aws_secret_access_key: AWS secret access key (optional)
        """
        client_kwargs = {"region_name": config["region_name"]}

        # Add API key credentials if provided
        if "aws_access_key_id" in config and "aws_secret_access_key" in config:
            client_kwargs["aws_access_key_id"] = config["aws_access_key_id"]
            client_kwargs["aws_secret_access_key"] = config["aws_secret_access_key"]

        self.client = boto3.client("bedrock-runtime", **client_kwargs)
        self.model_id = config["model_id"]

    @staticmethod
    def _default_params(system_prompt: str, user_prompt) -> dict:
        params = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 50000,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": user_prompt}]
                }
            ]
        }
        return params

    def generate_response(
            self,
            user_prompt: str,
            system_prompt: str,
            ignore_defaults_params: bool = False,
            **kwargs
    ) -> str:
        # Use Default parameters initially if not set to ignore.
        # Specific params can be overwritten or added through kwargs
        if ignore_defaults_params:
            params = {}
        else:
            params = self._default_params(system_prompt, user_prompt)

        # Params can be overwritten by the kwargs being passed in
        body = json.dumps({**params, **kwargs})

        # Invoke Bedrock model
        try:
            response = self.client.invoke_model_with_response_stream(
                modelId=self.model_id,
                body=body,
                contentType="application/json"
            )
            stream = response.get('body')
            string_response = ""
            if stream:
                for event in stream:
                    chunk = json.loads(event['chunk']['bytes'])
                    if chunk['type'] == 'content_block_delta':
                        string_response += chunk['delta']['text']
                        print(chunk['delta']['text'], end="", flush=True)
            return string_response

        # TODO: explor more specific Exceptions
        except Exception as e:
            # Handle errors appropriately
            raise RuntimeError(f"Bedrock API error: {str(e)}") from e