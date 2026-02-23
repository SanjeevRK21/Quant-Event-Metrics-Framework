# llm/ollama_client.py

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"  # use lightweight model


def call_llm(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.4,
            "top_p": 0.9,
            "num_predict": 600
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=1800
        )
        return response.json()["response"]
    except Exception as e:
        return f"[LLM Error: {str(e)}]"
