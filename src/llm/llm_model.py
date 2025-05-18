from langchain_community.llms import LlamaCpp

def get_llm(model_path: str, n_ctx=2048, max_new_token = 2048, temperature=0.8):
    llm = LlamaCpp(model_path=model_path,
                   n_gpu_layers=-1,
                   n_batch=512,
                   f16_kv=True,
                   n_ctx=n_ctx,
                   max_tokens=max_new_token,
                   temperature=temperature,
                   verbose=False,
                   streaming=True,
                   )
    return llm