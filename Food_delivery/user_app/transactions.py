from . models import Account
# from restuarant.models import Manager
from django.contrib.auth import authenticate
from django.db import transaction




@transaction.atomic
def register_user_with_email_and_password(email, password):
    user = User.objects.create_user(email=email, name=email, password=password)
    user.save()
    manager = Manager.objects.create(user=user)
    manager.save()
    return user