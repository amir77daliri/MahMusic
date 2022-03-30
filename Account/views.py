from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth import (
    views as auth_views,
    update_session_auth_hash
)
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, ListView
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    LoginForm,
    SignUpForm,
    ProfileUpdateForm,
    ChangePasswordForm,
    MyPasswordResetForm,
    SetNewResetPasswordForm
)
from Music.models import Music

User = get_user_model()


class Login(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class Logout(LoginRequiredMixin, auth_views.LogoutView):
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


class Profile(LoginRequiredMixin, ListView):
    model = Music
    template_name = 'Account/profile.html'
    paginate_by = 12
    context_object_name = 'musics'

    def get_queryset(self):
        return Music.objects.all().order_by('name')


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'Account/profile_update.html'
    success_url = reverse_lazy('account:profile')

    def get_object(self, **kwargs):
        user = get_object_or_404(User, pk=self.request.user.id)
        return user


@login_required()
def change_password(request):
    form = ChangePasswordForm(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('account:profile')
    context = {
        'form': form
    }
    return render(request, 'registration/password_change_form.html', context)


class MyPasswordReset(auth_views.PasswordResetView):
    form_class = MyPasswordResetForm
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')


class MyPasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class MyPasswordResetConfirm(auth_views.PasswordResetConfirmView):
    form_class = SetNewResetPasswordForm
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('account:profile')
