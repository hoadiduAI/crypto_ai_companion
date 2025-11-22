# 🚀 Hướng Dẫn Deploy Telegram Bot Lên Koyeb

## 📋 Tổng Quan

**Koyeb** là dịch vụ hosting miễn phí tốt nhất cho bot Telegram:

### ✅ Ưu điểm:
- 🆓 **Hoàn toàn miễn phí** vĩnh viễn
- 🚫 **KHÔNG cần thẻ tín dụng**
- 🔄 **Auto-deploy** từ GitHub
- ⚡ **Bot chạy 24/7** thực sự
- 🌍 **Global deployment** (Frankfurt, Washington, Singapore)
- 📊 **Logs realtime**
- 💾 **Persistent storage**

### 📊 Free Tier:
- ✅ **2 Web Services** hoặc **1 Worker**
- ✅ **512MB RAM**
- ✅ **2GB disk**
- ✅ **100GB bandwidth/tháng**
- ✅ **Không giới hạn thời gian**

---

## 🎯 Bước 1: Đăng Ký Koyeb

### 1.1. Truy cập Koyeb

1. Mở trình duyệt: **https://app.koyeb.com/auth/signup**
2. Chọn **"Sign up with GitHub"** (dễ nhất!)
3. Authorize Koyeb truy cập GitHub
4. **KHÔNG cần** thêm thẻ tín dụng!

---

## 🎯 Bước 2: Tạo Service Mới

### 2.1. Tạo App

1. Sau khi đăng nhập, click **"Create App"**
2. Chọn **"GitHub"** làm deployment method

### 2.2. Kết Nối GitHub Repository

1. Click **"Connect GitHub account"** (nếu chưa kết nối)
2. Authorize Koyeb
3. Chọn repository **`crypto-radar-bot`**
4. Branch: **`main`**

---

## 🎯 Bước 3: Cấu Hình Deployment

### 3.1. Builder

| Trường | Giá Trị |
|--------|---------|
| **Builder** | `Dockerfile` |
| **Dockerfile path** | `Dockerfile` |

### 3.2. Environment Variables

Click **"Add Variable"** và thêm:

**Variable 1:**
- **Key**: `TELEGRAM_BOT_TOKEN`
- **Value**: Token từ @BotFather (ví dụ: `1234567890:ABCdef...`)
- **Secret**: ✅ Tick vào (để ẩn)

**Variable 2:**
- **Key**: `TELEGRAM_CHAT_ID`
- **Value**: Chat ID từ @userinfobot (ví dụ: `123456789`)
- **Secret**: ❌ Không cần tick

### 3.3. Service Settings

| Trường | Giá Trị |
|--------|---------|
| **Service name** | `crypto-radar-bot` |
| **Service type** | **Worker** (quan trọng!) |
| **Region** | `Frankfurt` (gần VN nhất trong free tier) |
| **Instance type** | `Nano` (512MB RAM - Free) |
| **Scaling** | `1` instance |

### 3.4. Health Checks

- **KHÔNG cần** health checks cho bot Telegram
- Bỏ qua phần này

---

## 🎯 Bước 4: Deploy!

1. Kiểm tra lại tất cả thông tin
2. Click **"Deploy"** ở cuối trang
3. Đợi 2-5 phút để Koyeb build và deploy

---

## 🎯 Bước 5: Kiểm Tra Bot Hoạt Động

### 5.1. Xem Logs

1. Trong Koyeb dashboard, click vào service `crypto-radar-bot`
2. Click tab **"Logs"**
3. Bạn sẽ thấy:
   ```
   Bot started successfully!
   Listening for commands...
   ```

### 5.2. Kiểm Tra Status

- Trong dashboard, status sẽ hiển thị: **"Healthy"** ✅

### 5.3. Test Bot

1. Mở Telegram
2. Tìm bot của bạn
3. Gửi `/start`
4. Bot sẽ trả lời ngay lập tức! 🎉

