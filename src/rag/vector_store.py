from typing import Union
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
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
    
    def get_retriever(self, search_type: str='similarity', search_kwargs: dict={'k' : 1}):
        retriever = self.db.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
        return retriever