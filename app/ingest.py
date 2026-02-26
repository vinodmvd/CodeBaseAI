import os
import re
import json

def split_by_functions(code):
    pattern = r"(def .*?:|class .*?:)"
    splits = re.split(pattern, code)

    chunks = []
    for i in range(1, len(splits), 2):
        header = splits[i]
        body = splits[i+1] if i+1 < len(splits) else ""
        chunks.append(header + body)

    return chunks


def read_code_files(repo_path):
    chunks = []

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    code = f.read()

                parts = split_by_functions(code)
                    
                for p in parts:
                    chunks.append({
                        "text": p,
                        "file": path
                    })

    return chunks