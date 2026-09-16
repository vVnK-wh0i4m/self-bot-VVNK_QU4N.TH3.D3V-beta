<div align="center">

# ⚡ VVNK Bot ⚡

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/Discord.py--self-2.0%2B-purple?logo=discord&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.0.0-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

**Discord Self Bot đa năng với đầy đủ tính năng spam, raid, nhạc, giải trí, quản lý và proxy rotation.**

[📥 **Tải code (.zip)**](https://github.com/vVnK-wh0i4m/self-bot-VVNK_QU4N.TH3.D3V-beta/archive/refs/heads/main.zip) • [📦 **Clone repo**](https://github.com/vVnK-wh0i4m/self-bot-VVNK_QU4N.TH3.D3V-beta.git)

</div>

---

## ⚠️ Cảnh báo quan trọng

> **Self bot vi phạm Discord Terms of Service (ToS).** Sử dụng có thể dẫn đến tài khoản bị **khóa vĩnh viễn**. Hãy sử dụng **tài khoản phụ**, **KHÔNG** dùng tài khoản chính. Tác giả **không chịu trách nhiệm** về bất kỳ hậu quả nào.

---

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt và chạy](#-cài-đặt-và-chạy)
- [Cấu hình](#-cấu-hình)
- [Danh sách lệnh](#-danh-sách-lệnh)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Bản quyền và điều khoản](#-bản-quyền-và-điều-khoản)
- [FAQ](#-câu-hỏi-thường-gặp)

---

## 🌟 Giới thiệu

**VVNK Bot** (v1.0.0) là Discord Self Bot được xây dựng bởi **QU4N.TH3.D3V** với bộ tính năng đa dạng từ spam, raid, nhạc, giải trí cho đến quản lý server. Bot được thiết kế với hệ thống **proxy rotation** tự động giúp tránh rate limit.

**Điểm nổi bật:**
- 🚀 Cài đặt đơn giản chỉ với 1 click `Run.bat`
- 🔄 Tự động restart khi crash
- 🌐 Proxy rotation tự động
- ⚔️ Nuke & Overnuke server
- 🎵 Phát nhạc trong voice
- 🎯 Nitro Sniper tự động

---

## 🚀 Tính năng

### ⚔️ War / Spam

| Tính năng | Mô tả |
|-----------|--------|
| `.spam [delay] [text]` | Spam tùy chỉnh với độ trễ |
| `.nhay [delay]` | Spam từ file nhay.txt |
| `.ngon [delay]` | Spam từ file ngon.txt |
| `.webhook [url] [text]` | Spam qua Webhook |
| `.tokenspam [delay] [text]` | Spam đa token |
| `.nuke [server] [amount]` | Nuke server (xóa + tạo kênh + spam) |
| `.overnuke [server] [amount]` | Overnuke (xả nhay.txt + @everyone) |
| `.bomb` | Xóa toàn bộ kênh |
| `.massreact [số] [emoji]` | Reaction hàng loạt |

### 🎤 Voice Channel

| Tính năng | Mô tả |
|-----------|--------|
| `.vcjoin [id] [M] [D] [C]` | Vào voice channel |
| `.vcleave` | Rời voice |
| `.xanhac [id] [file]` | Phát nhạc trong voice |
| `.tokenvc [id]` | Treo voice đa token |
| `.vcspam [id]` | Spam join/leave voice |
| `.forcedisconnect [@user]` | Ngắt user khỏi voice |

### 🎵 Nhạc

| Tính năng | Mô tả |
|-----------|--------|
| `.xanhac [id] [file]` | Phát file nhạc trong voice |
| Hỗ trợ `.mp3`, `.wav`, `.ogg` | Đặt file vào thư mục `music/` |

### 🎮 Giải trí

| Tính năng | Mô tả |
|-----------|--------|
| `.nsfw [loại]` | NSFW (anal/hanal/4k/gif/pussy/boobs/ass/hboobs/thighs) |
| `.succac` | Hiệu ứng animation |
| `.rainbowrole [@role]` | Role 7 màu |
| `.rizz [@user]` | Random câu tán tỉnh |
| `.roast [@user]` | Random câu roast |
| `.cat` | Ảnh mèo ngẫu nhiên |
| `.phc [@user] [text]` | PornHub comment |

### 🔧 Tiện ích

| Tính năng | Mô tả |
|-----------|--------|
| `.clear [số]` | Xóa tin nhắn |
| `.hackclear` | Xóa chat bằng tin nhắn trống |
| `.avatar [@user]` | Xem avatar |
| `.banner [@user]` | Xem banner |
| `.serverinfo` | Thông tin server |
| `.botinfo` | Thông tin bot |
| `.iplookup [IP]` | Tra cứu IP |
| `.insta [tên]` | Xem Instagram |
| `.math [phép tính]` | Máy tính |
| `.cloneemoji [emoji]` | Sao chép emoji |
| `.clone_channels [id_cũ] [id_mới]` | Sao chép kênh |
| `.clone_roles [id_cũ] [id_mới]` | Sao chép role |
| `.deleteallroles` | Xóa tất cả role |

### 🔄 Trạng thái

| Tính năng | Mô tả |
|-----------|--------|
| `.cyclestatus` | Tự động chuyển status |
| `.setstatus [text]` | Đặt status |
| `.addstatus [text]` | Thêm status vào danh sách |
| `.clearstatus` | Xóa tất cả status |
| `.rpc playing [tên]` | Đang chơi game |
| `.rpc streaming [tên]` | Đang stream |
| `.rpc listening [tên]` | Đang nghe |
| `.rpc watching [tên]` | Đang xem |
| `.stoprpc` | Dừng RPC |

### 🛡️ Quản lý

| Tính năng | Mô tả |
|-----------|--------|
| `.kick [@user]` | Kick thành viên |
| `.ban [@user]` | Ban thành viên |
| `.unban [id]` | Unban |

### 🃏 Troll

| Tính năng | Mô tả |
|-----------|--------|
| `.autoreact on/off` | Bật/tắt tự reaction |
| `.afk [lý_do]` | Bật chế độ AFK |
| `.unafk` | Tắt chế độ AFK |

### 🎯 Auto Features

| Tính năng | Mô tả |
|-----------|--------|
| Nitro Sniper | Tự động claim Nitro gift |
| Proxy Rotation | Tự động xoay proxy |
| Auto Delete | Xóa tin nhắn lệnh sau khi xử lý |
| Auto Reaction | Tự động reaction theo từ khóa |

### 🌐 Proxy System

| Tính năng | Mô tả |
|-----------|--------|
| Load proxy từ file | `config/proxies.txt` |
| Fetch proxy từ API | Tự động lấy proxy miễn phí |
| Auto refresh | Tự động cập nhật proxy mỗi 5 phút |
| Random rotate | Xoay proxy ngẫu nhiên |

---

## 💻 Yêu cầu hệ thống

| Thành phần | Yêu cầu |
|------------|----------|
| Hệ điều hành | Windows 10+, macOS, Linux |
| Python | 3.8 trở lên |
| RAM | Tối thiểu 512MB |
| Ổ cứng | 500MB trống |
| Mạng | Kết nối internet ổn định |
| FFmpeg | Cần thiết cho tính năng phát nhạc |

---

## 📥 Cài đặt và chạy

### Cách 1: Dùng Run.bat (khuyến nghị - Windows)

1. **Tải code:**
   - [📥 Tải file ZIP](https://github.com/vVnK-wh0i4m/self-bot-VVNK_QU4N.TH3.D3V-beta/archive/refs/heads/main.zip)
   - Hoặc clone: `git clone https://github.com/vVnK-wh0i4m/self-bot-VVNK_QU4N.TH3.D3V-beta.git`

2. **Giải nén** thư mục `VVNK_QU4N.TH3.D3V-main`

3. **Double-click** file `Run.bat`

4. **Nhập Discord Token** khi được yêu cầu (sẽ mở Notepad)

5. Bot sẽ tự động:
   - Cài đặt thư viện
   - Tạo thư mục cần thiết
   - Khởi động bot
   - Tự restart khi crash

### Cách 2: Chạy thủ công

```bash
# Clone repo
git clone https://github.com/vVnK-wh0i4m/self-bot-VVNK_QU4N.TH3.D3V-beta.git
cd VVNK_QU4N.TH3.D3V-main

# Cài thư viện
pip install -r requirements.txt

# Tạo thư mục config
mkdir config

# Chạy bot
python bot.py
```

### Cách 3: Dùng index.py (tự động cài + chạy)

```bash
python index.py
```

---

## ⚙️ Cấu hình

### File `config/config.json`

```json
{
    "token": "DISCORD_TOKEN_CỦA_BẠN",
    "prefix": ".",
    "sniper_webhook": "WEBHOOK_URL"
}
```

| Trường | Mô tả |
|--------|-------|
| `token` | Token tài khoản Discord (bắt buộc) |
| `prefix` | Tiền tố lệnh (mặc định: `.`) |
| `sniper_webhook` | Webhook thông báo Nitro (không bắt buộc) |

### File `config/proxies.txt`

Danh sách proxy (mỗi dòng 1 proxy):

```
http://ip:port
socks5://ip:port
```

> Bot sẽ tự động fetch proxy từ API nếu file trống.

### File `cogs/cycstatus.txt`

Danh sách status tự động chuyển (mỗi dòng 1 status):

```
Playing VVNK Bot
discord.gg/vvnk
Đang online 24/7
```

### File `cogs/nhay.txt`

Danh sách tin nhắn nháy (mỗi dòng 1 tin nhắn):

```
DẬY
ALO
DẬY
```

### File `cogs/ngon.txt`

Danh sách tin nhắn ngon (mỗi dòng 1 tin nhắn):

```
Hello
Xin chào
```

### Cách lấy Token Discord

> ⚠️ **CẢNH BÁO:** KHÔNG BAO GIỜ chia sẻ token.

1. Mở Discord trên trình duyệt
2. Nhấn `F12` → Tab **Network**
3. Tìm header `Authorization` → đó là token

---

## 💬 Danh sách lệnh

> Prefix mặc định: `.`

### 🔹 Lệnh chính

| Lệnh | Aliases | Mô tả |
|-------|---------|--------|
| `.menu` | - | Hiển thị menu chính |
| `.botinfo` | - | Thông tin chi tiết bot |
| `.serverinfo` | - | Thông tin server |
| `.shutdown` | - | Tắt bot |
| `.restart` | `.reboot` | Khởi động lại bot |
| `.stop` | - | Dừng tất cả thuật thức đang chạy |

### ⚔️ War / Spam

| Lệnh | Mô tả | Ví dụ |
|-------|-------|-------|
| `.spam [delay] [text]` | Spam tin nhắn | `.spam 2 Hello` |
| `.nhay [delay]` | Spam từ nhay.txt | `.nhay 1.5` |
| `.ngon [delay]` | Spam từ ngon.txt | `.ngon 1` |
| `.webhook [url] [text]` | Spam Webhook | `.webhook https://... Hi` |
| `.tokenspam [delay] [text]` | Spam đa token | `.tokenspam 2 Hello` |
| `.nuke [server] [amount]` | Nuke server | `.nuke 300` |
| `.overnuke [server] [amount]` | Overnuke | `.overnuke 150` |
| `.bomb` | Xóa toàn bộ kênh | `.bomb` |
| `.massreact [số] [emoji]` | Reaction hàng loạt | `.massreact 10 👍` |
| `.clear` | Quét sạch chat | `.clear` |

### 🎤 Voice Channel

| Lệnh | Mô tả | Ví dụ |
|-------|-------|-------|
| `.vcjoin [id] [M] [D] [C]` | Vào voice (Y/N) | `.vcjoin 123456 N N N` |
| `.vcleave` | Rời voice | `.vcleave` |
| `.xanhac [id] [file]` | Phát nhạc | `.xanhac 123456 song.mp3` |
| `.tokenvc [id]` | Treo voice đa token | `.tokenvc 123456` |
| `.vcspam [id]` | Spam join/leave | `.vcspam 123456` |
| `.forcedisconnect [@user]` | Ngắt user khỏi voice | `.forcedisconnect @user` |
| `.stopforcedisconnect` | Dừng forced disconnect | `.stopforcedisconnect` |

> **Ghi chú:** M = Mute, D = Deafen, C = Camera (Y hoặc N)

### 🔄 Trạng thái

| Lệnh | Mô tả | Ví dụ |
|-------|-------|-------|
| `.cyclestatus` | Bật/tắt cycle status | `.cyclestatus` |
| `.setstatus [text]` | Đặt status | `.setstatus Playing VVNK` |
| `.addstatus [text]` | Thêm status | `.addstatus Hello` |
| `.clearstatus` | Xóa tất cả status | `.clearstatus` |
| `.rpc playing [tên]` | Đang chơi game | `.rpc playing Minecraft` |
| `.rpc streaming [tên]` | Đang stream | `.rpc streaming Just Chatting` |
| `.rpc listening [tên]` | Đang nghe | `.rpc listening Spotify` |
| `.rpc watching [tên]` | Đang xem | `.rpc watching YouTube` |
| `.stoprpc` | Dừng RPC | `.stoprpc` |

### 🔧 Tiện ích

| Lệnh | Mô tả | Ví dụ |
|-------|-------|-------|
| `.clear [số]` | Xóa tin nhắn | `.clear 100` |
| `.hackclear` | Xóa chat bằng tin nhắn trống | `.hackclear` |
| `.avatar [@user]` | Xem avatar | `.avatar @user` |
| `.banner [@user]` | Xem banner | `.banner @user` |
| `.iplookup [IP]` | Tra cứu IP | `.iplookup 8.8.8.8` |
| `.insta [tên]` | Xem Instagram | `.insta username` |
| `.math [phép tính]` | Máy tính | `.math 2+2` |
| `.tokencheck [token]` | Kiểm tra token | `.tokencheck abc123` |
| `.checkpromo [link]` | Kiểm tra Nitro promo | `.checkpromo https://...` |
| `.cloneemoji [emoji]` | Clone emoji | `.cloneemoji :smile:` |
| `.clone_channels [id_cũ] [id_mới]` | Clone kênh | `.clone_channels 111 222` |
| `.clone_roles [id_cũ] [id_mới]` | Clone role | `.clone_roles 111 222` |
| `.deleteallroles` | Xóa tất cả role | `.deleteallroles` |
| `.closealldms` | Đóng tất cả DM | `.closealldms` |
| `.delfriends` | Xóa tất cả bạn bè | `.delfriends` |
| `.autoreact on/off` | Auto react | `.autoreact on` |
| `.afk [lý_do]` | Bật AFK | `.afk Đang bận` |
| `.unafk` | Tắt AFK | `.unafk` |

### 🛡️ Quản lý

| Lệnh | Mô tả | Ví dụ |
|-------|-------|-------|
| `.kick [@user]` | Kick | `.kick @user` |
| `.ban [@user]` | Ban | `.ban @user` |
| `.unban [id]` | Unban | `.unban 123456` |

### 🃏 Giải trí

| Lệnh | Mô tả | Ví dụ |
|-------|-------|-------|
| `.nsfw [loại]` | NSFW | `.nsfw anal` |
| `.succac` | Hiệu ứng | `.succac` |
| `.rainbowrole [@role]` | Role 7 màu | `.rainbowrole @Role` |
| `.rizz [@user]` | Tán tỉnh | `.rizz @user` |
| `.roast [@user]` | Chế giễu | `.roast @user` |
| `.cat` | Ảnh mèo | `.cat` |
| `.phc [@user] [text]` | PH Comment | `.phc @user Hello` |

---

## 📁 Cấu trúc dự án

```
VVNK_QU4N.TH3.D3V/
├── bot.py              # Entry point chính
├── index.py            # Script cài đặt + chạy
├── Run.bat             # Launcher tự động (Windows)
├── install.bat         # Cài thư viện
├── install.py          # Script cài tự động
├── config/
│   ├── config.json     # Token + prefix + webhook (gitignore)
│   └── proxies.txt     # Danh sách proxy
├── requirements.txt    # Danh sách thư viện
├── .gitignore
│
├── cogs/
│   ├── cycstatus.txt   # Status tự động chuyển
│   ├── ngon.txt        # Nội dung .ngon
│   └── nhay.txt        # Nội dung .nhay
├── music/              # File nhạc (.mp3, .wav, .ogg)
├── trash/              # Thư mục tạm
└── datoken.txt         # Token phụ (cho tokenspam)
```

---

## 📜 Bản quyền và điều khoản sử dụng

### Giấy phép MIT

```
MIT License

Copyright (c) 2026 vVnK-wh0i4m

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Điều khoản sử dụng

**1. Mục đích sử dụng:**

| ✅ Được phép | ❌ Không được phép |
|-------------|-------------------|
| Giải trí cá nhân | Quấy rối người khác |
| Nghiên cứu, học tập | Spam, gây phiền |
| Thử nghiệm tính năng | Vi phạm pháp luật |
| Quản lý server cá nhân | Gian lận, lừa đảo |

**2. Trách nhiệm người dùng:**

- Người dùng **chịu toàn bộ trách nhiệm** khi sử dụng bot.
- **PHẢI** dùng tài khoản phụ, **KHÔNG** dùng tài khoản chính.
- Người dùng phải **tuân thủ ToS của Discord**.
- Người dùng **tự chịu rủi ro** khi sử dụng self bot.

**3. Hành vi bị cấm:**

- ❌ Sử dụng bot để **quấy rối, spam** người dùng khác.
- ❌ Sử dụng bot để **vi phạm pháp luật** hoặc ToS Discord.
- ❌ **Chia sẻ token** của người dùng khác.
- ❌ Sử dụng bot cho mục đích **gian lận, lừa đảo**.

**4. Giới hạn trách nhiệm:**

- ❌ **Không đảm bảo** bot hoạt động liên tục, không lỗi.
- ❌ **Không chịu trách nhiệm** về mất mát dữ liệu.
- ❌ **Không chịu trách nhiệm** về tài khoản bị khóa.

**5. Bảo mật token:**

> ⚠️ Token cho phép truy cập **hoàn toàn** vào tài khoản Discord.

- **KHÔNG** chia sẻ token với bất kỳ ai.
- **KHÔNG** commit token lên GitHub công khai.
- **Reset ngay** nếu token bị lộ tại https://discord.com/developers/applications

---

## ❓ Câu hỏi thường gặp

### Bot cần Python version nào?

Python 3.8 trở lên. Kiểm tra: `python --version`

### Run.bat không hoạt động?

- Đảm bảo Python đã cài và nằm trong PATH
- Thử chạy thủ công: `pip install -r requirements.txt` rồi `python bot.py`

### Lỗi `No module named 'discord'`?

```bash
pip install discord.py-self
```

> ⚠️ Dùng `discord.py-self`, **KHÔNG** dùng `discord.py` thường.

### Lỗi phát nhạc?

- Cần cài FFmpeg: https://ffmpeg.org/download.html
- Đặt `ffmpeg.exe` vào thư mục `ffmpeg/`

### Bot không hoạt động?

Kiểm tra:
1. Token có hợp lệ không?
2. Bot có trong server không?
3. Terminal có lỗi gì không?

### Bot chạy 24/7 bằng cách nào?

Dùng hosting: Replit, Railway, VPS - xem hướng dẫn tại [self-bot-cam](https://github.com/vVnK-wh0i4m/self-bot-cam)

### Token là gì? Lấy ở đâu?

Token là chuỗi ký tự xác thực bot. Lấy bằng cách:
1. Mở Discord trên trình duyệt
2. Nhấn `F12` → Tab **Network**
3. Tìm header `Authorization`

> ⚠️ **KHÔNG** chia sẻ token. Reset tại https://discord.com/developers/applications

### Bot có an toàn không?

Self bot vi phạm ToS Discord. Sử dụng có thể bị khóa tài khoản. **Luôn dùng tài khoản phụ.**

### Proxy hoạt động như thế nào?

Bot tự động fetch proxy từ nhiều API miễn phí và xoay proxy ngẫu nhiên khi gặp rate limit. Có thể thêm proxy thủ công vào `config/proxies.txt`.

---

<div align="center">

**⭐ Star repo nếu thấy hữu ích! ⭐**

Made with ❤️ by vVnK

</div>