---

## 🔄 Bước 6: Auto-Deploy (Tự Động)

Từ giờ, **mỗi khi bạn push code mới lên GitHub**, Koyeb sẽ **tự động deploy**!

```bash
# Sau khi sửa code
git add .
git commit -m "Update features"
git push

# Koyeb sẽ tự động deploy trong vài phút
```

---

## 🛠️ Quản Lý Service

### Xem Logs Realtime

1. Dashboard → Service → **Logs**
2. Hoặc click **"Live logs"** để xem realtime

### Restart Service

1. Dashboard → Service → **Settings**
2. Click **"Redeploy"**

### Pause Service

1. Dashboard → Service → **Settings**
2. Click **"Pause"**

### Xóa Service

1. Dashboard → Service → **Settings**
2. Scroll xuống → **"Delete service"**

---

## 📊 Monitoring

### Dashboard

Truy cập: **https://app.koyeb.com**

Bạn sẽ thấy:
- ✅ Service status
- 📊 Metrics (CPU, RAM, Network)
- 📝 Logs
- ⚙️ Settings

### Metrics

Dashboard sẽ hiển thị:
- **CPU usage**
- **Memory usage**
- **Network traffic**
- **Uptime**

---

## 🆘 Xử Lý Lỗi

### ❌ Lỗi: "Build failed"

**Nguyên nhân**: Dockerfile hoặc requirements.txt có lỗi

**Giải pháp**:
1. Xem logs để biết lỗi cụ thể
2. Sửa lỗi trong code
3. Push lên GitHub
4. Koyeb sẽ tự động rebuild

### ❌ Lỗi: "Unhealthy"

**Nguyên nhân**: Bot không chạy được

**Giải pháp**:
1. Kiểm tra logs
2. Kiểm tra `TELEGRAM_BOT_TOKEN` đúng chưa
3. Kiểm tra code có lỗi không

### ❌ Bot không trả lời

**Kiểm tra**:
1. Service status có "Healthy" không?
2. Logs có lỗi gì không?
3. Bot Token đúng chưa?
4. Test token bằng URL:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getMe
   ```

### ❌ Lỗi: "Out of memory"

**Giải pháp**: Bot Telegram rất nhẹ, không nên gặp lỗi này. Nếu gặp:
1. Kiểm tra code có memory leak không
2. Optimize code

---

## 💰 Chi Phí

### Free Tier (Vĩnh Viễn):
- ✅ **1 Worker service**
- ✅ **512MB RAM**
- ✅ **2GB disk**
- ✅ **100GB bandwidth/tháng**
- ✅ **$0/tháng**

**Lưu ý**: Bot Telegram rất nhẹ, **KHÔNG BAO GIỜ** vượt free tier!

---

## 🎯 So Sánh Với Các Dịch Vụ Khác

| Dịch vụ | Miễn phí | Không cần thẻ | Bot 24/7 | Auto-deploy | Dễ dùng |
|---------|----------|---------------|----------|-------------|---------|
| **Koyeb** | ✅ | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| Fly.io | ✅ | ❌ | ✅ | ✅ | ⭐⭐⭐⭐ |
| Railway | $5 credit | ❌ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| Render | ❌ ($7) | ❌ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| PythonAnywhere | ✅ | ✅ | ❌ | ❌ | ⭐⭐⭐ |

---

## 🎉 Hoàn Thành!

Bot của bạn đã chạy 24/7 trên Koyeb hoàn toàn miễn phí! 🚀

### Next Steps:
1. ✅ Monitor logs định kỳ
2. ✅ Thêm tính năng mới cho bot
3. ✅ Tận hưởng bot chạy 24/7 miễn phí!

---

## 📞 Hỗ Trợ

- **Koyeb Docs**: https://www.koyeb.com/docs
- **Koyeb Community**: https://community.koyeb.com
- **Telegram Bot API**: https://core.telegram.org/bots/api
