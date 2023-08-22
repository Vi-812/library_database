from django.conf import settings
from django.core.mail import send_mail
from loguru import logger
from books.models import AppSettings

log_file_path = '../logfile.log'
logger.add(log_file_path, format='{time} {level} {message}', level='INFO')


def send_feedback(feedback_data):
    subject = "Сообщение из формы обратной связи"

    message = ""
    if feedback_data.name:
        message += f"\nИмя отправителя: {feedback_data.name}"
    message += f"\nЭлектронная почта: {feedback_data.email}"
    if feedback_data.phone:
        message += f"\nТелефон: {feedback_data.phone}"
    message += f"\nТекст сообщения: {feedback_data.message}"

    from_email = settings.EMAIL_HOST_USER

    app_settings = AppSettings.objects.first()
    recipient_list = [app_settings.feedback_email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        logger.error(f"Ошибка при отправке почты: {e}")
