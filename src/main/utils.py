from pydantic import BaseModel, Field

class InputQA(BaseModel):
    question: str = Field(..., title='Question to ask the model.')
    id: str = Field(..., title='User session id')

class OutputQA(BaseModel):
    answer: str = Field(..., title='Answer from the model.')

def should_query(input: str):
    keywords = ['nấu', 'nguyên liệu', 'làm']
    for kw in keywords:
        if kw in input.lower():
            return True
    return False