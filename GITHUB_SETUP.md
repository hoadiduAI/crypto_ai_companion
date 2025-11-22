# 🚀 Hướng Dẫn Push Code Lên GitHub

## 📋 Chuẩn Bị

Bạn cần có:
- ✅ Tài khoản GitHub (đã có)
- ✅ Git đã cài đặt (đã có)
- ❓ Username GitHub của bạn
- ❓ Email đã đăng ký GitHub

---

## 🎯 Bước 1: Tạo Repository Trên GitHub

### 1.1. Đăng nhập GitHub
1. Mở trình duyệt, truy cập: **https://github.com**
2. Đăng nhập với tài khoản của bạn

### 1.2. Tạo Repository Mới
1. Click nút **"+"** ở góc trên bên phải
2. Chọn **"New repository"**
3. Điền thông tin:
   - **Repository name**: `crypto-radar-bot` (hoặc tên bạn thích)
   - **Description**: `Telegram bot for crypto market alerts`
   - **Visibility**: Chọn **Public** (bắt buộc cho free tier)
   - **KHÔNG** tick "Add a README file"
   - **KHÔNG** tick "Add .gitignore"
4. Click **"Create repository"**

### 1.3. Copy URL Repository
Sau khi tạo xong, GitHub sẽ hiển thị URL dạng:
```
https://github.com/YOUR_USERNAME/crypto-radar-bot.git
```
**LƯU LẠI URL NÀY** - bạn sẽ cần dùng ở bước sau!

---

## 🎯 Bước 2: Push Code Lên GitHub

### Cách 1: Dùng Git Bash (Khuyến Nghị)

1. **Mở Git Bash**:
   - Vào thư mục `crypto_ai_companion`
   - Click chuột phải vào khoảng trống
   - Chọn **"Git Bash Here"**

2. **Cấu hình Git** (chỉ cần làm 1 lần):
   ```bash
   # Thay YOUR_NAME bằng tên của bạn
   git config --global user.name "Your Name"
   
   # Thay YOUR_EMAIL bằng email GitHub của bạn
   git config --global user.email "your.email@example.com"
   ```

3. **Kiểm tra Git đã hoạt động**:
   ```bash
   git --version
   ```
   Nếu hiện `git version 2.x.x` là OK!

4. **Khởi tạo Git repository**:
   ```bash
   git init
   ```

5. **Thêm tất cả files**:
   ```bash
   git add .
   ```

6. **Commit**:
   ```bash
   git commit -m "Initial commit - Crypto Radar Bot"
   ```

7. **Kết nối với GitHub** (thay YOUR_USERNAME bằng username GitHub của bạn):
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/crypto-radar-bot.git
   ```

8. **Push lên GitHub**:
   ```bash
   git branch -M main
   git push -u origin main
   ```

9. **Nhập thông tin đăng nhập**:
   - Username: username GitHub của bạn
   - Password: **KHÔNG PHẢI** mật khẩu GitHub!
     - Bạn cần tạo **Personal Access Token** (xem bước 2.1 bên dưới)

---

### 2.1. Tạo Personal Access Token (Để Đăng Nhập)

GitHub không cho phép dùng mật khẩu trực tiếp nữa. Bạn cần tạo token:

1. Truy cập: **https://github.com/settings/tokens**
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Điền thông tin:
   - **Note**: `Crypto Radar Bot`
   - **Expiration**: `90 days` (hoặc `No expiration`)
   - **Scopes**: Tick vào **`repo`** (toàn bộ)
4. Click **"Generate token"**
5. **COPY TOKEN NGAY** (chỉ hiện 1 lần!)
   - Token dạng: `ghp_xxxxxxxxxxxxxxxxxxxx`
6. Dùng token này làm **password** khi push code

---

### Cách 2: Dùng GitHub Desktop (Dễ Hơn Cho Người Mới)

Nếu bạn thấy command line khó, có thể dùng GitHub Desktop:

1. **Tải GitHub Desktop**: https://desktop.github.com
2. **Cài đặt** và đăng nhập với tài khoản GitHub
3. **Add repository**:
   - File → Add Local Repository
   - Chọn thư mục `crypto_ai_companion`
4. **Commit**:
   - Tick tất cả files
   - Gõ commit message: "Initial commit"
   - Click "Commit to main"
5. **Publish**:
   - Click "Publish repository"
   - Đặt tên: `crypto-radar-bot`
   - Bỏ tick "Keep this code private"
   - Click "Publish repository"

---

## 🎯 Bước 3: Kiểm Tra Code Đã Lên GitHub

1. Truy cập: `https://github.com/YOUR_USERNAME/crypto-radar-bot`
2. Bạn sẽ thấy tất cả files đã được upload!

---

## 🎯 Bước 4: Deploy Lên Render.com

Sau khi code đã lên GitHub, làm theo hướng dẫn trong file `DEPLOYMENT_GUIDE.md`:

1. Đăng ký Render.com bằng GitHub account
2. Tạo Background Worker
3. Kết nối với repository `crypto-radar-bot`
4. Thêm environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
5. Click Deploy!

---

## 🆘 Xử Lý Lỗi Thường Gặp

### ❌ Lỗi: "git: command not found"
- **Nguyên nhân**: Git chưa được thêm vào PATH
- **Giải pháp**: Dùng Git Bash thay vì PowerShell

### ❌ Lỗi: "Authentication failed"
- **Nguyên nhân**: Dùng mật khẩu thay vì Personal Access Token
- **Giải pháp**: Tạo Personal Access Token (xem bước 2.1)

### ❌ Lỗi: "remote origin already exists"
- **Giải pháp**: Chạy `git remote remove origin` rồi thử lại

### ❌ Lỗi: "fatal: not a git repository"
- **Giải pháp**: Chạy `git init` trước

---

## 📞 Cần Hỗ Trợ?

Nếu gặp vấn đề, hãy:
1. Copy toàn bộ thông báo lỗi
2. Gửi cho tôi để được hỗ trợ chi tiết

---

## 🎉 Hoàn Thành!

Sau khi push code lên GitHub thành công, bạn có thể:
- ✅ Deploy lên Render.com
- ✅ Tự động deploy mỗi khi cập nhật code
- ✅ Backup code an toàn trên cloud
