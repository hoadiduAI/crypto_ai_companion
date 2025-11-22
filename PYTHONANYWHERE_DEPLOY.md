# 🚀 Hướng Dẫn Deploy Telegram Bot Lên PythonAnywhere

## 📋 Tổng Quan

PythonAnywhere là dịch vụ hosting Python **hoàn toàn miễn phí** với:
- ✅ **Free tier vĩnh viễn** (không cần thẻ tín dụng)
- ✅ **Hỗ trợ Python** native
- ✅ **Web console** để quản lý code
- ⚠️ **Giới hạn**: CPU hạn chế, cần restart thủ công mỗi 3 tháng

---

## 🎯 Bước 1: Đăng Ký Tài Khoản

1. Truy cập: **https://www.pythonanywhere.com/registration/register/beginner/**
2. Điền form đăng ký:
   - **Username**: Chọn username (ví dụ: `nguyen-crypto`)
   - **Email**: Email của bạn
   - **Password**: Mật khẩu mạnh
3. Click **"Register"**
4. Xác nhận email (check hộp thư)
5. Đăng nhập vào PythonAnywhere

---

## 🎯 Bước 2: Clone Code Từ GitHub

### 2.1. Mở Bash Console

1. Sau khi đăng nhập, click vào tab **"Consoles"**
2. Click **"Bash"** để mở terminal
3. Bạn sẽ thấy terminal màu đen

### 2.2. Clone Repository

Trong Bash console, chạy lệnh sau (thay `YOUR_USERNAME`):

```bash
# Clone repository từ GitHub
git clone https://github.com/YOUR_USERNAME/crypto-radar-bot.git

# Di chuyển vào thư mục
cd crypto-radar-bot

# Kiểm tra files
ls -la
```

---

## 🎯 Bước 3: Cài Đặt Dependencies

Trong Bash console, chạy:

```bash
# Cài đặt các thư viện cần thiết
pip3 install --user -r requirements.txt
```

Đợi vài phút để cài đặt hoàn tất.

---

## 🎯 Bước 4: Tạo File .env (Cấu Hình Bot)

### 4.1. Tạo file .env

```bash
# Tạo file .env
nano .env
```

### 4.2. Thêm nội dung vào file

Copy và paste nội dung sau (thay thông tin của bạn):

```env
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE
```

**Cách lấy thông tin:**
- **Bot Token**: Mở Telegram → tìm `@BotFather` → `/mybots` → chọn bot → API Token
- **Chat ID**: Mở Telegram → tìm `@userinfobot` → `/start` → copy số ID

### 4.3. Lưu file

- Nhấn `Ctrl + O` (lưu)
- Nhấn `Enter` (xác nhận tên file)
- Nhấn `Ctrl + X` (thoát)

---

## 🎯 Bước 5: Test Bot Thủ Công

Trước khi chạy tự động, test xem bot hoạt động không:

```bash
python3 alert_bot.py
```

Nếu thấy:
```
Bot started successfully!
Listening for commands...
```

→ **Thành công!** Nhấn `Ctrl + C` để dừng.

---

## 🎯 Bước 6: Chạy Bot 24/7 (Always-On Task)

### ⚠️ **LƯU Ý QUAN TRỌNG:**

PythonAnywhere **free tier KHÔNG hỗ trợ Always-On Tasks**. Bạn có 2 lựa chọn:

### **Lựa Chọn A: Dùng Scheduled Task (Khuyến Nghị)**

Chạy bot định kỳ mỗi giờ (phù hợp cho alert bot):

1. Click tab **"Tasks"**
2. Trong phần **"Scheduled tasks"**, điền:
   - **Time**: `Hourly` (mỗi giờ)
   - **Command**: 
     ```bash
     cd /home/YOUR_USERNAME/crypto-radar-bot && python3 alert_bot.py
     ```
   - Thay `YOUR_USERNAME` bằng username PythonAnywhere của bạn
3. Click **"Create"**

Bot sẽ chạy mỗi giờ để kiểm tra và gửi alerts.

---

### **Lựa Chọn B: Chạy Trong Console (Thủ Công)**

Nếu muốn bot chạy liên tục:

1. Mở **Bash console**
2. Chạy:
   ```bash
   cd crypto-radar-bot
   python3 alert_bot.py
   ```
3. **KHÔNG đóng** tab console

**Nhược điểm**: 
- Phải giữ tab mở
- Nếu đóng tab, bot sẽ dừng
- Console tự động timeout sau vài giờ

---

### **Lựa Chọn C: Upgrade Lên Paid Plan ($5/tháng)**

Nếu cần bot chạy 24/7 thực sự:
- Click **"Account"** → **"Upgrade"**
- Chọn **"Hacker plan"** ($5/tháng)
- Bạn sẽ có **Always-On Task**

---

## 🎯 Bước 7: Kiểm Tra Bot Hoạt Động

1. Mở Telegram
2. Tìm bot của bạn
3. Gửi `/start`
4. Bot sẽ trả lời! 🎉

---

## 🔄 Cập Nhật Code Sau Này

Khi bạn thay đổi code trên GitHub:

```bash
# Mở Bash console
cd crypto-radar-bot

# Pull code mới
git pull

# Restart bot (nếu đang chạy)
# Ctrl + C để dừng, rồi chạy lại:
python3 alert_bot.py
```

---

## 🛠️ Các Lệnh Hữu Ích

### Xem logs
```bash
cd crypto-radar-bot
tail -f nohup.out
```

### Kiểm tra bot có đang chạy không
```bash
ps aux | grep alert_bot
```

### Dừng bot
```bash
pkill -f alert_bot.py
```

---

## ⚠️ Giới Hạn Free Tier

| Tính năng | Giới hạn |
|-----------|----------|
| **CPU time** | 100 seconds/day |
| **Disk space** | 512 MB |
| **Always-On tasks** | ❌ Không có (cần paid) |
| **Scheduled tasks** | ✅ 1 task miễn phí |
| **Console timeout** | 5 phút không hoạt động |

---

## 💡 Khuyến Nghị

Vì bot Telegram cần chạy **liên tục 24/7**, PythonAnywhere free tier **KHÔNG phải lựa chọn tốt nhất**.

### **Nên dùng:**
1. **Railway.app** - $5 credit/tháng (đủ chạy bot)
2. **Fly.io** - Free tier hào phóng hơn
3. **Koyeb** - Free tier tốt

### **Chỉ dùng PythonAnywhere nếu:**
- Bot chỉ cần chạy định kỳ (scheduled task)
- Bạn sẵn sàng trả $5/tháng cho Always-On

---

## 🆘 Xử Lý Lỗi

### ❌ Lỗi: "ModuleNotFoundError"
```bash
pip3 install --user <tên_module>
```

### ❌ Lỗi: "Permission denied"
```bash
chmod +x alert_bot.py
```

### ❌ Bot không trả lời
- Kiểm tra `TELEGRAM_BOT_TOKEN` đúng chưa
- Kiểm tra bot có đang chạy: `ps aux | grep alert_bot`
- Xem logs: `tail -f nohup.out`

---

## 🎉 Hoàn Thành!

Nếu mọi thứ OK, bot của bạn đã chạy trên PythonAnywhere! 

**Lưu ý**: Nhớ restart bot mỗi 3 tháng (PythonAnywhere yêu cầu).
