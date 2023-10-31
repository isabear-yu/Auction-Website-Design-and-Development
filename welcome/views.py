from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from LuxuryAuction.models import Profile, ConfirmString
import datetime
import hashlib
from django.conf import settings
# Django transaction system so we can use @transaction.atomic
from django.db import transaction
from django.utils import timezone
import pytz

from welcome.forms import LoginForm, RegistrationForm

# Create your views here.


def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'welcome/login.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'welcome/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    if not ConfirmString.objects.get(user=new_user).has_confirmed:
        message = "You haven't verified your email！"
        return render(request, 'welcome/verification.html', locals())
    login(request, new_user)
    return redirect(reverse('homePage'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


@transaction.atomic
def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'welcome/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'welcome/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],)
    new_user.save()
    new_profile = Profile()
    new_profile.user = new_user
    new_profile.age = form.cleaned_data['age']
    new_profile.city = form.cleaned_data['city']
    new_profile.address = form.cleaned_data['address']
    new_profile.zip_code = form.cleaned_data['zip_code']
    new_profile.state = form.cleaned_data['state']
    new_profile.phone_number = form.cleaned_data['phone_number']
    new_profile.save()
    # new_user = authenticate(username=form.cleaned_data['username'],
    #                         password=form.cleaned_data['password1'])
    #
    # login(request, new_user)
    code = make_confirm_string(new_user)
    send_email(new_user.email, code)
    message = 'You have registered successfully. Please verify your email to login'
    return render(request, 'welcome/verification.html', locals())


def make_confirm_string(user):
    now = timezone.now()
    code = hash_code(user.username, now.strftime("%Y-%m-%d %H:%M:%S"))
    ConfirmString.objects.create(code=code, user=user, c_time=now)
    return code


def hash_code(s, salt='LuxuryAuction'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = 'Verification Email From LuxuryAuction'

    text_content = '''Thank you for registering LuxuryAuction. If you see these texts, your email doesn't support 
                    HTML content. Please contact us'''

    html_content = '''
                    <p>Thank you for registering LuxuryAuction.</p>
                    <p>Please click the link to verify your email</p>
                    <p>This link is valid for 7 days</p>
                    <p><a href="http://{}/welcome/verify/?code={}" target=blank>Click here!</a></p>
                    '''.format('127.0.0.1:8000', code)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def email_verify(request):
    code = request.GET.get('code', None)
    message = ''

    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = 'Invalid Request'
        return render(request, 'welcome/verification.html', locals())

    c_time = confirm.c_time
    now = timezone.now()
    if now > (c_time + datetime.timedelta(7)):
        message = 'Your email has expired. Please contact us to resend email'
        return render(request, 'welcome/verification.html', locals())
    else:
        confirm.has_confirmed = True
        confirm.save()
        message = 'Thank you for verification. Please login now！'
        return render(request, 'welcome/verification.html', locals())
