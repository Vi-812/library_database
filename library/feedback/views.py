import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import FeedbackForm


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        captcha_num1 = random.randint(0, 20)
        captcha_num2 = random.randint(0, 20)
        if form.is_valid():
            captcha_answer = request.POST.get('captcha')
            captcha_solution = str(captcha_num1 + captcha_num2)

            if captcha_answer == captcha_solution:
                feedback = form.save()

                subject = 'New Feedback'
                message = f"Name: {feedback.name}\nEmail: {feedback.email}\nMessage: {feedback.message}"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [settings.FEEDBACK_EMAIL]
                send_mail(subject, message, from_email, recipient_list)

                return redirect('success_page')
            else:
                context = {
                    'form': form,
                    'captcha_error': True,
                    'captcha_num1': captcha_num1,
                    'captcha_num2': captcha_num2
                }
                return render(request, 'feedback/feedback_form.html', context)
        else:
            context = {'form': form, 'captcha_num1': captcha_num1, 'captcha_num2': captcha_num2}
            return render(request, 'feedback/feedback_form.html', context)
    else:
        captcha_num1 = random.randint(0, 20)
        captcha_num2 = random.randint(0, 20)
        form = FeedbackForm()
        context = {'form': form, 'captcha_num1': captcha_num1, 'captcha_num2': captcha_num2}
        return render(request, 'feedback/feedback_form.html', context)
