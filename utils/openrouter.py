from openai import OpenAI
from openai import RateLimitError
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def ask_ai(messages, model):

    try:

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3
        )

        return response.choices[0].message.content

    except RateLimitError:

        return (
            "⚠️ OpenRouter free daily limit has been reached.\n\n"
            "Please switch to another free model, "
            "use another API key, or add credits to OpenRouter."
        )

    except Exception as e:

        return f"Error: {str(e)}"