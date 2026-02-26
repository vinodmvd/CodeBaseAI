import os

from openai import OpenAI

from app.retrieve import retrieve

openai_api = os.getenv("open_api")
llm = OpenAI(api_key = openai_api )

def ask(question):
    context = retrieve(question)

    prompt = f"""
        You are a senior software engineer analyzing a codebase.

        Answer ONLY using the provided context.
        Cite file names.
        If unsure, say you did not find any relavant contents to the user query

        Context:
        {context}

        Question: {question}
    """

    resp = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.choices[0].message.content