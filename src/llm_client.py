from abc import ABC, abstractmethod
from typing import Dict, Any
import os
import logging

# Assuming openai is installed and used for DeepSeek
from openai import OpenAI

class BaseLLMClient(ABC):
    """Abstract base class for all LLM clients."""
    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """Generates text based on the given prompt."""
        pass

class DeepSeekLLMClient(BaseLLMClient):
    """LLM client for DeepSeek API, using OpenAI compatibility."""
    def __init__(self, api_key: str, model: str):
        super().__init__(model)
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating text with DeepSeek LLM: {e}")
            return ""

def LLMClientFactory(config: Dict[str, Any]) -> BaseLLMClient:
    """Factory function to create LLM client instances based on configuration."""
    provider = config.get("provider")
    model_id = config.get("modelId")

    if provider == "deepseek":
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set.")
        return DeepSeekLLMClient(api_key=api_key, model=model_id)
    # Add more providers here as needed
    # elif provider == "openai":
    #     api_key = os.environ.get("OPENAI_API_KEY")
    #     if not api_key:
    #         raise ValueError("OPENAI_API_KEY environment variable is not set.")
    #     return OpenAILLMClient(api_key=api_key, model=model_id)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
