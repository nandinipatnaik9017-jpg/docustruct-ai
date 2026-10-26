
import requests
import time

print("Testing Ollama API...")
start = time.time()

try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3.5:4b",
            "prompt": "Say hello in one short sentence.",
            "stream": False,
            "think": False,
            "options": {
                "num_predict": 40
            }
        },
        timeout=300
    )

    response.raise_for_status()
    result = response.json()

    print("Full API response:", result)
    print("Generated text:", repr(result.get("response")))
    print("Time taken:", round(time.time() - start, 2), "seconds")

except Exception as e:
    print("Error:", e)
