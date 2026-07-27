from utils.openrouter import ask_ai

messages = [
    {
        "role": "user",
        "content": "Say Hello"
    }
]

reply = ask_ai(
    messages,
    "openai/gpt-oss-20b:free"
)

print(reply)