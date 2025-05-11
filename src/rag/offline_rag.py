from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
class Offline_RAG:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = PromptTemplate(
            input_variables=["context", "user_request"],
            template = """Bạn là một trợ lý ẩm thực thông minh, thân thiện. Nhiệm vụ của bạn là giúp người dùng:
- Gợi ý món ăn từ nguyên liệu họ có: dựa trên nguyên liệu và tài liệu tìm được, gợi ý tên các món kèm mô tả ngắn gọn từng món.
- Hướng dẫn nấu ăn theo công thức: hướng dẫn rõ ràng từng bước kèm nguyên liệu cần chuẩn bị.
- Gợi ý thay thế nguyên liệu: chỉ ra các nguyên liệu cần thay thế để giúp món ăn ngon hơn.
- Tư vấn theo chế độ ăn: gợi ý các món ăn phù hợp với chế độ ăn của người dùng.
- Tính toán khẩu phần ăn phù hợp: dựa trên khẩu phần ăn người dùng cung cấp, tính toán số lượng nguyên liệu phù hợp.

Trả lời câu hỏi dựa trên qui định trên, không cần trả lời thông tin thừa.

Bạn **phải sử dụng các công thức nấu ăn trong dữ liệu sau** để trả lời. Nếu cần, bạn có thể suy luận thêm dựa trên kiến thức nấu ăn thông thường, nhưng **ưu tiên thông tin trong tài liệu trước**.

---

Dữ liệu công thức nấu ăn liên quan:
{context}

---

### Yêu cầu người dùng: {user_request}

### Trả lời:
"""
        )
        
    def get_chain(self, retreiver):
        input_data = {
            'context': retreiver | self.format_recipes,
            'user_request': RunnablePassthrough()
        }
        rag_chain = (
            input_data
            | self.prompt
            | self.llm
        )
        return rag_chain
    
    def format_recipes(self, recipes):
        return '\n\n'.join(recipe.page_content for recipe in recipes)