from services.openai_client import llm

def ask(question, context):

    prompt = f"""
        You are a senior software engineer analyzing a codebase.
        Answer ONLY using the provided context. Cite file names from where you fetched the answers from.
        If you're unsure, say you did not find any relavant contents to the user query

        Context:
        {context}

        Question: {question}
    """

    stream = llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )

    print() 

    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            print(delta.content, end="", flush=True)

    print("\n")