from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def email_html(path_template: str, assunto: str, para: list, **kwargs):
    
    html_content = render_to_string(path_template, kwargs)

    email = EmailMultiAlternatives(assunto, html_content, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 0}
