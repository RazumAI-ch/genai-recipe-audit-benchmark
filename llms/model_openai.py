# File: llms/model_openai.py

import os
import json
from openai import OpenAI
from llms.base import BaseLLM
from config.paths import PATH_CONFIG_OPENAI
from scripts.utils.logging import save_raw_response
from scripts.utils.utils import extract_json_from_text

class OpenAIModel(BaseLLM):
    def __init__(self):
        super().__init__(PATH_CONFIG_OPENAI)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def evaluate(self, records: list[dict]) -> dict:
        self.prepare()  # Load self.model, self.system_prompt, self.user_prompt

        user_prompt = self.build_full_prompt(records)
        system_prompt = self.system_prompt

        # print("🧾 FINAL USER PROMPT:")
        # print(user_prompt)

        # Send request to OpenAI using 1.x client interface
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            max_tokens=16000,
        )

        raw_content = response.choices[0].message.content or ""
        content = raw_content.strip()

        # Save raw response for traceability
        filename = save_raw_response(content, model_name=self.model)
        print(f"📁 Raw response saved to: {filename}")

        # Handle empty response early
        if not content:
            raise ValueError("❌ Empty response from OpenAI.")

        try:
            clean_json = extract_json_from_text(content)

            # Save cleaned JSON for debugging
            with open("logs/debug/cleaned_gpt4o_response.json", "w", encoding="utf-8") as f:
                f.write(clean_json)

            if not clean_json.strip().startswith("{") and not clean_json.strip().startswith("["):
                print(f"🧪 Cleaned content starts with: {clean_json.strip()[:60]}")
                raise ValueError("❌ Cleaned response is not valid JSON — check for Markdown formatting or truncation.")

            if '"issue%' in clean_json or clean_json.strip().endswith(","):
                print("⚠️ Possible truncation detected at end of response.")

            parsed = json.loads(clean_json)

            if isinstance(parsed, list):
                parsed = {
                    "summary_text": "",
                    "records": parsed
                }

            if "summary_text" not in parsed:
                parsed["summary_text"] = ""

            return parsed

        except Exception as e:
            print("❌ LLM returned invalid JSON. Check saved logs.")
            raise ValueError(f"❌ JSON parsing failed: {e}")