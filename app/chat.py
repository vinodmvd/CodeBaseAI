from services.openai_client import llm
from app.retrieve import retrieve

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