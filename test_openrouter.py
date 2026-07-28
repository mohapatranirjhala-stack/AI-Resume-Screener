
from utils.openrouter import client

response = client.chat.completions.create(
    model="openai/gpt-oss-20b:free",
    messages=[
        {
            "role": "user",
            "content": "Say Hello"
        }
    ]
)

print(response.choices[0].message.content)