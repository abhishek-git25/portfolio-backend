import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from core.exceptions import OpenAIAPIError, ConfigurationError

load_dotenv()

SYSTEM_PROMPT = "You are Abhishek Yadav's AI assistant. Answer only based on his experience and projects."

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ConfigurationError("AI service configuration error")

    return OpenAI(api_key=api_key)




def generate_reply(message: str) -> str:
    try:
        client = get_openai_client()

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            max_output_tokens=150
        )

        return response.output_text.strip()

    except Exception as e:
        print(f"Unexpected Error: {type(e).__name__}: {str(e)}")
        raise OpenAIAPIError("Failed to generate response")