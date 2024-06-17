import random
import datetime
import secrets, string
import ssl

from django.core.mail import send_mail
from core import settings

def generate_code():
    code =random.randint(0, 9999)   

    return code

def send_code(code,email):
    try:
        a = send_mail(
                        subject= "Код для подверждение",
                        message=f'{code}',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email,],
                        fail_silently=True,
                    )
        if a==0:return "Errror"
        return "Task completed"

    except Exception as er:
        print(er)
        raise ValueError(f"{er}")



def make_bool(val):
    if str(val) == 'false' or str(val) == '0' or str(val) == 'False':
        return False
    else:
        return True


def make_next_date(day):
    now = datetime.datetime.now()
    return now + datetime.timedelta(days=day)


def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist as e:
        return None


def make_password():
    letters = string.ascii_letters
    digits = string.digits
    alphabet = letters + digits
    pwd_length = 9
    pwd = ''
    for i in range(pwd_length):
        pwd += ''.join(secrets.choice(alphabet))
    return pwd