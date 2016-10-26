# coding=utf-8
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import Signal
from django.core.urlresolvers import reverse

notify = Signal(providing_args=['domain'])


def new_notification(sender, **kwargs):
    domain = kwargs.pop("domain")
    full_url = 'https://%s%s' % (domain, sender.get_absolute_url())
    qs = User.objects.filter(userprofile__subs__in=[sender.blog])
    recipients = [x[0] for x in qs.values_list('email')]

    subject = u'Новый пост в вашей ленте'
    text_content = u'Новый пост вы можете прочитать по ссылке %s' % (full_url)
    sender = settings.EMAIL_HOST_USER

    send_mail(subject, text_content, sender, recipients, fail_silently=True)



notify.connect(new_notification)