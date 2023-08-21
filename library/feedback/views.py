from random import randint
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from .forms import FeedbackForm
from .models import Feedback
from books.models import AppSettings


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

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def feedback_view(request):
    if request.method == "GET":
        captcha_num1 = randint(0, 20)
        captcha_num2 = randint(0, 20)
        form = FeedbackForm()
        context = {
            "form": form,
            "captcha_num1": captcha_num1,
            "captcha_num2": captcha_num2,
        }
        return render(request, 'feedback/feedback_form.html', context)
    else:
        form = FeedbackForm(request.POST)
        if form.is_valid():

            form_captcha1 = int(request.POST.get('captcha_num1', 0))
            form_captcha2 = int(request.POST.get('captcha_num2', 0))
            captcha = int(request.POST.get('captcha', 1))

            if captcha == form_captcha1 + form_captcha2:
                feedback_data = Feedback(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    message=form.cleaned_data['message']
                )
                feedback_data.save()

                send_feedback(feedback_data)

                form = FeedbackForm()
                captcha_num1 = randint(0, 20)
                captcha_num2 = randint(0, 20)
                context = {
                    "form": form,
                    "captcha_num1": captcha_num1,
                    "captcha_num2": captcha_num2,
                    "message_to_user": "Сообщение успешно отправлено!",
                }
                return render(request, 'feedback/feedback_form.html', context)

            else:
                captcha_num1 = randint(0, 20)
                captcha_num2 = randint(0, 20)
                context = {
                    "form": form,
                    "captcha_num1": captcha_num1,
                    "captcha_num2": captcha_num2,
                    "message_to_user": "Ошибка проверки поля captcha! Попробуйте еще раз!",
                }
                return render(request, 'feedback/feedback_form.html', context)
        else:
            print(form.errors)

            form_data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone'),
                'message': request.POST.get('message'),
            }

            print(form_data)
            form = FeedbackForm(initial=form_data)

            captcha_num1 = randint(0, 20)
            captcha_num2 = randint(0, 20)
            context = {
                "form": form,
                "captcha_num1": captcha_num1,
                "captcha_num2": captcha_num2,
                "message_to_user": "Ошибка заполнения формы! Попробуйте еще раз!",
            }
            return render(request, 'feedback/feedback_form.html', context)
