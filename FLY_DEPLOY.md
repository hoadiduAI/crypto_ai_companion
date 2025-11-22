# 🚀 Hướng Dẫn Deploy Telegram Bot Lên Fly.io

## 📋 Tổng Quan

**Fly.io** là lựa chọn tốt nhất để host bot Telegram miễn phí:

### ✅ Ưu điểm:
- 🆓 **Hoàn toàn miễn phí** (3 VMs shared-cpu-1x)
- 🌍 **Global deployment** (chọn Singapore gần VN)
- 🔄 **Auto-deploy** từ GitHub (với GitHub Actions)
- 📊 **Logs realtime**
- 💾 **Persistent storage** (volumes)
- ⚡ **Bot chạy 24/7** thực sự

### 📊 Free Tier Limits:
- ✅ **3 shared-cpu-1x VMs** (256MB RAM mỗi VM)
- ✅ **160GB bandwidth/tháng**
- ✅ **3GB persistent storage**
- ✅ **Không cần credit card** (nhưng khuyến nghị thêm để tránh bị giới hạn)

---

## 🎯 Bước 1: Cài Đặt Fly CLI

### Windows:

Mở **PowerShell** và chạy:

```powershell
# Cài đặt Fly CLI
iwr https://fly.io/install.ps1 -useb | iex
```

Sau khi cài xong, **đóng và mở lại PowerShell** để Fly CLI có hiệu lực.

### Kiểm tra cài đặt:

```powershell
fly version
```

Nếu hiện version (ví dụ: `0.x.xxx`) là thành công!

---

## 🎯 Bước 2: Đăng Ký & Đăng Nhập Fly.io

### 2.1. Đăng ký tài khoản

```powershell
fly auth signup
```

Lệnh này sẽ mở trình duyệt để bạn đăng ký:
1. Chọn **"Sign up with GitHub"** (dễ nhất)
2. Authorize Fly.io
3. Điền thông tin:
   - **Email**: Email của bạn
   - **Phone** (tùy chọn): Số điện thoại (để tăng giới hạn)
   - **Credit card** (tùy chọn): Không bắt buộc nhưng khuyến nghị

### 2.2. Đăng nhập

Nếu đã có tài khoản:

```powershell
fly auth login
```

---

## 🎯 Bước 3: Tạo & Deploy App

### 3.1. Di chuyển vào thư mục project

```powershell
cd c:\Users\nguye\.gemini\antigravity\scratch\crypto_ai_companion
```

### 3.2. Khởi tạo Fly app

```powershell
fly launch --no-deploy
```

Fly CLI sẽ hỏi một số câu hỏi:

| Câu hỏi | Trả lời |
|---------|---------|
| **App name** | `crypto-radar-bot` (hoặc tên bạn thích) |
| **Region** | Chọn `sin` (Singapore) |
| **Set up Postgres?** | **No** (chọn `n`) |
| **Set up Redis?** | **No** (chọn `n`) |
| **Deploy now?** | **No** (chọn `n`) - vì cần thêm secrets trước |

Fly sẽ tự động:
- Phát hiện Python app
- Tạo file `fly.toml` (đã có sẵn)
- Tạo `Dockerfile` (đã có sẵn)

### 3.3. Thêm Environment Variables (Secrets)

Thêm Bot Token và Chat ID:

```powershell
# Thêm Bot Token (thay YOUR_BOT_TOKEN)
fly secrets set TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN

# Thêm Chat ID (thay YOUR_CHAT_ID)
fly secrets set TELEGRAM_CHAT_ID=YOUR_CHAT_ID
```

**Cách lấy thông tin:**
- **Bot Token**: Telegram → `@BotFather` → `/mybots` → chọn bot → API Token
- **Chat ID**: Telegram → `@userinfobot` → `/start` → copy số ID

### 3.4. Deploy!

```powershell
fly deploy
```

Quá trình deploy sẽ:
1. Build Docker image
2. Push lên Fly.io registry
3. Deploy container
4. Start bot

Đợi 2-5 phút...

---

## 🎯 Bước 4: Kiểm Tra Bot Hoạt Động

### 4.1. Xem logs

```powershell
fly logs
```

Bạn sẽ thấy:
```
Bot started successfully!
Listening for commands...
```

### 4.2. Kiểm tra status

```powershell
fly status
```

Nếu thấy `Status: running` → **Thành công!** 🎉

### 4.3. Test bot trên Telegram

1. Mở Telegram
2. Tìm bot của bạn
3. Gửi `/start`
4. Bot sẽ trả lời ngay lập tức!

---

## 🔄 Bước 5: Cập Nhật Code (Sau Này)

