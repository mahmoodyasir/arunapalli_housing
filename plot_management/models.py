from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("User must have an email.")

        email = self.normalize_email(email)
        user = self.model(email=email,  **kwargs)
        user.set_password(password)
        user.is_superuser = False
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class Profile(models.Model):
    prouser = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/images/users', null=True, blank=True)

    def __str__(self):
        return self.prouser.email


class Status(models.Model):
    title = models.CharField(max_length=199)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Member(models.Model):
    member_email = models.ForeignKey(Profile, on_delete=models.CASCADE)
    member_firstname = models.CharField(max_length=200)
    member_lastname = models.CharField(max_length=200)
    member_nid = models.CharField(max_length=200)
    member_phone = models.CharField(max_length=200)
    member_status = models.ForeignKey(Status, on_delete=models.CASCADE, default=3)

    def __str__(self):
        return f"{self.member_email}=={self.member_firstname}=={self.member_lastname}=={self.member_nid}"


class PaymentStatus(models.Model):
    member_email = models.ForeignKey(Profile, on_delete=models.CASCADE)
    payment_complete = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.member_email


class OfflinePayment(models.Model):
    member_email = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cheque_number = models.CharField(max_length=255, unique=True)
    account_no = models.CharField(max_length=255)
    member_nid = models.CharField(max_length=200)
    plot_no = models.CharField(max_length=199)
    road_no = models.CharField(max_length=199)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.member_email}=={self.account_no}=={self.plot_no}=={self.road_no}=={self.payment_date}"


