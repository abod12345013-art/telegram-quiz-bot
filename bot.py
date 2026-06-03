import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from config import TELEGRAM_BOT_TOKEN
from utils.pdf_extractor import extract_text_from_pdf
from utils.docx_extractor import extract_text_from_docx
from utils.question_parser import parse_mcq_questions

# إعداد التسجيل (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /start"""
    await update.message.reply_text(
        "مرحباً! أنا بوت تحويل الملفات إلى استطلاعات رأي (Quiz Polls).\n"
        "أرسل لي ملف PDF أو DOCX يحتوي على أسئلة MCQ وسأقوم بتحويلها لك."
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الملفات المرسلة"""
    document = update.message.document
    file_name = document.file_name
    file_ext = os.path.splitext(file_name)[1].lower()

    if file_ext not in ['.pdf', '.docx']:
        await update.message.reply_text("عذراً، أنا أدعم ملفات PDF و DOCX فقط.")
        return

    await update.message.reply_text(f"جاري معالجة الملف: {file_name}...")

    # تحميل الملف
    new_file = await context.bot.get_file(document.file_id)
    file_path = f"downloads/{document.file_id}{file_ext}"
    os.makedirs("downloads", exist_ok=True)
    await new_file.download_to_drive(file_path)

    # استخراج النص
    text = ""
    if file_ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_ext == '.docx':
        text = extract_text_from_docx(file_path)

    if not text:
        await update.message.reply_text("فشل استخراج النص من الملف.")
        return

    # تحليل الأسئلة
    questions = parse_mcq_questions(text)

    if not questions:
        await update.message.reply_text("لم أجد أي أسئلة MCQ في هذا الملف.")
        return

    await update.message.reply_text(f"تم العثور على {len(questions)} سؤال. جاري إنشاء استطلاعات الرأي...")

    # إنشاء استطلاعات الرأي (Quiz Polls)
    for q in questions:
        try:
            # التأكد من أن عدد الخيارات يتراوح بين 2 و 10 (قيود تيليجرام)
            options = q['options'][:10]
            if len(options) < 2:
                continue

            await context.bot.send_poll(
                chat_id=update.effective_chat.id,
                question=q['question'],
                options=options,
                type='quiz',
                correct_option_id=q['correct_option_id'], # افتراضي، يمكن تطويره لاحقاً
                is_anonymous=False
            )
        except Exception as e:
            logging.error(f"خطأ أثناء إرسال الاستطلاع: {e}")

    # حذف الملف بعد المعالجة
    if os.path.exists(file_path):
        os.remove(file_path)

if __name__ == '__main__':
    # التحقق من وجود التوكن
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        print("خطأ: يرجى وضع توكن البوت الخاص بك في ملف config.py")
    else:
        application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        
        start_handler = CommandHandler('start', start)
        document_handler = MessageHandler(filters.Document.ALL, handle_document)
        
        application.add_handler(start_handler)
        application.add_handler(document_handler)
        
        print("البوت يعمل الآن...")
        application.run_polling()
