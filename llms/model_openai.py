# File: llms/model_openai.py

import os
import json
import openai
from llms.base import BaseLLM
from config.keys import SYSTEM_PROMPT

class OpenAIModel(BaseLLM):
    def __init__(self):
        super().__init__(model_config={})  # Will be overridden by `prepare()` later
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def evaluate(self, records: list[dict]) -> dict:
        # Load and apply prompt + model config
        self.prepare()

        # Build prompt using shared logic
        user_prompt = self.build_full_prompt(records)
        system_prompt = self.system_prompt

        # Send to OpenAI
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=4096,
            response_format="text"
        )

        response_content = response.choices[0].message.content

        print("🔍 RAW LLM OUTPUT:")
        print(response_content)

        try:
            parsed = json.loads(response_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ LLM call failed: No valid JSON content found in response.\n{e}")

        return parsed