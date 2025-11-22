# 🚀 Hướng Dẫn Deploy Crypto Radar Bot lên Render.com

## 📋 Tổng Quan

Hướng dẫn này sẽ giúp bạn deploy Telegram Bot lên **Render.com** - một dịch vụ hosting miễn phí, tự động deploy từ GitHub.

### ✅ Ưu điểm của Render.com:
- ✨ **Hoàn toàn miễn phí** cho background workers
- 🔄 **Auto-deploy** từ GitHub (mỗi lần push code mới)
- 🐍 **Hỗ trợ Python** native
- 🔒 **SSL/HTTPS** miễn phí
- 📊 **Logs** và monitoring tích hợp
- ⚡ **Không cần credit card** cho free tier

---

## 🎯 Bước 1: Chuẩn Bị GitHub Repository

### 1.1. Tạo GitHub Repository (nếu chưa có)

1. Truy cập [github.com](https://github.com) và đăng nhập
2. Click nút **"New"** hoặc **"+"** → **"New repository"**
3. Đặt tên repository: `crypto-radar-bot` (hoặc tên bạn thích)
4. Chọn **Public** (bắt buộc cho free tier của Render)
5. **KHÔNG** chọn "Add a README file" (vì đã có code sẵn)
6. Click **"Create repository"**

### 1.2. Push Code Lên GitHub

Mở **PowerShell** hoặc **Git Bash** trong thư mục project và chạy:

```bash
# Khởi tạo Git (nếu chưa có)
git init

# Thêm tất cả files
git add .

# Commit
git commit -m "Initial commit - Crypto Radar Bot"

# Thêm remote repository (thay YOUR_USERNAME bằng username GitHub của bạn)
git remote add origin https://github.com/YOUR_USERNAME/crypto-radar-bot.git

# Push lên GitHub
git branch -M main
git push -u origin main
```

> ⚠️ **LƯU Ý:** File `.env` đã được ignore trong `.gitignore`, nên **KHÔNG** bị push lên GitHub (bảo mật).

---

## 🎯 Bước 2: Đăng Ký Render.com

1. Truy cập [render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Đăng ký bằng **GitHub account** (khuyến nghị - dễ kết nối)
4. Authorize Render truy cập GitHub repositories của bạn

---

## 🎯 Bước 3: Tạo Web Service trên Render

### 3.1. Tạo Service Mới

1. Sau khi đăng nhập, click **"New +"** → **"Background Worker"**
2. Chọn **"Build and deploy from a Git repository"**
3. Click **"Next"**

### 3.2. Kết Nối Repository

1. Tìm repository `crypto-radar-bot` trong danh sách
2. Click **"Connect"**

### 3.3. Cấu Hình Service

Điền thông tin như sau:

| Trường | Giá Trị |
|--------|---------|
| **Name** | `crypto-radar-bot` (hoặc tên bạn thích) |
| **Region** | `Singapore` (gần Việt Nam nhất) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python alert_bot.py` |
| **Plan** | **Free** (chọn free tier) |

### 3.4. Thêm Environment Variables (Biến Môi Trường)

Scroll xuống phần **"Environment Variables"** và thêm:

1. Click **"Add Environment Variable"**
2. Thêm các biến sau:

| Key | Value | Ghi chú |
|-----|-------|---------|
| `TELEGRAM_BOT_TOKEN` | `YOUR_BOT_TOKEN` | Lấy từ @BotFather |
| `TELEGRAM_CHAT_ID` | `YOUR_CHAT_ID` | Lấy từ @userinfobot |

> 💡 **Cách lấy Bot Token:**
> - Mở Telegram, tìm `@BotFather`
> - Gửi `/newbot` hoặc `/token` để lấy token
> - Copy token dạng: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

> 💡 **Cách lấy Chat ID:**
> - Mở Telegram, tìm `@userinfobot`
> - Gửi `/start`
> - Copy số ID (dạng: `123456789`)

### 3.5. Deploy

1. Click **"Create Web Service"** (hoặc "Deploy")
2. Render sẽ bắt đầu build và deploy
3. Đợi 2-5 phút cho quá trình hoàn tất

---

## 🎯 Bước 4: Kiểm Tra Bot Hoạt Động

### 4.1. Xem Logs

1. Trong Render dashboard, click vào service `crypto-radar-bot`
2. Click tab **"Logs"**
3. Bạn sẽ thấy logs như:
   ```
   Bot started successfully!
   Listening for commands...
   ```

### 4.2. Test Bot trên Telegram

1. Mở Telegram
2. Tìm bot của bạn (tên bạn đã tạo với @BotFather)
3. Gửi `/start`
4. Bot sẽ trả lời nếu hoạt động đúng! 🎉

---

## 🔄 Bước 5: Auto-Deploy (Tự Động Deploy)

Từ giờ, **mỗi khi bạn push code mới lên GitHub**, Render sẽ **tự động deploy** phiên bản mới!

```bash
# Sau khi sửa code
git add .
git commit -m "Update features"
git push

# Render sẽ tự động deploy trong vài phút
```

---

## 🛠️ Các Lệnh Hữu Ích

### Xem Logs Realtime
- Vào Render Dashboard → Service → **Logs**

### Restart Service
- Vào Render Dashboard → Service → **Manual Deploy** → **"Clear build cache & deploy"**

### Suspend Service (Tạm dừng)
- Vào Render Dashboard → Service → **Settings** → **"Suspend Service"**

---

## 📊 Giới Hạn Free Tier của Render

| Tính năng | Giới hạn |
|-----------|----------|
| **Background Workers** | Miễn phí (không giới hạn) |
| **Build time** | 15 phút/build |
| **Bandwidth** | 100 GB/tháng |
| **Uptime** | 99.9% |
| **Auto-deploy** | Unlimited |

> ⚠️ **LƯU Ý:** Background workers trên free tier có thể bị **sleep sau 15 phút không hoạt động**. Để bot luôn chạy, bạn cần upgrade lên **Paid plan ($7/tháng)** hoặc dùng cron job để ping bot định kỳ.

---

## 🎯 Các Dịch Vụ Thay Thế (Nếu Cần)

### 1. **Railway.app**
- ✅ Free $5 credit/tháng
- ✅ Dễ dùng, UI đẹp
- ❌ Cần credit card để verify

### 2. **Fly.io**
- ✅ Free tier hào phóng
- ✅ Nhiều regions
- ❌ Phức tạp hơn cho người mới

### 3. **PythonAnywhere**
- ✅ Chuyên cho Python
- ✅ Có free tier
- ❌ Giới hạn CPU và bandwidth

### 4. **Heroku**
- ❌ **Không còn free tier** (từ 2022)

---

## 🆘 Troubleshooting (Xử Lý Lỗi)

### ❌ Lỗi: "Build failed"
- Kiểm tra `requirements.txt` có đúng format không
- Xem logs để biết package nào bị lỗi

### ❌ Bot không trả lời
- Kiểm tra `TELEGRAM_BOT_TOKEN` đã đúng chưa
- Xem logs trên Render có lỗi gì không
- Test bot token bằng cách gửi request:
  ```
  https://api.telegram.org/bot<YOUR_TOKEN>/getMe
  ```

### ❌ Service bị sleep
- Upgrade lên paid plan ($7/tháng)
- Hoặc dùng cron job để ping bot mỗi 10 phút

---

## 📞 Liên Hệ & Hỗ Trợ

Nếu gặp vấn đề, bạn có thể:
1. Xem logs trên Render Dashboard
2. Kiểm tra [Render Documentation](https://render.com/docs)
3. Hỏi trên [Render Community](https://community.render.com)

---

## 🎉 Hoàn Thành!

Chúc mừng! Bot của bạn đã được deploy thành công và đang chạy 24/7 trên cloud! 🚀

**Next Steps:**
- Thêm tính năng mới
- Monitor logs định kỳ
- Upgrade plan nếu cần uptime 100%
