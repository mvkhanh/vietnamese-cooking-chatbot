from pydantic import BaseModel, Field

from src.rag.data_loader import Loader
from src.rag.vector_store import VectorDB
from src.rag.offline_rag import Offline_RAG

class InputQA(BaseModel):
    question: str = Field(..., title='Question to ask the model.')

class OutputQA(BaseModel):
    answer: str = Field(..., title='Answer from the model.')
    
def build_rag_chain(llm, data_file, data_type):
    text_loaded = Loader(data_type).load(data_file)
    retriever = VectorDB(texts=text_loaded).get_retriever()
    rag_chain = Offline_RAG(llm).get_chain(retriever)
    return rag_chain