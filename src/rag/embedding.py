from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer

class CustomeEmbedding(Embeddings):
    def __init__(self, model_name, device='cpu'):
        self.model = SentenceTransformer(model_name, trust_remote_code=True)
        self.model.to(device)
        
    def embed_documents(self, texts):
        return self.model.encode(texts, show_progress_bar=True)
    
    def embed_query(self, text):
        return self.model.encode(text)