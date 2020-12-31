from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager
)

class EmailActivation:
	pass

# Create your models here.
class UserManager(BaseUserManager):
	def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have a password")

		user_obj = self.model(
			email = self.normalize_email(email)
		)
		user_obj.set_password(password)
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.active = is_active
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, email, password=None):
		user_obj = self.create_user(
			email,
			password=password,
			is_staff=True
		)
		return user_obj

	def create_superuser(self, email, password=None):
		user_obj = self.create_user(
			email,
			password=password,
			is_staff=True,
			is_admin=True
		)
		return user_obj


class User(AbstractBaseUser):
	email = models.EmailField(max_length=255, unique=True)
	# full_name = models.CharField(max_length=255)
	active = models.BooleanField(default=True) # can login
	staff = models.BooleanField(default=False) # staff user, not superuser
	admin = models.BooleanField(default=False) # superuser
	timestamp = models.DateTimeField(auto_now_add=True)
	# confirm = models.BooleanField(default=False)
	# confirm_date = models.DateTimeField(default=False)

	USERNAME_FIELD = 'email' # username

	REQUIRED_FIELD = [] #['full_name'] # python manage.py createsuperuser

	objects = UserManager()

	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_lable):
		return True


	@property
	def is_active(self):
		return self.active

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_admin(self):
		return self.admin
	


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
