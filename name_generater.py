import os
import wandb
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "your key"

client = OpenAI()


def generate_name(word):
    try:

        q = word

        message = [{"role": "user", "content": q}]
        temperature = 0.5
        max_tokens = 50
        frequency_penalty = 0.5

        response = client.chat.completions.create(
            model="your key",
            messages=message,
            temperature=temperature,
            max_tokens=max_tokens,
            frequency_penalty=frequency_penalty
        )

        generated_text = response.choices[0].message.content

        return generated_text

    except Exception as e:
        return str(e)
