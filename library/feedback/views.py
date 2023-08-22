from random import randint
from django.shortcuts import render
from .forms import FeedbackForm
from .models import Feedback
from .send_email import send_feedback

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
            captcha = int(request.POST.get('recaptcha', 1))

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
            for field_name, field in form.fields.items():
                print(f"Field: {field_name}")
                print(f"Value: {form.cleaned_data.get(field_name)}")
                print(f"Errors: {form.errors.get(field_name)}")

            form_data = {
                'name': request.POST.get('name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone'),
                'message': request.POST.get('message'),
            }

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
