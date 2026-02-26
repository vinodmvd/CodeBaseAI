import chromadb

chroma = chromadb.Client()
collection = chroma.get_or_create_collection("codebase")