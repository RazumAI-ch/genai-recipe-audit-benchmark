# File: benchmark_llms/providers/implementations/openai/provider.py

from typing import Dict, Any, List, Optional
import requests  # will be used once we wire real HTTP

from config.keys.keys_llms import YAMLKeys, PromptKeys
from config.keys.keys_providers import ProviderYAMLKeys, LLMProviders
from benchmark_llms.providers.abstract_provider import AbstractProvider


class OpenAIProvider(AbstractProvider):
    """
    Provider implementation for OpenAI API access.
    Uses the /v1/chat/completions endpoint.
    """

    # Must match config.keys.keys_providers.LLMProviders
    provider_key = LLMProviders.OPENAI

    # ---- OpenAI-specific field names / endpoints (kept as statics to avoid string literals)
    ENDPOINT_CHAT_COMPLETIONS = "chat/completions"

    FIELD_CHOICES = "choices"
    FIELD_MESSAGE = "message"
    FIELD_CONTENT = "content"
    FIELD_ROLE = "role"

    ROLE_SYSTEM = "system"
    ROLE_USER = "user"

    # -------- InterfaceProvider concretes (make this class non-abstract) --------
    def prepare(self) -> None:
        # Nothing extra to do beyond AbstractProvider.__init__ for now.
        # Keep this so the class is concrete.
        return None

    def infer(
        self,
        records: List[Dict[str, Any]],
        system_prompt: str,
        user_prompt_template: str,
        *,
        model: str,
        temperature: Optional[float],
        max_tokens: Optional[int],
        batch_size: Optional[int],
    ) -> str:
        """
        For now, stub the actual HTTP call and return minimal JSON.
        This keeps MC1 path green; we’ll replace with real transport shortly.
        """
        # Debug print to verify we’re actually being called
        print(
            f"[OpenAIProvider] infer() called with model={model}, "
            f"temp={temperature}, max_tokens={max_tokens}, batch_size={batch_size}, "
            f"records={len(records)}"
        )

        # In the real version, we’d:
        #   - build the prompt per record (using user_prompt_template)
        #   - call self.send_inference(...) for each/batches
        #   - merge results
        # For MC1 bring-up, return minimal valid JSON for downstream.
        return '{"records": []}'

    # -------- Internal helpers used by the real HTTP path (kept ready) --------
    def _resolve_endpoint(self, model_config: Dict[str, Any]) -> str:
        base_url = self.provider_config[ProviderYAMLKeys.BASE_URL]
        return f"{base_url}/{self.ENDPOINT_CHAT_COMPLETIONS}"

    def _build_payload(self, prompt: str, model_config: Dict[str, Any]) -> Dict[str, Any]:
        return {
            YAMLKeys.MODEL: model_config[YAMLKeys.MODEL],
            YAMLKeys.TEMPERATURE: model_config[YAMLKeys.TEMPERATURE],
            YAMLKeys.MAX_TOKENS: model_config[YAMLKeys.MAX_TOKENS],
            "messages": [
                {self.FIELD_ROLE: self.ROLE_SYSTEM, self.FIELD_CONTENT: model_config.get(PromptKeys.SYSTEM_PROMPT, "")},
                {self.FIELD_ROLE: self.ROLE_USER, self.FIELD_CONTENT: prompt},
            ],
        }

    def _parse_response(self, response: requests.Response) -> str:
        data = response.json()
        try:
            return data[self.FIELD_CHOICES][0][self.FIELD_MESSAGE][self.FIELD_CONTENT]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Invalid OpenAI API response format: {data}") from e

    # Optional: when we flip to real HTTP, implement this and have infer() call it.
    def send_inference(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_tokens: Optional[int],
        temperature: Optional[float],
    ) -> str:
        # Placeholder to satisfy the abstract contract if we decide to use it.
        # We’re not invoking it yet; return minimal JSON so pipeline keeps running.
        print("[OpenAIProvider] send_inference() stub called (no HTTP yet).")
        return '{"records": []}'