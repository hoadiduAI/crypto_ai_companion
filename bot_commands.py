"""
Telegram Bot Command Handlers for Crypto Radar
Handles user interactions: /start, /track, /untrack, /list, /status, /help, /menu
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import user_db
import mm_detector
from datetime import datetime

# ==================== COMMAND HANDLERS ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - Register user and show welcome message"""
    user = update.effective_user
    telegram_id = user.id
    username = user.username
    
    # Register user if not exists
    db_user = user_db.create_user(telegram_id, username)
    
    # Check for deep linking arguments
    args = context.args
    if args and args[0] == 'login':
        # Generate login code immediately
        code = user_db.create_login_code(telegram_id)
        await update.message.reply_text(
            f"🔐 **Mã đăng nhập Web App:**\n\n`{code}`\n\n"
            f"Mã có hiệu lực trong 5 phút. Vui lòng nhập mã này vào trang web Crypto Radar.",
            parse_mode='Markdown'
        )
        return

    if db_user:
        message = f"Chào mừng {username} đến với Crypto Radar! 📡\n\nBạn đã đăng ký thành công với gói **Free** (1 coin miễn phí).\n\nGửi /menu để bắt đầu!"
    else:
        message = f"Chào mừng trở lại, {username}! 📡\n\nGửi /menu để mở bảng điều khiển."

    # Show menu immediately after start
    keyboard = [
        [
            InlineKeyboardButton("🔍 Quét Thị Trường", callback_data='scan_market'),
            InlineKeyboardButton("📋 Danh Sách Của Tôi", callback_data='my_watchlist')
        ],
        [
            InlineKeyboardButton("🔑 Lấy Mã Đăng Nhập", callback_data='get_login_code')
        ],
        [
            InlineKeyboardButton("❓ Hướng Dẫn", callback_data='help')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /menu command - Show interactive panel"""
    keyboard = [
        [
            InlineKeyboardButton("🔍 Quét Thị Trường", callback_data='scan_market'),
            InlineKeyboardButton("📋 Danh Sách Của Tôi", callback_data='my_watchlist')
        ],
        [
            InlineKeyboardButton("🔑 Lấy Mã Đăng Nhập", callback_data='get_login_code')
        ],
        [
            InlineKeyboardButton("❓ Hướng Dẫn", callback_data='help')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📡 **Crypto Radar Control Panel**\n\nChọn tác vụ bên dưới:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    telegram_id = query.from_user.id
    
    if data == 'scan_market':
        await query.edit_message_text("🔍 Đang quét thị trường... Vui lòng đợi giây lát.")
        
        # Fetch data
        try:
            df = mm_detector.fetch_binance_data()
            ghost_towns = mm_detector.detect_ghost_towns(df)
            
            if ghost_towns.empty:
                await query.edit_message_text("✅ Thị trường bình yên. Không phát hiện Ghost Town nào.")
                return

            # Format message
            message = "👻 **Top 5 Ghost Towns (Giá cao - Vol thấp):**\n\n"
            keyboard = []
            
            for _, row in ghost_towns.head(5).iterrows():
                symbol = row['Symbol']
                price = row['Price']
                vol = row['Volume'] / 1_000_000
                
                message += f"• {symbol}: ${price:.4f} (Vol: ${vol:.2f}M)\n"
                
                keyboard.append([InlineKeyboardButton(f"Theo dõi {symbol}", callback_data=f"track_{symbol}")])
            
            keyboard.append([InlineKeyboardButton("🔄 Quét Lại", callback_data='scan_market')])
            keyboard.append([InlineKeyboardButton("🔙 Quay lại Menu", callback_data='main_menu')])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
            
        except Exception as e:
            await query.edit_message_text(f"❌ Lỗi khi quét: {str(e)}")

    elif data == 'my_watchlist':
        coins = user_db.get_tracked_coins(telegram_id)
        
        if not coins:
            keyboard = [[InlineKeyboardButton("🔙 Quay lại Menu", callback_data='main_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("📋 Bạn chưa theo dõi coin nào.", reply_markup=reply_markup)
            return
            
        message = "📋 **Danh sách theo dõi của bạn:**\n\n"
        keyboard = []
        
        for coin in coins:
            symbol = coin['symbol']
            message += f"• {symbol}\n"
            keyboard.append([InlineKeyboardButton(f"❌ Bỏ theo dõi {symbol}", callback_data=f"untrack_{symbol}")])
            
        keyboard.append([InlineKeyboardButton("🔙 Quay lại Menu", callback_data='main_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    elif data == 'get_login_code':
        code = user_db.create_login_code(telegram_id)
        await context.bot.send_message(
            chat_id=telegram_id,
            text=f"🔐 **Mã đăng nhập Web App:**\n\n`{code}`\n\n"
                 f"Mã có hiệu lực trong 5 phút.",
            parse_mode='Markdown'
        )

    elif data == 'help':
        message = """
📚 **Hướng dẫn sử dụng**

• **Quét Thị Trường:** Tìm các coin có dấu hiệu "Ghost Town" (Giá cao, Vol thấp) để theo dõi.
• **Danh Sách:** Quản lý các coin bạn đang theo dõi.
• **Cảnh Báo:** Bot sẽ tự động gửi tin nhắn khi coin trong danh sách có biến động lạ.

Liên hệ: @YourAdminUsername
        """
        keyboard = [[InlineKeyboardButton("🔙 Quay lại Menu", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup)

    elif data == 'main_menu':
        keyboard = [
            [
                InlineKeyboardButton("🔍 Quét Thị Trường", callback_data='scan_market'),
                InlineKeyboardButton("📋 Danh Sách Của Tôi", callback_data='my_watchlist')
            ],
            [
                InlineKeyboardButton("🔑 Lấy Mã Đăng Nhập", callback_data='get_login_code')
            ],
            [
                InlineKeyboardButton("❓ Hướng Dẫn", callback_data='help')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📡 **Crypto Radar Control Panel**", reply_markup=reply_markup, parse_mode='Markdown')

    elif data.startswith('track_'):
        symbol = data.split('_')[1]
        if user_db.add_tracked_coin(telegram_id, symbol):
            await query.answer(f"✅ Đã thêm {symbol} vào danh sách theo dõi!")
        else:
            await query.answer(f"❌ Không thể thêm {symbol}. Kiểm tra giới hạn gói hoặc đã tồn tại.", show_alert=True)

    elif data.startswith('untrack_'):
        symbol = data.split('_')[1]
        if user_db.remove_tracked_coin(telegram_id, symbol):
            coins = user_db.get_tracked_coins(telegram_id)
            if not coins:
                keyboard = [[InlineKeyboardButton("🔙 Quay lại Menu", callback_data='main_menu')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text("📋 Bạn chưa theo dõi coin nào.", reply_markup=reply_markup)
            else:
                message = "📋 **Danh sách theo dõi của bạn:**\n\n"
                keyboard = []
                for coin in coins:
                    s = coin['symbol']
                    message += f"• {s}\n"
                    keyboard.append([InlineKeyboardButton(f"❌ Bỏ theo dõi {s}", callback_data=f"untrack_{s}")])
                keyboard.append([InlineKeyboardButton("🔙 Quay lại Menu", callback_data='main_menu')])
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
            
            await query.answer(f"🗑️ Đã xóa {symbol} khỏi danh sách.")
        else:
            await query.answer(f"❌ Lỗi khi xóa {symbol}.", show_alert=True)

async def track_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /track <SYMBOL> command"""
    telegram_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("❌ Vui lòng cung cấp symbol coin.\n\n**Ví dụ:** `/track BTC/USDT`", parse_mode='Markdown')
        return
    
    symbol = context.args[0].upper()
    if '/USDT' not in symbol:
        symbol = f"{symbol}/USDT"
    
    if user_db.add_tracked_coin(telegram_id, symbol):
        status = user_db.get_user_status(telegram_id)
        await update.message.reply_text(
            f"✅ **Đã thêm {symbol} vào danh sách theo dõi!**\n\n"
            f"Bạn đang theo dõi: {status['tracked_count']}/{status['limit']} coins",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(f"❌ Không thể thêm {symbol}. Kiểm tra giới hạn gói.", parse_mode='Markdown')

async def untrack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /untrack <SYMBOL> command"""
    telegram_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text("❌ Vui lòng cung cấp symbol coin.\n\n**Ví dụ:** `/untrack BTC/USDT`", parse_mode='Markdown')
        return
    
    symbol = context.args[0].upper()
    if '/USDT' not in symbol:
        symbol = f"{symbol}/USDT"
    
    if user_db.remove_tracked_coin(telegram_id, symbol):
        await update.message.reply_text(f"✅ Đã xóa {symbol} khỏi danh sách!", parse_mode='Markdown')
    else:
        await update.message.reply_text(f"❌ Bạn không theo dõi {symbol}!", parse_mode='Markdown')

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /list command"""
    telegram_id = update.effective_user.id
    coins = user_db.get_tracked_coins(telegram_id)
    
    if not coins:
        await update.message.reply_text("📋 Bạn chưa theo dõi coin nào.", parse_mode='Markdown')
        return
    
    message = "📋 **Danh sách theo dõi:**\n\n"
    for i, coin in enumerate(coins, 1):
        message += f"{i}. {coin['symbol']}\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    telegram_id = update.effective_user.id
    status = user_db.get_user_status(telegram_id)
    
    if not status:
        await update.message.reply_text("❌ Bạn chưa đăng ký. Gửi `/start` để bắt đầu!", parse_mode='Markdown')
        return
    
    message = f"""
📊 **Trạng thái tài khoản**

**Gói:** {status['tier'].upper()}
**Đang theo dõi:** {status['tracked_count']}/{status['limit']} coins
**Slot còn lại:** {status['slots_available']}
    """
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /login command - Generate login code for Web App"""
    telegram_id = update.effective_user.id
    
    user = user_db.get_user(telegram_id)
    if not user:
        user_db.create_user(telegram_id, update.effective_user.username)
    
    code = user_db.create_login_code(telegram_id)
    
    await update.message.reply_text(
        f"🔐 **Mã đăng nhập Web App:**\n\n`{code}`\n\n"
        f"Mã có hiệu lực trong 5 phút. Vui lòng nhập mã này vào trang web Crypto Radar.",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    message = """
📚 **Hướng dẫn sử dụng Crypto Radar Bot**

**Lệnh cơ bản:**
• `/menu` - Mở Menu tương tác (MỚI)
• `/login` - Lấy mã đăng nhập Web App (MỚI)
• `/start` - Đăng ký tài khoản
• `/track <SYMBOL>` - Theo dõi coin
• `/untrack <SYMBOL>` - Bỏ theo dõi coin
• `/list` - Xem danh sách coin đang theo dõi
• `/status` - Xem gói dịch vụ hiện tại
• `/help` - Hiển thị hướng dẫn này

**Gói dịch vụ:**
🆓 **Free:** 1 coin miễn phí
💎 **Basic ($5/tháng):** 5 coins
🚀 **Pro ($20/tháng):** Không giới hạn

**Cảnh báo tự động:**
Bot sẽ tự động gửi cảnh báo khi coin bạn theo dõi có dấu hiệu bất thường!
    """
    
    await update.message.reply_text(message, parse_mode='Markdown')

# ==================== BOT SETUP ====================

def setup_bot_commands(application: Application):
    """Register all command handlers"""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("login", login_command))
    application.add_handler(CommandHandler("track", track_command))
    application.add_handler(CommandHandler("untrack", untrack_command))
    application.add_handler(CommandHandler("list", list_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("help", help_command))
    
    application.add_handler(CallbackQueryHandler(button_handler))
