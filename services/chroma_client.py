import chromadb
from chromadb.config import Settings

chroma = chromadb.PersistentClient(
    path="data/chroma_db",
    settings=Settings(anonymized_telemetry=False)
)
collection = chroma.get_or_create_collection("codebase")