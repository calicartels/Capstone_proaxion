import openai
import sys

def get_chat_response(message):
    openai.api_base = "http://localhost:8080/v1"
    openai.api_key = "not-needed"

    response = openai.ChatCompletion.create(
        model="mistral",
        messages=[{"role": "user", "content": message}],
        max_tokens=60
    )

    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    message = sys.argv[1]
    print(get_chat_response(message))
