# File: benchmark_llms/providers/implementations/openai/provider.py
from typing import Dict, Any, Optional
import requests

from config.keys.keys_llms import YAMLKeys
from config.keys.keys_providers import LLMProviders
from benchmark_llms.providers.abstract_provider import AbstractProvider


class OpenAIProvider(AbstractProvider):
    ENDPOINT_CHAT_COMPLETIONS = "chat/completions"

    def __init__(self, *, model_name: str, model_config: Dict[str, Any]):
        super().__init__(
            provider_key=LLMProviders.OPENAI,  # validated in AbstractProvider.__init__
            model_name=model_name,
            model_config=model_config,
        )

    def send_inference(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: Optional[int],
        temperature: Optional[float],
    ) -> str:
        # Resolve runtime params (prefer explicit args over config defaults)
        effective_temp = (
            temperature
            if temperature is not None
            else self.model_config.get(YAMLKeys.TEMPERATURE)
        )
        effective_max_tokens = (
            max_tokens
            if max_tokens is not None
            else self.model_config.get(YAMLKeys.MAX_TOKENS)
        )

        url = f"{self.base_url}/{self.ENDPOINT_CHAT_COMPLETIONS}"
        payload = {
            YAMLKeys.MODEL: self.endpoint_model_id,  # mapped by AbstractProvider
            YAMLKeys.TEMPERATURE: effective_temp,
            YAMLKeys.MAX_TOKENS: effective_max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt or ""},
                {"role": "user", "content": user_prompt},
            ],
        }

        headers = {"Content-Type": "application/json", **self.build_auth_header()}
        resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout_seconds)
        resp.raise_for_status()
        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Invalid OpenAI API response format: {data}") from e