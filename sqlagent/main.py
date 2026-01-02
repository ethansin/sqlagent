import os
from openai import OpenAI
from dotenv import load_dotenv
from jinja2 import Template

load_dotenv()

api_key = os.getenv("OPENAI_KEY")

def sqlagent(request: str, database: str, model: str = "gpt-5-nano-2025-08-07") -> None:

    client = OpenAI(api_key=api_key)

    with open("sqlagent/templates/initial.md", "r") as f:
        initial_message_template = Template(f.read())
    
    initial_message = initial_message_template.render(
        database=database,
        request=request
        )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": initial_message
            }
        ]
    )

    return response.choices[0].message.content

print(sqlagent("please find the number of rows where the amount of slot tags are mismatched with the number of tokens","243hw2.db"))