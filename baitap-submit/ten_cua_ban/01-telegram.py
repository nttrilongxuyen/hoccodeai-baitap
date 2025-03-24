import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes


# Load biến môi trường từ file .env
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
# https://platform.openai.com/api-keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

# Lịch sử chat (list gồm nhiều tin nhắn, mỗi tin nhắn là một list [user_message, bot_message])
chat_history = []


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_history

    # Chuyển lịch sử chat thành dạng OpenAI có thể đọc
    messages = []

    for user_message, bot_message in chat_history:
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "assistant", "content": bot_message})

    # Thêm tin nhắn mới của user
    user_message = update.message.text
    messages.append({"role": "user", "content": user_message})

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
    )

    bot_message = chat_completion.choices[0].message.content
    chat_history.append([user_message, bot_message])

    await context.bot.send_message(chat_id=update.message.chat_id, text=bot_message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Hàm này sẽ được gọi khi bạn gửi lệnh /start
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Mình là bot, bạn có câu hỏi gì không!")

# Khởi tạo ứng dụng, gắn BOT_TOKEN vào
application = ApplicationBuilder().token(BOT_TOKEN).build()

start_handler = CommandHandler('start', start)
application.add_handler(start_handler)

chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)
application.add_handler(chat_handler)

# chạy bot cho đến khi bạn nhấn CTRL+C
print("Bot is running...")
application.run_polling()