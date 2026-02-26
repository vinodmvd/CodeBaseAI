from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._model_initializer()
    
    def _model_initializer(self):
        print('Initializing')
        self.model = SentenceTransformer(self.model_name)
        print("Finished Initializing")
        
    def embedding_text(self, text):
        embeddings = self.model.encode(text).tolist()
        return embeddings
    
    
if __name__ == "__main__":
    embedding_model = EmbeddingModel()
    print(embedding_model.embedding_text("Embed me"))