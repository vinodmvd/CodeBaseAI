import os

from openai import OpenAI

openai_api = os.getenv("open_api")
llm = OpenAI(api_key = openai_api )