### Cách 1: Deploy thủ công

Sau khi sửa code và push lên GitHub:

```powershell
# Pull code mới từ GitHub
git pull

# Deploy lại
fly deploy
```

### Cách 2: Auto-deploy với GitHub Actions (Khuyến Nghị)

Tạo file `.github/workflows/fly-deploy.yml`:

```yaml
name: Deploy to Fly.io

on:
  push:
    branches:
      - main

jobs:
  deploy:
    name: Deploy app
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

Sau đó thêm Fly API token vào GitHub Secrets:

```powershell
# Lấy API token
fly auth token

# Copy token và thêm vào GitHub:
# GitHub repo → Settings → Secrets → New repository secret
# Name: FLY_API_TOKEN
# Value: <paste token>
```

Từ giờ, **mỗi khi push code lên GitHub**, bot sẽ tự động deploy! 🚀

---

## 🛠️ Các Lệnh Hữu Ích

### Xem logs realtime
```powershell
fly logs -f
```

### Restart app
```powershell
fly apps restart crypto-radar-bot
```

### SSH vào container
```powershell
fly ssh console
```

### Xem thông tin app
```powershell
fly info
```

### Scale app (thay đổi resources)
```powershell
# Scale lên 512MB RAM (vẫn free)
fly scale memory 512

# Scale về 256MB
fly scale memory 256
```

### Xem danh sách apps
```powershell
fly apps list
```

### Xóa app
```powershell
fly apps destroy crypto-radar-bot
```

---

## 🔒 Quản Lý Secrets

### Xem danh sách secrets
```powershell
fly secrets list
```

### Thêm secret mới
```powershell
fly secrets set KEY=VALUE
```

### Xóa secret
```powershell
fly secrets unset KEY
```

---

## 📊 Monitoring

### Dashboard Web

Truy cập: **https://fly.io/dashboard**

Bạn sẽ thấy:
- ✅ App status
- 📊 Metrics (CPU, RAM, Network)
- 📝 Logs
- ⚙️ Settings

### Metrics

```powershell
fly metrics
```

---

## 🆘 Xử Lý Lỗi

### ❌ Lỗi: "fly: command not found"
- **Nguyên nhân**: Chưa cài Fly CLI hoặc chưa restart PowerShell
- **Giải pháp**: Đóng và mở lại PowerShell

### ❌ Lỗi: "Could not find App"
- **Nguyên nhân**: Chưa chạy `fly launch`
- **Giải pháp**: Chạy `fly launch --no-deploy`

### ❌ Lỗi: "Error: failed to fetch an image"
- **Nguyên nhân**: Dockerfile có lỗi
- **Giải pháp**: Kiểm tra `Dockerfile` và `requirements.txt`

### ❌ Bot không trả lời
- Kiểm tra logs: `fly logs`
- Kiểm tra secrets: `fly secrets list`
- Kiểm tra app status: `fly status`

### ❌ Lỗi: "Out of memory"
- **Giải pháp**: Scale lên 512MB: `fly scale memory 512`

---

## 💰 Chi Phí

### Free Tier (Đủ Cho Bot Telegram):
- ✅ **3 shared-cpu-1x VMs** (256MB RAM)
- ✅ **160GB bandwidth/tháng**
- ✅ **$0/tháng**

### Nếu Vượt Free Tier:
- **shared-cpu-1x**: $1.94/tháng (256MB RAM)
- **Bandwidth**: $0.02/GB sau 160GB

**Lưu ý**: Bot Telegram rất nhẹ, sẽ **KHÔNG vượt** free tier!

---

## 🎯 So Sánh Với Các Dịch Vụ Khác

| Dịch vụ | Miễn phí | Bot 24/7 | Auto-deploy | Dễ dùng |
|---------|----------|----------|-------------|---------|
| **Fly.io** | ✅ | ✅ | ✅ | ⭐⭐⭐⭐ |
| Railway | $5 credit | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| Render | ❌ ($7) | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| PythonAnywhere | ✅ | ❌ | ❌ | ⭐⭐⭐ |

---

## 🎉 Hoàn Thành!

Bot của bạn đã chạy 24/7 trên Fly.io hoàn toàn miễn phí! 🚀

### Next Steps:
1. ✅ Setup GitHub Actions để auto-deploy
2. ✅ Monitor logs định kỳ
3. ✅ Thêm tính năng mới cho bot

---

## 📞 Hỗ Trợ

- **Fly.io Docs**: https://fly.io/docs
- **Fly.io Community**: https://community.fly.io
- **Telegram Bot API**: https://core.telegram.org/bots/api
