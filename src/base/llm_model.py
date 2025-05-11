from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

def get_llm(model_path: str, max_new_token = 2048):
    llm = LlamaCpp(model_path=model_path,
                   n_gpu_layers=1,
                   n_batch=512,
                   f16_kv=True,
                   n_ctx=2048,
                   max_tokens=max_new_token,
                   temperature=0.8,
                   )
    return llm