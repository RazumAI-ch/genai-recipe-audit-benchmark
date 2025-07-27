# File: llms/model_openai.py

import os
import json
import openai

import config.paths
import config.keys
import scripts.utils.utils
import llms.base
from loggers.implementations.benchmark_log_manager import BenchmarkLogFileManager


class OpenAIModel(llms.base.BaseLLM):
    def __init__(self):
        super().__init__(config.paths.PATH_CONFIG_OPENAI)
        self.client = openai.OpenAI(api_key=os.getenv(config.keys.OPENAI_API_KEY_ENV))

    def evaluate(self, records: list[dict]) -> dict:
        self.prepare()

        user_prompt = self.build_full_prompt(records)
        system_prompt = self.system_prompt

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

        log_path = BenchmarkLogFileManager.write_log(model_name=self.model, suffix="response", content=content)
        print(f"Raw response saved to: {log_path}")

        if not content:
            raise ValueError("Empty response from OpenAI.")

        try:
            clean_json = scripts.utils.utils.extract_json_from_text(content)

            if not clean_json.strip().startswith("{") and not clean_json.strip().startswith("["):
                print(f"Cleaned content starts with: {clean_json.strip()[:60]}")
                raise ValueError("Cleaned response is not valid JSON — check for Markdown formatting or truncation.")

            if '"issue%' in clean_json or clean_json.strip().endswith(","):
                print("Possible truncation detected at end of response.")

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
            print("LLM returned invalid JSON. Check saved logs.")
            raise ValueError(f"JSON parsing failed: {e}")