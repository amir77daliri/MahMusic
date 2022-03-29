from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth import views as AuthViews
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, SignUpForm
from Music.models import Music

User = get_user_model()


class Login(AuthViews.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class Logout(AuthViews.LogoutView):
    pass


class Register(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('registration/active_account_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(self.request, 'registration/confirm_email_send.html', {'email': form.cleaned_data.get('email')})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request, 'registration/confirm_active_email_send.html', {})
    else:
        return HttpResponse('Activation link is invalid!')
