# File: llms/model_openai.py

import json
from typing import List, Dict
from openai import OpenAI
from llms.proprietary import ProprietaryLLM
from config.paths import OPENAI_CONFIG_PATH


class OpenAIModel(ProprietaryLLM):
    """
    Concrete LLM implementation using OpenAI GPT-4o.
    Loads config from openai.yaml via ProprietaryLLM.
    """

    def __init__(self):
        super().__init__(OPENAI_CONFIG_PATH)

    def prepare(self) -> None:
        super().prepare()
        self.client = OpenAI(api_key=self.api_key)

    def evaluate_batch(self, records: List[Dict]) -> List[Dict]:
        results = []

        for record in records:
            record_id = record["id"]
            content_json = record["content"]

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": f"{self.user_prompt_prefix}\n{json.dumps(content_json)}"}
                    ],
                    temperature=0.0,
                )
                reply = response.choices[0].message.content.strip()
                parsed = json.loads(reply)
                detected_ids = parsed.get("detected_deviation_ids", [])
            except Exception:
                detected_ids = []

            results.append({
                "sample_record_id": record_id,
                "detected_deviation_ids": detected_ids
            })

        return results