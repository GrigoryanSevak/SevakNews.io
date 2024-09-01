from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

def send_email_for_verify(request, user):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    
    html_message = render_to_string(
        template_name='Users/verify_email.html',
        context=context,
    )
    
    email = EmailMessage(
        'Верификация почты',
        html_message,
        'sevak.grigoryan.06@mail.ru',
        to=[user.email],
    )
    
    email.content_subtype = 'html'
    
    email.send()