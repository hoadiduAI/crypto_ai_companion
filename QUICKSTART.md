# Crypto AI Chat - Quick Start Guide

## 🚀 Cách chạy nhanh nhất

### Bước 1: Tạo file `.env`
Tạo file `.env` trong thư mục này với nội dung:
```
GEMINI_API_KEY=your-api-key-here
```

### Bước 2: Chạy backend
**Windows:**
```bash
start_backend.bat
```

**Hoặc thủ công:**
```powershell
$env:GEMINI_API_KEY="your-key"
python ai_chat_api.py
```

### Bước 3: Mở giao diện
Mở file `crypto-ai-chat.html` trong browser

---

## ❌ Nếu gặp lỗi "404 model not found"

Có thể API key của bạn chưa được enable đúng. Thử các bước sau:

### 1. Kiểm tra API key hoạt động
```powershell
python test_gemini_api.py
```

### 2. Tạo API key mới
- Vào: https://aistudio.google.com/app/apikey
- Xóa key cũ
- Tạo key mới trong project mới
- Update vào file `.env`

### 3. Đợi vài phút
API key mới có thể cần 2-3 phút để kích hoạt hoàn toàn

---

## 🔧 Troubleshooting

### Backend không chạy
- Kiểm tra Python đã cài chưa: `python --version`
- Cài dependencies: `pip install -r requirements.txt`

### Frontend không kết nối được
- Kiểm tra backend đang chạy ở port 8000
- Mở http://localhost:8000/health để test

### Lỗi CORS
- Mở file HTML bằng local server:
  ```
  python -m http.server 8080
  ```
- Truy cập: http://localhost:8080/crypto-ai-chat.html

---

## 📞 Support

Nếu vẫn gặp vấn đề, check:
1. API key có đúng không (20+ ký tự, bắt đầu bằng AIza...)
2. Backend console có lỗi gì không
3. Browser console (F12) có lỗi gì không
