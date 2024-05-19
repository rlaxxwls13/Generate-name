import os
import wandb
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "your key"

client = OpenAI()


def make_abbreviation(word):
    try:
        q = '다음 단어의 약칭을 만들어줘: ' + word

        message = [{"role": "user", "content": q}]
        temperature = 0.5
        max_tokens = 100
        frequency_penalty = 0.2

        response = client.chat.completions.create(
            model="your key",
            messages=message,
            temperature=temperature,
            max_tokens=max_tokens,
            frequency_penalty=frequency_penalty
        )

        changed_word = response.choices[0].message.content
        return changed_word

    except Exception as e:
        return str(e)
