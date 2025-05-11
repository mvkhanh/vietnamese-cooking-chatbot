# 🇻🇳 Vietnamese Cooking Chatbot

Một chatbot ẩm thực giúp bạn:
- Gợi ý món ăn từ nguyên liệu có sẵn
- Hướng dẫn nấu ăn theo công thức
- Gợi ý thay thế nguyên liệu
- Tư vấn theo chế độ ăn
- Tính toán khẩu phần phù hợp

## 🚀 Cách chạy ứng dụng

### 1. Clone repo
```bash
git clone https://github.com/your-username/vietnamese-cooking-chatbot.git
cd vietnamese-cooking-chatbot
```
### 2. Cài đặt các thư viện cần thiết
pip install -r requirements.txt
### 3. Chạy ứng dụng FastAPI với Uvicorn
uvicorn src.app:app --host "0.0.0.0" --port 5000 --reload