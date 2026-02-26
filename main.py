from dotenv import load_dotenv
load_dotenv()

import os

from app.ingest import read_code_files
from app.embed import embed_and_store
from app.chat import ask

def main():

    repo_path = input("Enter path to codebase: ").strip()
    repo_path = os.path.abspath(repo_path)

    print("\nIndexing repository...")
    chunks = read_code_files(repo_path)
    print(f"Total chunks: {len(chunks)}")

    embed_and_store(chunks)
    print("Indexing complete.\n")

    print("You can now ask questions about the codebase.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("> ")
        if question.lower() == "exit":
            break

        answer = ask(question)
        print("\n" + answer + "\n")


if __name__ == "__main__":
    main()