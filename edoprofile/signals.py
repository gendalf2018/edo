from django.conf import settings
from django.db.models.signals import post_save

def post_save_receiver(sender, instance, created, **kwargs):
    print('NEW USER SAVED')

post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)
