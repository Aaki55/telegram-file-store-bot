from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
import logging
from config import TELEGRAM_TOKEN, MAX_FILE_SIZE_MB, LOG_FILE

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper function to log user activity
def log_user_activity(user_id, message):
    with open(LOG_FILE, 'a') as f:
        f.write(f'User: {user_id}, Message: {message}\n')

# Command Handlers
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_text(f'Welcome, {user.first_name}!')
    log_user_activity(user.id, 'Started interaction')

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text('Send me any files, and I will store them for you!')
    log_user_activity(update.effective_user.id, 'Requested help')

async def handle_document(update: Update, context: CallbackContext):
    file = update.message.document
    file_size = file.file_size / (1024 * 1024)  # Convert bytes to MB

    if file_size > MAX_FILE_SIZE_MB:
        await update.message.reply_text('Sorry, the file exceeds the 4 GB limit.')
        log_user_activity(update.effective_user.id, 'Attempted to upload a file larger than 4 GB')
        return

    file_id = file.file_id
    new_file = await context.bot.get_file(file_id)
    file_path = f'./files/{file.file_name}'
    
    # Download the file
    await new_file.download_to_drive(file_path)
    await update.message.reply_text(f'File {file.file_name} has been stored successfully.')
    log_user_activity(update.effective_user.id, f'Uploaded file {file.file_name}')

async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Run the bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
        
