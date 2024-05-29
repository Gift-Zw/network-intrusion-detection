from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.full_name


class NetworkTraffic(models.Model):
    duration = models.IntegerField()
    protocol_type = models.CharField(max_length=10)  # e.g., 'tcp', 'udp', 'icmp'
    service = models.CharField(max_length=50)  # e.g., 'http', 'ftp', etc.
    flag = models.CharField(max_length=10)  # e.g., 'SF', 'REJ', etc.
    src_bytes = models.IntegerField()
    dst_bytes = models.IntegerField()
    land = models.BooleanField()
    wrong_fragment = models.IntegerField()
    urgent = models.IntegerField()
    hot = models.IntegerField()
    num_failed_logins = models.IntegerField()
    logged_in = models.BooleanField()
    num_compromised = models.IntegerField()
    root_shell = models.BooleanField()
    su_attempted = models.IntegerField()
    num_root = models.IntegerField()
    num_file_creations = models.IntegerField()
    num_shells = models.IntegerField()
    num_access_files = models.IntegerField()
    num_outbound_cmds = models.IntegerField()
    is_host_login = models.BooleanField()
    is_guest_login = models.BooleanField()
    count = models.IntegerField()
    srv_count = models.IntegerField()
    serror_rate = models.FloatField()
    srv_serror_rate = models.FloatField()
    rerror_rate = models.FloatField()
    srv_rerror_rate = models.FloatField()
    same_srv_rate = models.FloatField()
    diff_srv_rate = models.FloatField()
    srv_diff_host_rate = models.FloatField()
    dst_host_count = models.IntegerField()
    dst_host_srv_count = models.IntegerField()
    dst_host_same_srv_rate = models.FloatField()
    dst_host_diff_srv_rate = models.FloatField()
    dst_host_same_src_port_rate = models.FloatField()
    dst_host_srv_diff_host_rate = models.FloatField()
    dst_host_serror_rate = models.FloatField()
    dst_host_srv_serror_rate = models.FloatField()
    dst_host_rerror_rate = models.FloatField()
    dst_host_srv_rerror_rate = models.FloatField()
    outcome = models.CharField(max_length=50)  # 'normal' or attack type
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'NetworkTraffic({self.id})'

    class Meta:
        verbose_name = 'Network Traffic'
        verbose_name_plural = 'Network Traffic'
