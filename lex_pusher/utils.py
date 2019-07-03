from hashlib import md5
from django.conf import settings


def fk_hash(p1, p2, check=False):
    secret = settings.FK_SECRET_2 if check else settings.FK_SECRET_1
    hash = f"{settings.FK_ID}:{p1}:{secret}:{p2}"
    hash = md5(hash.encode('utf-8')).hexdigest()
    return hash


def fk_url(price, desc):
    return f"http://www.free-kassa.ru/merchant/cash.php?m={settings.FK_ID}&oa={price}&o={desc}&s={fk_hash(price, desc)}"

