
import json
import re

def parse_llm_json(text):
    try:
        # Remove markdown code fences if present
        text = re.sub(r"^```json", "", text.strip(), flags=re.IGNORECASE)
        text = re.sub(r"^```", "", text.strip())
        text = re.sub(r"```$", "", text.strip())

        # Extract JSON object
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            text = text[start:end + 1]

        # Remove control characters
        text = re.sub(r"[\x00-\x1F\x7F]", "", text)

        return json.loads(text)

    except Exception:
        return {
            "error": "Invalid JSON returned by LLM",
            "raw_output": text
        }