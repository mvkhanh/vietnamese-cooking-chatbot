from langgraph.graph import MessagesState, StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from src.rag.vector_store import VectorDB
from src.rag.data_loader import Loader
from langgraph.checkpoint.memory import MemorySaver
from langgraph.config import get_stream_writer
from .utils import should_query

class GraphBuilder:
    def __init__(self, llm, data_path, data_type='json'):
        self.graph_builder = StateGraph(MessagesState)
        self.llm = llm
        text_loaded = Loader(data_type).load(data_path)
        self.vector_db = VectorDB(text_loaded)
        
    def query_or_respond(self, state: MessagesState):
        """Decide whether to retrieve documents or respond directly."""
        
        latest_message = state['messages'][-1]
        query = latest_message.content if isinstance(latest_message, HumanMessage) else ''
        if should_query(query):
            retrieved_content = self.vector_db.retrieve(query)
            
            # Store retrieved content as a tool-like message
            tool_message = AIMessage(
                content='',
                additional_kwargs={"tool_call_id": "retrieve_1", "name": "retrieve", "retrieved_content": retrieved_content}
            )
            return  {'messages': state['messages'] + [tool_message]}
        return {'messages': state['messages'] }
            
    def generate(self, state: MessagesState):
        """Generate answer using retrieved documents."""
        # Collect retrieved content from tool messages
        writer = get_stream_writer()
        docs_content = ""
        question = ""
        reverse_messages = list(reversed(state['messages']))
        for i, message in enumerate(reverse_messages):
            if message.type == 'human':
                if i > 0:
                    docs_content = reverse_messages[i - 1].additional_kwargs['retrieved_content']
                question += message.content
                break
            
        conversation_history = []
        while i + 1 < len(reverse_messages) and len(conversation_history) < 2:
            i += 1
            if reverse_messages[i].type == 'ai' and 'tool_call_id' in reverse_messages[i].additional_kwargs:
                continue
            if reverse_messages[i].type == 'human':
                conversation_history.append(f"###Câu hỏi: {reverse_messages[i].content}\n")
            else:
                conversation_history.append(f"###Trả lời: {reverse_messages[i].content}\n")
            
        conversation_history = '\n'.join(conversation_history[::-1]) + '\n'

        # Build prompt in the format expected by PhoGPT-4B-Chat
        system_instruction = "Bạn là một trợ lý ẩm thực chuyên nghiệp. \n"

        if docs_content != "":
            system_instruction += (
                "Sử dụng thông tin dưới đây để trả lời câu hỏi. "
                "Nếu thông tin không đủ hoặc không liên quan, trả lời dựa trên kiến thức ẩm thực thông thường, miễn là đúng. "
                "Nếu không biết, hãy nói là bạn không biết.\n\n"
                f"{docs_content}\n"
            )
        prompt = (
            f"{system_instruction}\n"
            f"{conversation_history}\n"
            f"###Câu hỏi: {question}\n"
            f"###Trả lời:\n"
        )
        
        try:
            response = ''
            for chunk in self.llm.stream(prompt):
                response += chunk
                writer(chunk)
        except Exception as e:
            response = "Xin lỗi, tôi gặp lỗi khi xử lý yêu cầu. Vui lòng thử lại sau."
        
        return {'messages': [AIMessage(content=response)]}
    
    def build_graph(self):
        # Define graph nodes
        self.graph_builder.add_node("query_or_respond", self.query_or_respond)
        self.graph_builder.add_node("generate", self.generate)

        # Define graph edges
        self.graph_builder.set_entry_point("query_or_respond")
        self.graph_builder.add_edge("query_or_respond", "generate")
        self.graph_builder.add_edge("generate", END)

        # Compile the graph
        return self.graph_builder.compile(checkpointer=MemorySaver())
