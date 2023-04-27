from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.template.loader import render_to_string
from django.views import View
from .models import User
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserEditForm


def create_message(user) -> str:
    message = render_to_string(
        'registration/email_confirm.html',
        {
            'domain': '127.0.0.1:8000',
            'user': user,
            'uid': user.id,
            'token': default_token_generator.make_token(user)
        }
    )
    return message


class Register(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            # send_mail(
            #     subject="Подтвердите регистрацию",
            #     from_email='maxim.ryabtsev.631@yandex.ru',
            #     recipient_list=[user.email],
            #     message=create_message(user)
            # )

            return redirect('main')
        else:
            return render(request, 'registration/register.html', {'form': form})


class EditUser(View):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        return render(request, 'registration/settings.html', {'form': form})

    def post(self, request):
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile')
        return render(request, 'registration/settings.html', {'form': form})


def activate(request, uid: str, token: str):
    user = get_object_or_404(User, id=int(uid))

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])

        return redirect('main')
