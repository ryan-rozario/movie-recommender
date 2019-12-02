from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

u=[]
p=make_password("password")
for i in range(1,944):
    u.append(User(username=str(i), password=p))
User.objects.bulk_create(u)