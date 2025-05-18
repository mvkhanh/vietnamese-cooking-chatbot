from typing import Union
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
from .embedding import CustomeEmbedding
import torch
import os

class VectorDB:
    def __init__(self, texts, vector_db: Union[Chroma, FAISS] = Chroma, embedding='dangvantuan/vietnamese-document-embedding'):
        self.vector_db = vector_db
        device = 'mps' if torch.backends.mps.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu'
        self.embedding = CustomeEmbedding(embedding, device)
        self.persist_directory = './chroma_db'
        self.db = self._build_db(texts)
        
    def _build_db(self, texts):
        if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
            print('Load existing Chroma DB')
            db = self.vector_db(persist_directory=self.persist_directory, embedding_function=self.embedding)
        else:
            print('Creating new Chroma DB')
            db = self.vector_db.from_texts(texts, embedding=self.embedding, persist_directory='./chroma_db')
        return db
    
    def retrieve(self, query: str, k=3) -> str:
        """Truy xuất thông tin liên quan đến truy vấn."""
        retrieved_docs = self.db.similarity_search(query, k=k)
        serialized = '\n\n'.join(
            f"{doc.page_content}"
            for doc in retrieved_docs
        )
        return serialized