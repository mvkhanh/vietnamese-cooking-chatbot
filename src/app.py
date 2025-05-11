# uvicorn src.app:app --host "0.0.0.0" --port 5000 --reload 
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langserve import add_routes

from src.base.llm_model import get_llm
from src.rag.main import build_rag_chain, InputQA, OutputQA

llm = get_llm('model/PhoGPT-4B-Chat.gguf')
data_path = 'data_source/recipes.json'

# --------- Chains ----------------
chain = build_rag_chain(llm, data_path, data_type='json')

# --------- App - FastAPI ----------------
app = FastAPI(
    title='Cooking chatbot',
    version='1.0',
    description='A simple cooking assistant',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['*'],
)

# --------- Routes - FastAPI ----------------
@app.get('/check')
async def check():
    return {'status': 'OK'}

@app.post('/generative_ai', response_model=OutputQA)
async def generative_ai(inputs: InputQA):
    answer = chain.invoke(inputs.question)
    return {'answer': answer}

# --------- Langserve Routes - Playground ----------------
add_routes(app, chain, playground_type='default', path='/cooking_chatbot')
