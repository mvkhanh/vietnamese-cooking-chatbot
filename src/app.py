# uvicorn src.app:app --host "0.0.0.0" --port 5001 --reload 
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from langserve import add_routes

from src.llm.llm_model import get_llm
from src.main.graph_builder import GraphBuilder
from src.main.utils import InputQA, OutputQA
from .template import html

llm = get_llm('model/PhoGPT-4B-Chat.gguf')
data_path = 'data_source/recipes.json'

# --------- Graphs ----------------
graph = GraphBuilder(llm, data_path, data_type='json').build_graph()

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

@app.post('/chatbot', response_model=OutputQA)
async def generative_ai(inputs: InputQA):
    config = {"configurable": {"thread_id": inputs.id}}
    answer = await graph.ainvoke({"messages": [{"role": "user", "content": inputs.question}]}, config=config)['messages'][-1].content
    return {'answer': answer}

# --------- Demo - Websocket ----------------
# Serve the HTML chat interface
@app.get('/')
async def get():
    return HTMLResponse(html)

# WebSocket endpoint for real-time streaming
@app.websocket('/ws/{thread_id}')
async def websocket_endpoint(websocket: WebSocket, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        async for step in graph.astream({"messages": [{"role": "user", "content": data}]}, config=config, stream_mode='custom'):
            await websocket.send_text(step)